from decimal import Decimal
from sqlalchemy import CheckConstraint, ForeignKey, JSON, Numeric, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.database.base import Base

class Hotel(Base):
    __tablename__ = "hotels"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(150))
    description: Mapped[str] = mapped_column(Text, default="")
    location: Mapped[str] = mapped_column(String(200))
    rooms: Mapped[list["Room"]] = relationship(back_populates="hotel")

class Room(Base):
    __tablename__ = "rooms"
    __table_args__ = (
        CheckConstraint("price_per_night >= 0", name="room_price_nonnegative"),
        CheckConstraint("max_guests > 0", name="room_guests_positive"),
        CheckConstraint("size_sqm > 0", name="room_size_positive"),
        CheckConstraint(
            "category IN ('beachfront', 'ocean_suite', 'garden', 'family')",
            name="room_category_valid",
        ),
    )

    id: Mapped[int] = mapped_column(primary_key=True)
    hotel_id: Mapped[int] = mapped_column(ForeignKey("hotels.id"), index=True)
    name: Mapped[str] = mapped_column(String(150))
    description: Mapped[str] = mapped_column(Text, default="")
    category: Mapped[str] = mapped_column(String(30), index=True)
    price_per_night: Mapped[Decimal] = mapped_column(Numeric(10, 2))
    currency: Mapped[str] = mapped_column(String(3), default="USD")
    max_guests: Mapped[int]
    size_sqm: Mapped[int]
    bed_type: Mapped[str] = mapped_column(String(100))
    amenities: Mapped[list[str]] = mapped_column(JSON, default=list)
    image_url: Mapped[str | None] = mapped_column(Text, nullable=True)
    hotel: Mapped[Hotel] = relationship(back_populates="rooms")
