import pytest
from fastapi.testclient import TestClient
from sqlalchemy import func, select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.database.sessions import create_database_engine
from app.main import create_app
from app.models.hotel import Hotel, Room
from app.seed import seed_demo_data


def test_startup_health_and_empty_catalogue(empty_client):
    assert empty_client.get("/health").json() == {"status": "ok"}
    for path in ["/api/hotels", "/api/rooms"]:
        response = empty_client.get(path)
        assert response.status_code == 200
        assert response.json() == {"items": [], "total": 0, "skip": 0, "limit": 20}


def test_hotel_pagination_and_detail(client):
    page = client.get("/api/hotels?skip=1&limit=1").json()
    assert page["total"] == 3
    assert page["skip"] == 1 and page["limit"] == 1
    assert [hotel["id"] for hotel in page["items"]] == [2]
    response = client.get("/api/hotels/1")
    assert response.status_code == 200
    assert response.json()["name"] == "Island Hotel"


def test_room_response_and_hotel_scope(client):
    response = client.get("/api/rooms/1")
    assert response.status_code == 200
    assert response.headers["content-type"] == "application/json"
    room = response.json()
    assert room["price_per_night"] == "780.00"
    assert room["currency"] == "USD"
    assert room["amenities"] == ["WiFi"]
    assert room["image_url"] is None
    page = client.get("/api/hotels/1/rooms").json()
    assert page["total"] == 2
    assert {room["hotel_id"] for room in page["items"]} == {1}
    assert client.get("/api/hotels/3/rooms").json()["items"] == []


@pytest.mark.parametrize(("query", "expected_ids"), [
    ("category=garden", [3]),
    ("guests=3", [2, 4]),
    ("max_price=650", [2, 3]),
    ("q=DELUXE", [1]),
    ("q=pool", [1]),
    ("q=%25", []),
    ("q=_", []),
    ("q=%27%20OR%201%3D1--", []),
    ("guests=4&max_price=650&category=family", [2]),
    ("sort=price_asc", [3, 2, 1, 4]),
    ("sort=price_desc", [1, 4, 2, 3]),
])
def test_room_filters_and_sort(client, query, expected_ids):
    response = client.get(f"/api/rooms?{query}")
    assert response.status_code == 200
    page = response.json()
    assert [room["id"] for room in page["items"]] == expected_ids
    assert page["total"] == len(expected_ids)


def test_filtered_total_and_pagination(client):
    page = client.get("/api/rooms?guests=2&sort=price_asc&skip=1&limit=2").json()
    assert page["total"] == 4
    assert page["skip"] == 1 and page["limit"] == 2
    assert [room["id"] for room in page["items"]] == [2, 1]
    assert client.get("/api/rooms?skip=100").json()["items"] == []
    page = client.get("/api/hotels/1/rooms?category=garden").json()
    assert page["total"] == 0 and page["items"] == []


@pytest.mark.parametrize(("path", "detail"), [
    ("/api/hotels/999", "Hotel not found"),
    ("/api/hotels/999/rooms", "Hotel not found"),
    ("/api/rooms/999", "Room not found"),
])
def test_missing_records(client, path, detail):
    response = client.get(path)
    assert response.status_code == 404
    assert response.json() == {"detail": detail}


@pytest.mark.parametrize("path", [
    "/api/hotels/0", "/api/rooms/-1", "/api/rooms/abc",
    "/api/hotels?skip=-1", "/api/hotels?limit=0", "/api/hotels?limit=101",
    "/api/rooms?limit=101", "/api/rooms?skip=-1", "/api/rooms?guests=0",
    "/api/rooms?guests=two", "/api/rooms?max_price=-1",
    "/api/rooms?max_price=NaN", "/api/rooms?max_price=Infinity",
    "/api/rooms?max_price=10.001", "/api/rooms?category=unknown",
    "/api/rooms?sort=unknown", "/api/rooms?q=", "/api/rooms?q=" + "a" * 101,
    "/api/hotels/1/rooms?guests=0",
])
def test_invalid_requests(client, path):
    response = client.get(path)
    assert response.status_code == 422
    assert response.json()["detail"]


def test_catalogue_persists_across_app_restart(client, engine, auth_settings):
    restarted_engine = create_database_engine(str(engine.url))
    try:
        with TestClient(create_app(restarted_engine, auth_settings)) as restarted_client:
            assert restarted_client.get("/api/rooms").json()["total"] == 4
    finally:
        restarted_engine.dispose()


def test_cors(client):
    headers = {"Origin": "http://localhost:5173", "Access-Control-Request-Method": "GET"}
    response = client.options("/api/rooms", headers=headers)
    assert response.status_code == 200
    assert response.headers["access-control-allow-origin"] == "http://localhost:5173"
    response = client.get("/api/rooms", headers={"Origin": "https://unrelated.example"})
    assert "access-control-allow-origin" not in response.headers


def test_catalogue_is_read_only(client):
    assert client.post("/api/rooms", json={}).status_code == 405


def test_demo_seed_is_optional_and_does_not_duplicate(empty_client, engine):
    with Session(engine) as session:
        assert seed_demo_data(session) is True
        assert seed_demo_data(session) is False
        assert session.scalar(select(func.count()).select_from(Hotel)) == 1
        assert session.scalar(select(func.count()).select_from(Room)) == 4


def test_demo_seed_preserves_existing_catalogue(client, engine):
    with Session(engine) as session:
        assert seed_demo_data(session) is False
    assert client.get("/api/hotels/1").json()["name"] == "Island Hotel"


def test_database_rejects_orphan_room(empty_client, engine):
    with Session(engine) as session:
        session.add(Room(
            hotel_id=999, name="Orphan", category="garden", price_per_night=10,
            max_guests=2, size_sqm=20, bed_type="Queen bed",
        ))
        with pytest.raises(IntegrityError):
            session.commit()
