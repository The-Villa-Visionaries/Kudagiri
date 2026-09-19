"""Optional sample catalogue for local development: python -m app.seed."""

from decimal import Decimal
from datetime import datetime, time, timedelta

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.config import DATABASE_URL
from app.database.base import Base
from app.database.sessions import create_database_engine
from app.models.hotel import Hotel, Room
from app.models.booking import TicketSession
from app.core.dates import ISLAND_TIMEZONE, island_today


def seed_demo_data(session: Session) -> bool:
    # Only seed an empty catalogue; never overwrite an existing hotel's data.
    if session.scalar(select(Hotel.id).limit(1)) is not None:
        return False

    hotel = Hotel(
        name="Demo Island Hotel", 
        description="Sample hotel for local testing.",
        location="Demo island",
    )
    session.add(hotel)
    session.flush()
    for name, category, price, guests, size, bed in [
        ("Deluxe Room", "beachfront", "780.00", 2, 95, "1 King Bed"),
        ("Garden Bungalow", "garden", "320.00", 2, 60, "1 Queen Bed"),
        ("Ocean Suite", "ocean_suite", "920.00", 3, 110, "1 King Bed and 1 Sofa Bed"),
        ("Family Villa", "family", "650.00", 4, 120, "2 Queen Beds"),
    ]:
        session.add(Room(
            hotel_id=hotel.id, name=name, description=f"Sample {name.lower()} for local testing.",
            category=category, price_per_night=Decimal(price), currency="USD",
            max_guests=guests, size_sqm=size, bed_type=bed, amenities=["WiFi"],
        ))
    session.commit()
    return True


def seed_ticket_sessions(session: Session) -> bool:
    if session.scalar(select(TicketSession.id).limit(1)) is not None:
        return False
    tomorrow = island_today() + timedelta(days=1)
    for kind, name, hour, capacity, price in [
        ("ferry", "Demo ferry: Harbour to Island", 9, 20, "15.00"),
        ("theme_park", "Demo theme-park admission", 10, 30, "28.00"),
    ]:
        start = datetime.combine(tomorrow, time(hour), tzinfo=ISLAND_TIMEZONE)
        session.add(TicketSession(
            kind=kind, name=name, description="Sample schedule and price for local testing only.",
            location="Demo island", starts_at=start, ends_at=start + timedelta(hours=1),
            capacity=capacity, price=Decimal(price), currency="USD",
        ))
    session.commit()
    return True


def main():
    engine = create_database_engine(DATABASE_URL)
    try:
        Base.metadata.create_all(engine)
        with Session(engine) as session:
            added = seed_demo_data(session)
            if added:
                print("Added one demo hotel and four demo rooms.")
            else:
                print("Catalogue already has data; nothing changed.")
            if seed_ticket_sessions(session):
                print("Added two demo ticket sessions for tomorrow.")
            else:
                print("Ticket sessions already exist; nothing changed.")
    finally:
        engine.dispose()


if __name__ == "__main__":
    main()
