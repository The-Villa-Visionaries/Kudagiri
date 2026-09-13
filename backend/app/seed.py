"""Optional sample catalogue for local development: python -m app.seed."""

from decimal import Decimal

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.config import DATABASE_URL
from app.database.base import Base
from app.database.sessions import create_database_engine
from app.models.hotel import Hotel, Room


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
    finally:
        engine.dispose()


if __name__ == "__main__":
    main()
