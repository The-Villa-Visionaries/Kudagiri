from concurrent.futures import ThreadPoolExecutor
from datetime import date, datetime, timedelta, timezone
from decimal import Decimal
from threading import Barrier
from uuid import uuid4

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.core import dates
from app.core.security import create_access_token
from app.database.sessions import create_database_engine
from app.main import create_app
from app.models.booking import Booking, RoomNight, Ticket, TicketSession, TicketStaff
from app.models.hotel import Room
from app.models.user import User
from app.seed import seed_ticket_sessions
from app.services import serviceBookings

NOW = datetime(2030, 1, 10, 6, tzinfo=timezone.utc)
STAY = {"room_id": 1, "check_in": "2030-01-11", "check_out": "2030-01-14", "guests": 2}


@pytest.fixture(autouse=True)
def fixed_clock(monkeypatch):
    monkeypatch.setattr(dates, "utc_now", lambda: NOW)
    monkeypatch.setattr(serviceBookings, "utc_now", lambda: NOW)


@pytest.fixture
def actors(client, engine, auth_settings):
    with Session(engine) as session:
        session.add_all([
            User(id=i, full_name=name, email=f"actor{i}@example.com", hashed_password="unused-bearer-test")
            for i, name in [(1, "Guest One"), (2, "Guest Two"), (3, "Park Staff")]
        ])
        session.flush()
        session.add(TicketStaff(user_id=3, kind="theme_park"))
        session.commit()
    return {
        name: {"Authorization": "Bearer " + create_access_token(user_id, auth_settings)}
        for name, user_id in [("owner", 1), ("other", 2), ("staff", 3)]
    }


@pytest.fixture
def slots(actors, engine):
    with Session(engine) as session:
        for slot_id, kind, hours, capacity, price in [
            (1, "ferry", 2, 2, "15.25"),
            (2, "theme_park", 3, 5, "28.10"),
            (3, "ferry", -25, 20, "10.00"),
            (4, "theme_park", 27, 20, "30.00"),
        ]:
            session.add(TicketSession(
                id=slot_id, kind=kind, name=f"Session {slot_id}", location="Test island",
                starts_at=NOW + timedelta(hours=hours), ends_at=NOW + timedelta(hours=hours + 1),
                capacity=capacity, price=Decimal(price), currency="USD",
            ))
        session.commit()


def reserve(client, actors, **changes):
    return client.post("/api/bookings", headers=actors["owner"], json={**STAY, **changes})


def buy(client, actors, session_id=2, quantity=2):
    return client.post("/api/tickets", headers=actors["owner"], json={"session_id": session_id, "quantity": quantity})


def test_booking_price_owner_and_persistence(client, actors, engine, auth_settings):
    response = reserve(client, actors)
    assert response.status_code == 201
    record = response.json()
    assert record["user_id"] == 1 and record["nights"] == 3
    assert record["unit_price"] == "780.00" and record["total_price"] == "2340.00"
    assert record["status"] == "confirmed" and record["currency"] == "USD"
    assert record["created_at"].endswith("Z")
    assert response.headers["cache-control"] == "no-store"
    with Session(engine) as session:
        assert session.scalar(select(func.count()).select_from(RoomNight)) == 3
        session.get(Room, 1).price_per_night = Decimal("999.99")
        session.commit()
    restarted_engine = create_database_engine(str(engine.url))
    try:
        with TestClient(create_app(restarted_engine, auth_settings)) as restarted:
            saved = restarted.get(f"/api/bookings/{record['id']}", headers=actors["owner"])
            assert saved.status_code == 200 and saved.json()["total_price"] == "2340.00"
    finally:
        restarted_engine.dispose()


@pytest.mark.parametrize("changes", [
    {"check_in": "2030-01-09"}, {"check_out": "2030-01-11"},
    {"check_out": "2030-01-10"}, {"check_out": "2032-01-11"},
    {"check_in": "not-a-date"}, {"guests": 0}, {"guests": True},
    {"guests": 3}, {"room_id": 0}, {"room_id": 2**63},
    {"user_id": 2}, {"total_price": "0.01"}, {"status": "confirmed"},
    {"promo_code": "FREE"},
])
def test_invalid_booking(client, actors, engine, changes):
    assert reserve(client, actors, **changes).status_code == 422
    with Session(engine) as session:
        assert session.scalar(select(func.count()).select_from(Booking)) == 0
        assert session.scalar(select(func.count()).select_from(RoomNight)) == 0


def test_missing_room(client, actors):
    assert reserve(client, actors, room_id=999).status_code == 404


def test_overlapping_booking_rolls_back_all_nights(client, actors, engine):
    assert reserve(client, actors, check_in="2030-01-12").status_code == 201
    assert reserve(client, actors, check_out="2030-01-13").status_code == 409
    with Session(engine) as session:
        assert session.scalar(select(func.count()).select_from(Booking)) == 1
        assert session.get(RoomNight, (1, date(2030, 1, 11))) is None
    assert reserve(client, actors, check_out="2030-01-12").status_code == 201
    assert reserve(client, actors, check_in="2030-01-14", check_out="2030-01-15").status_code == 201


def test_room_availability_filters_and_cancellation(client, actors):
    booking = reserve(client, actors).json()
    query = "check_in=2030-01-11&check_out=2030-01-14"
    for path in ["/api/rooms", "/api/hotels/1/rooms"]:
        response = client.get(f"{path}?{query}")
        assert response.status_code == 200
        assert 1 not in [room["id"] for room in response.json()["items"]]
    assert client.get(f"/api/rooms?{query}").json()["total"] == 3
    assert client.get("/api/rooms?check_in=2030-01-14&check_out=2030-01-15").json()["total"] == 4
    for _ in range(2):
        cancelled = client.post(f"/api/bookings/{booking['id']}/cancel", headers=actors["owner"])
        assert cancelled.status_code == 200 and cancelled.json()["status"] == "cancelled"
    assert client.get(f"/api/rooms?{query}").json()["total"] == 4
    assert reserve(client, actors).status_code == 201


@pytest.mark.parametrize("query", [
    "check_in=2030-01-11", "check_out=2030-01-14",
    "check_in=2030-01-09&check_out=2030-01-14",
    "check_in=2030-01-14&check_out=2030-01-11",
    "check_in=2030-01-11&check_out=2032-01-14",
])
def test_invalid_availability_dates(client, query):
    assert client.get(f"/api/rooms?{query}").status_code == 422


def test_booking_privacy_and_pagination(client, actors):
    first = reserve(client, actors).json()
    assert reserve(client, actors, room_id=2).status_code == 201
    for method, path in [("GET", f"/api/bookings/{first['id']}"), ("POST", f"/api/bookings/{first['id']}/cancel")]:
        assert client.request(method, path, headers=actors["other"]).status_code == 404
    assert client.get("/api/bookings", headers=actors["other"]).json()["items"] == []
    listing = client.get("/api/bookings?skip=1&limit=1", headers=actors["owner"]).json()
    assert listing["total"] == 2 and listing["items"][0]["id"] == first["id"]
    assert client.get("/api/bookings?status=cancelled", headers=actors["owner"]).json()["total"] == 0


def test_check_in_day_cannot_be_cancelled(client, actors):
    booking = reserve(client, actors, check_in="2030-01-10").json()
    assert client.post(f"/api/bookings/{booking['id']}/cancel", headers=actors["owner"]).status_code == 409


def race_requests(function, count):
    barrier = Barrier(count)
    def run(_):
        barrier.wait(timeout=10)
        return function()
    with ThreadPoolExecutor(max_workers=count) as pool:
        return list(pool.map(run, range(count), timeout=30))


def test_concurrent_room_reservations(client, actors, engine):
    responses = race_requests(lambda: reserve(client, actors), 4)
    assert sorted(response.status_code for response in responses) == [201, 409, 409, 409]
    with Session(engine) as session:
        assert session.scalar(select(func.count()).select_from(Booking)) == 1
        assert session.scalar(select(func.count()).select_from(RoomNight)) == 3


def test_session_catalogue(client, slots):
    page = client.get("/api/ticket-sessions").json()
    assert page["total"] == 3
    assert [item["id"] for item in page["items"]] == [1, 2, 4]
    page = client.get("/api/ticket-sessions?kind=theme_park&session_date=2030-01-10").json()
    assert page["total"] == 1 and page["items"][0]["id"] == 2
    assert page["items"][0]["remaining_capacity"] == 5
    assert page["items"][0]["starts_at"].endswith("Z")
    assert client.get("/api/ticket-sessions?skip=1&limit=1").json()["total"] == 3
    assert client.get("/api/ticket-sessions/999").status_code == 404


def test_ticket_price_and_capacity(client, actors, slots, engine):
    response = buy(client, actors)
    assert response.status_code == 201
    ticket = response.json()
    assert ticket["holder_name"] == "Guest One"
    assert ticket["unit_price"] == "28.10" and ticket["total_price"] == "56.20"
    assert ticket["remaining_uses"] == 2 and ticket["session"]["remaining_capacity"] == 3
    assert ticket["used_quantity"] == 0 and ticket["user_id"] == 1
    with Session(engine) as session:
        session.get(TicketSession, 2).price = Decimal("35.00")
        session.commit()
    assert client.get(f"/api/tickets/{ticket['id']}", headers=actors["owner"]).json()["total_price"] == "56.20"


@pytest.mark.parametrize("changes", [
    {"quantity": 0}, {"quantity": -1}, {"quantity": True}, {"quantity": 1.5},
    {"quantity": 101}, {"session_id": 0}, {"session_id": 2**63},
    {"user_id": 2}, {"unit_price": "0.01"}, {"kind": "ferry"},
])
def test_invalid_ticket_request(client, actors, slots, changes):
    response = client.post("/api/tickets", headers=actors["owner"], json={"session_id": 2, "quantity": 1, **changes})
    assert response.status_code == 422
    assert client.get("/api/ticket-sessions/2").json()["remaining_capacity"] == 5


def test_sold_out_started_and_missing_sessions(client, actors, slots):
    assert buy(client, actors, session_id=999).status_code == 404
    assert buy(client, actors, session_id=3).status_code == 409
    assert buy(client, actors, session_id=1, quantity=3).status_code == 409
    assert buy(client, actors, session_id=1, quantity=2).status_code == 201
    assert buy(client, actors, session_id=1, quantity=1).status_code == 409


def test_ticket_privacy_and_cancellation(client, actors, slots):
    ticket = buy(client, actors).json()
    assert client.get(f"/api/tickets/{ticket['id']}", headers=actors["other"]).status_code == 404
    assert client.post(f"/api/tickets/{ticket['id']}/cancel", headers=actors["other"]).status_code == 404
    assert client.get("/api/tickets", headers=actors["other"]).json()["total"] == 0
    assert client.get("/api/tickets?limit=1", headers=actors["owner"]).json()["total"] == 1
    for _ in range(2):
        response = client.post(f"/api/tickets/{ticket['id']}/cancel", headers=actors["owner"])
        assert response.status_code == 200
        assert response.json()["remaining_uses"] == 0
    assert client.get("/api/ticket-sessions/2").json()["remaining_capacity"] == 5
    assert client.get("/api/tickets?status=cancelled", headers=actors["owner"]).json()["total"] == 1


def test_concurrent_ticket_capacity(client, actors, slots, engine):
    responses = race_requests(lambda: buy(client, actors, session_id=1, quantity=1), 4)
    assert sorted(response.status_code for response in responses) == [201, 201, 409, 409]
    with Session(engine) as session:
        assert session.scalar(select(func.count()).select_from(Ticket)) == 2
        assert session.get(TicketSession, 1).reserved_quantity == 2


def test_concurrent_ticket_cancellation_releases_once(client, actors, slots):
    ticket = buy(client, actors).json()
    responses = race_requests(lambda: client.post(f"/api/tickets/{ticket['id']}/cancel", headers=actors["owner"]), 2)
    assert [response.status_code for response in responses] == [200, 200]
    assert client.get("/api/ticket-sessions/2").json()["remaining_capacity"] == 5


def test_staff_lookup_redemption_and_permission_scope(client, actors, slots):
    ticket = buy(client, actors).json()
    payload = {"ticket_code": ticket["code"], "session_id": 2}
    assert client.get("/api/tickets/staff-permissions", headers=actors["owner"]).json() == []
    assert client.get("/api/tickets/staff-permissions", headers=actors["staff"]).json() == ["theme_park"]
    assert client.post("/api/tickets/validate?role=Admin", headers=actors["owner"], json=payload).status_code == 403
    assert client.post("/api/tickets/validate", headers=actors["staff"], json=payload).status_code == 200
    ferry = buy(client, actors, session_id=1).json()
    assert client.post("/api/tickets/validate", headers=actors["staff"], json={"ticket_code": ferry["code"], "session_id": 1}).status_code == 404
    used = client.post("/api/tickets/redeem", headers=actors["staff"], json={**payload, "quantity": 1})
    assert used.status_code == 200 and used.json()["remaining_uses"] == 1
    assert client.post(f"/api/tickets/{ticket['id']}/cancel", headers=actors["owner"]).status_code == 409
    assert client.post("/api/tickets/redeem", headers=actors["staff"], json={**payload, "quantity": 2}).status_code == 409
    assert client.post("/api/tickets/redeem", headers=actors["staff"], json={**payload, "quantity": 1}).status_code == 200
    assert client.post("/api/tickets/validate", headers=actors["staff"], json=payload).status_code == 409
    assert client.get("/api/ticket-sessions/2").json()["remaining_capacity"] == 3


def test_invalid_ticket_codes_dates_and_cancellation(client, actors, slots, monkeypatch):
    ticket = buy(client, actors).json()
    payload = {"ticket_code": ticket["code"], "session_id": 2}
    assert client.post("/api/tickets/validate", headers=actors["staff"], json={**payload, "ticket_code": str(uuid4())}).status_code == 404
    assert client.post("/api/tickets/validate", headers=actors["staff"], json={**payload, "session_id": 4}).status_code == 404
    assert client.post("/api/tickets/validate", headers=actors["staff"], json={**payload, "ticket_code": "bad-code"}).status_code == 422
    tomorrow = buy(client, actors, session_id=4).json()
    assert client.post("/api/tickets/validate", headers=actors["staff"], json={"ticket_code": tomorrow["code"], "session_id": 4}).status_code == 409
    assert client.post(f"/api/tickets/{ticket['id']}/cancel", headers=actors["owner"]).status_code == 200
    assert client.post("/api/tickets/validate", headers=actors["staff"], json=payload).status_code == 409
    fresh = buy(client, actors).json()
    monkeypatch.setattr(serviceBookings, "utc_now", lambda: NOW + timedelta(hours=5))
    assert client.post(f"/api/tickets/{fresh['id']}/cancel", headers=actors["owner"]).status_code == 409
    assert client.post("/api/tickets/validate", headers=actors["staff"], json={**payload, "ticket_code": fresh["code"]}).status_code == 409


def test_staff_revocation_applies_to_existing_token(client, actors, slots, engine):
    ticket = buy(client, actors).json()
    with Session(engine) as session:
        session.delete(session.get(TicketStaff, (3, "theme_park")))
        session.commit()
    assert client.post("/api/tickets/validate", headers=actors["staff"], json={"ticket_code": ticket["code"], "session_id": 2}).status_code == 403


def test_concurrent_redemption_cannot_overuse(client, actors, slots):
    ticket = buy(client, actors).json()
    data = {"ticket_code": ticket["code"], "session_id": 2, "quantity": 2}
    responses = race_requests(lambda: client.post("/api/tickets/redeem", headers=actors["staff"], json=data), 2)
    assert sorted(response.status_code for response in responses) == [200, 409]
    assert client.get(f"/api/tickets/{ticket['id']}", headers=actors["owner"]).json()["used_quantity"] == 2


def test_redemption_racing_cancellation_stays_consistent(client, actors, slots, engine):
    ticket = buy(client, actors).json()
    barrier = Barrier(2)
    def cancel():
        barrier.wait(timeout=10)
        return client.post(f"/api/tickets/{ticket['id']}/cancel", headers=actors["owner"])
    def redeem():
        barrier.wait(timeout=10)
        return client.post("/api/tickets/redeem", headers=actors["staff"], json={"ticket_code": ticket["code"], "session_id": 2, "quantity": 1})
    with ThreadPoolExecutor(max_workers=2) as pool:
        futures = [pool.submit(cancel), pool.submit(redeem)]
        responses = [future.result(timeout=20) for future in futures]
    assert sorted(response.status_code for response in responses) == [200, 409]
    with Session(engine) as session:
        saved = session.get(Ticket, ticket["id"])
        assert (saved.status, saved.used_quantity, saved.session.reserved_quantity) in [
            ("cancelled", 0, 0), ("confirmed", 1, 2),
        ]


@pytest.mark.parametrize(("method", "path", "body"), [
    ("POST", "/api/bookings", STAY), ("GET", "/api/bookings", None),
    ("GET", "/api/bookings/1", None), ("POST", "/api/bookings/1/cancel", None),
    ("POST", "/api/tickets", {"session_id": 1, "quantity": 1}),
    ("GET", "/api/tickets", None), ("GET", "/api/tickets/1", None),
    ("POST", "/api/tickets/1/cancel", None),
    ("POST", "/api/tickets/validate", {"ticket_code": str(uuid4()), "session_id": 1}),
    ("POST", "/api/tickets/redeem", {"ticket_code": str(uuid4()), "session_id": 1, "quantity": 1}),
])
def test_authentication_required(client, method, path, body):
    assert client.request(method, path, json=body).status_code == 401


@pytest.mark.parametrize("path", [
    "/api/bookings?limit=101", "/api/bookings?skip=-1", "/api/bookings?status=unknown",
    "/api/tickets?limit=0", "/api/tickets?status=unknown", "/api/tickets/9223372036854775808",
    "/api/ticket-sessions?kind=unknown", "/api/ticket-sessions?session_date=invalid",
])
def test_invalid_list_parameters(client, actors, path):
    assert client.get(path, headers=actors["owner"]).status_code == 422


def test_demo_ticket_seed_is_separate_and_repeatable(client, engine):
    with Session(engine) as session:
        assert seed_ticket_sessions(session) is True
        assert seed_ticket_sessions(session) is False
        assert session.scalar(select(func.count()).select_from(TicketSession)) == 2
        assert session.scalar(select(func.count()).select_from(Room)) == 4
