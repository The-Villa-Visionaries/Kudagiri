from datetime import date, datetime
from decimal import Decimal
from uuid import uuid4

from sqlalchemy import CheckConstraint, ForeignKey, Numeric, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.dates import utc_now
from app.database.base import Base
from app.database.types import UTCDateTime
from app.models.user import User


class Booking(Base):
    __tablename__ = "bookings"
    __table_args__ = (
        CheckConstraint("check_out > check_in", name="booking_dates_valid"),
        CheckConstraint("guests > 0", name="booking_guests_positive"),
        CheckConstraint("unit_price >= 0 AND total_price >= 0", name="booking_price_valid"),
        CheckConstraint("status IN ('confirmed', 'cancelled')", name="booking_status_valid"),
        {"sqlite_autoincrement": True},
    )

    id: Mapped[int] = mapped_column(primary_key=True)
    reference: Mapped[str] = mapped_column(String(36), unique=True, default=lambda: str(uuid4()))
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), index=True)
    room_id: Mapped[int] = mapped_column(ForeignKey("rooms.id"), index=True)
    check_in: Mapped[date]
    check_out: Mapped[date]
    guests: Mapped[int]
    unit_price: Mapped[Decimal] = mapped_column(Numeric(10, 2))
    total_price: Mapped[Decimal] = mapped_column(Numeric(14, 2))
    currency: Mapped[str] = mapped_column(String(3))
    status: Mapped[str] = mapped_column(String(20), default="confirmed")
    created_at: Mapped[datetime] = mapped_column(UTCDateTime(), default=utc_now)
    owner: Mapped[User] = relationship()

    @property
    def nights(self) -> int:
        return (self.check_out - self.check_in).days


class RoomNight(Base):
    __tablename__ = "room_nights"

    # The primary key prevents two transactions reserving the same room/night.
    room_id: Mapped[int] = mapped_column(ForeignKey("rooms.id"), primary_key=True)
    stay_date: Mapped[date] = mapped_column(primary_key=True)
    booking_id: Mapped[int] = mapped_column(ForeignKey("bookings.id"), index=True)


class TicketSession(Base):
    __tablename__ = "ticket_sessions"
    __table_args__ = (
        CheckConstraint("kind IN ('ferry', 'theme_park')", name="session_kind_valid"),
        CheckConstraint("capacity > 0", name="session_capacity_positive"),
        CheckConstraint("reserved_quantity >= 0 AND reserved_quantity <= capacity", name="session_capacity_valid"),
        CheckConstraint("price >= 0", name="session_price_valid"),
        CheckConstraint("ends_at > starts_at", name="session_times_valid"),
    )

    id: Mapped[int] = mapped_column(primary_key=True)
    kind: Mapped[str] = mapped_column(String(20), index=True)
    name: Mapped[str] = mapped_column(String(150))
    description: Mapped[str] = mapped_column(Text, default="")
    location: Mapped[str] = mapped_column(String(200))
    starts_at: Mapped[datetime] = mapped_column(UTCDateTime(), index=True)
    ends_at: Mapped[datetime] = mapped_column(UTCDateTime())
    capacity: Mapped[int]
    reserved_quantity: Mapped[int] = mapped_column(default=0)
    price: Mapped[Decimal] = mapped_column(Numeric(10, 2))
    currency: Mapped[str] = mapped_column(String(3), default="USD")

    @property
    def remaining_capacity(self) -> int:
        return self.capacity - self.reserved_quantity


class Ticket(Base):
    __tablename__ = "tickets"
    __table_args__ = (
        CheckConstraint("quantity > 0", name="ticket_quantity_positive"),
        CheckConstraint("used_quantity >= 0 AND used_quantity <= quantity", name="ticket_usage_valid"),
        CheckConstraint("unit_price >= 0 AND total_price >= 0", name="ticket_price_valid"),
        CheckConstraint("status IN ('confirmed', 'cancelled')", name="ticket_status_valid"),
        {"sqlite_autoincrement": True},
    )

    id: Mapped[int] = mapped_column(primary_key=True)
    code: Mapped[str] = mapped_column(String(36), unique=True, default=lambda: str(uuid4()))
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), index=True)
    session_id: Mapped[int] = mapped_column(ForeignKey("ticket_sessions.id"), index=True)
    quantity: Mapped[int]
    used_quantity: Mapped[int] = mapped_column(default=0)
    unit_price: Mapped[Decimal] = mapped_column(Numeric(10, 2))
    total_price: Mapped[Decimal] = mapped_column(Numeric(14, 2))
    currency: Mapped[str] = mapped_column(String(3))
    status: Mapped[str] = mapped_column(String(20), default="confirmed")
    created_at: Mapped[datetime] = mapped_column(UTCDateTime(), default=utc_now)
    session: Mapped[TicketSession] = relationship(lazy="selectin")
    owner: Mapped[User] = relationship()

    @property
    def remaining_uses(self) -> int:
        return self.quantity - self.used_quantity if self.status == "confirmed" else 0

    @property
    def holder_name(self) -> str:
        return self.owner.full_name


class TicketStaff(Base):
    __tablename__ = "ticket_staff"
    __table_args__ = (
        CheckConstraint("kind IN ('ferry', 'theme_park')", name="staff_kind_valid"),
    )

    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), primary_key=True)
    kind: Mapped[str] = mapped_column(String(20), primary_key=True)
