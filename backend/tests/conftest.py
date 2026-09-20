from decimal import Decimal

import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from app.core.config import AuthSettings
from app.database.sessions import create_database_engine
from app.main import create_app
from app.models.hotel import Hotel, Room


@pytest.fixture
def engine(tmp_path):
    engine = create_database_engine(f"sqlite:///{(tmp_path / 'test.db').as_posix()}")
    yield engine
    engine.dispose()


@pytest.fixture
def auth_settings():
    return AuthSettings(secret_key="test-only-signing-key-never-use-in-deployment-" * 2)


@pytest.fixture
def empty_client(engine, auth_settings):
    with TestClient(create_app(engine, auth_settings)) as client:
        yield client


@pytest.fixture
def client(empty_client, engine):
    with Session(engine) as session:
        session.add_all([
            Hotel(id=1, name="Island Hotel", location="North island"),
            Hotel(id=2, name="Garden Hotel", location="South island"),
            Hotel(id=3, name="Empty Hotel", location="East island"),
        ])
        session.flush()
        for room_id, hotel_id, name, category, price, guests in [
            (1, 1, "Deluxe Room", "beachfront", "780.00", 2),
            (2, 1, "Family Villa", "family", "650.00", 4),
            (3, 2, "Garden Bungalow", "garden", "320.00", 2),
            (4, 2, "Ocean Suite", "ocean_suite", "780.00", 3),
        ]:
            session.add(Room(
                id=room_id, hotel_id=hotel_id, name=name, category=category,
                description="Private pool" if room_id == 1 else "Island stay",
                price_per_night=Decimal(price), currency="USD", max_guests=guests,
                size_sqm=95, bed_type="King bed", amenities=["WiFi"],
            ))
        session.commit()
    yield empty_client
