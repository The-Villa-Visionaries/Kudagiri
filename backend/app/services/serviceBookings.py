from contextlib import contextmanager
from datetime import datetime, time, timedelta
from decimal import Decimal

from sqlalchemy import delete, func, select, update
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.core.dates import ISLAND_TIMEZONE, island_today, utc_now
from app.models.booking import Booking, RoomNight, Ticket, TicketSession, TicketStaff
from app.models.hotel import Room
from app.schemas.schemaBooking import BookingCreate, TicketCreate, TicketRedemption, TicketValidation


class BookingError(Exception):
    def __init__(self, status_code: int, detail: str):
        self.status_code = status_code
        self.detail = detail
        super().__init__(detail)


@contextmanager
def transaction(session: Session):
    try:
        yield
        session.commit()
    except Exception:
        session.rollback()
        raise


def page(session, query, skip, limit):
    total = session.scalar(select(func.count()).select_from(query.order_by(None).subquery()))
    items = session.scalars(query.offset(skip).limit(limit)).all()
    return {"items": items, "total": total, "skip": skip, "limit": limit}


def get_booking(session: Session, user_id: int, booking_id: int) -> Booking:
    booking = session.scalar(select(Booking).where(Booking.id == booking_id, Booking.user_id == user_id))
    if booking is None:
        raise BookingError(404, "Booking not found")
    return booking


def list_bookings(session, user_id, skip, limit, status=None):
    query = select(Booking).where(Booking.user_id == user_id).order_by(Booking.id.desc())
    if status is not None:
        query = query.where(Booking.status == status)
    return page(session, query, skip, limit)


def create_booking(session: Session, user_id: int, data: BookingCreate) -> Booking:
    room = session.get(Room, data.room_id)
    if room is None:
        raise BookingError(404, "Room not found")
    if data.guests > room.max_guests:
        raise BookingError(422, "Guest count exceeds room capacity")
    nights = (data.check_out - data.check_in).days
    booking = Booking(
        user_id=user_id, room_id=room.id, check_in=data.check_in, check_out=data.check_out,
        guests=data.guests, unit_price=room.price_per_night,
        total_price=(room.price_per_night * nights).quantize(Decimal("0.01")),
        currency=room.currency,
    )
    with transaction(session):
        session.add(booking)
        session.flush()
        session.add_all([
            RoomNight(room_id=room.id, booking_id=booking.id, stay_date=data.check_in + timedelta(days=day))
            for day in range(nights)
        ])
        try:
            session.flush()
        except IntegrityError:
            # A single conflicting night rolls back the whole reservation.
            raise BookingError(409, "Room is already reserved for these dates") from None
    session.refresh(booking)
    return booking


def cancel_booking(session: Session, user_id: int, booking_id: int) -> Booking:
    booking = get_booking(session, user_id, booking_id)
    if booking.status == "cancelled":
        return booking
    if booking.check_in <= island_today():
        raise BookingError(409, "Booking can only be cancelled before its check-in date")
    with transaction(session):
        changed = session.execute(
            update(Booking).where(
                Booking.id == booking_id, Booking.user_id == user_id,
                Booking.status == "confirmed", Booking.check_in > island_today(),
            ).values(status="cancelled").execution_options(synchronize_session=False)
        ).rowcount
        if changed:
            session.execute(delete(RoomNight).where(RoomNight.booking_id == booking_id))
    session.refresh(booking)
    if booking.status != "cancelled":
        raise BookingError(409, "Booking can no longer be cancelled")
    return booking


def get_ticket_session(session: Session, session_id: int) -> TicketSession:
    slot = session.get(TicketSession, session_id)
    if slot is None:
        raise BookingError(404, "Ticket session not found")
    return slot


def list_ticket_sessions(session, skip, limit, kind=None, session_date=None):
    query = select(TicketSession).where(TicketSession.ends_at > utc_now())
    if kind is not None:
        query = query.where(TicketSession.kind == kind)
    if session_date is not None:
        start = datetime.combine(session_date, time.min, tzinfo=ISLAND_TIMEZONE)
        query = query.where(TicketSession.starts_at >= start, TicketSession.starts_at < start + timedelta(days=1))
    return page(session, query.order_by(TicketSession.starts_at, TicketSession.id), skip, limit)


def get_ticket(session: Session, user_id: int, ticket_id: int) -> Ticket:
    ticket = session.scalar(select(Ticket).where(Ticket.id == ticket_id, Ticket.user_id == user_id))
    if ticket is None:
        raise BookingError(404, "Ticket not found")
    return ticket


def list_tickets(session, user_id, skip, limit, status=None):
    query = select(Ticket).where(Ticket.user_id == user_id).order_by(Ticket.id.desc())
    if status is not None:
        query = query.where(Ticket.status == status)
    return page(session, query, skip, limit)


def create_ticket(session: Session, user_id: int, data: TicketCreate) -> Ticket:
    slot = get_ticket_session(session, data.session_id)
    if slot.starts_at <= utc_now():
        raise BookingError(409, "This session has already started")
    ticket = Ticket(
        user_id=user_id, session_id=slot.id, quantity=data.quantity,
        unit_price=slot.price, total_price=(slot.price * data.quantity).quantize(Decimal("0.01")),
        currency=slot.currency,
    )
    with transaction(session):
        # Check and increment together; concurrent requests cannot oversell.
        changed = session.execute(
            update(TicketSession).where(
                TicketSession.id == slot.id, TicketSession.starts_at > utc_now(),
                TicketSession.reserved_quantity + data.quantity <= TicketSession.capacity,
            ).values(reserved_quantity=TicketSession.reserved_quantity + data.quantity)
            .execution_options(synchronize_session=False)
        ).rowcount
        if not changed:
            raise BookingError(409, "Not enough tickets available or the session has started")
        session.add(ticket)
    session.refresh(ticket)
    return ticket


def cancel_ticket(session: Session, user_id: int, ticket_id: int) -> Ticket:
    ticket = get_ticket(session, user_id, ticket_id)
    if ticket.status == "cancelled":
        return ticket
    if ticket.used_quantity or ticket.session.starts_at <= utc_now():
        raise BookingError(409, "Only unused tickets for a future session can be cancelled")
    with transaction(session):
        changed = session.execute(
            update(Ticket).where(
                Ticket.id == ticket_id, Ticket.user_id == user_id,
                Ticket.status == "confirmed", Ticket.used_quantity == 0,
            ).values(status="cancelled").execution_options(synchronize_session=False)
        ).rowcount
        if changed:
            session.execute(
                update(TicketSession).where(TicketSession.id == ticket.session_id)
                .values(reserved_quantity=TicketSession.reserved_quantity - ticket.quantity)
                .execution_options(synchronize_session=False)
            )
    session.refresh(ticket)
    if ticket.status != "cancelled":
        raise BookingError(409, "Ticket has already been used")
    return ticket


def validate_ticket(session: Session, staff_id: int, data: TicketValidation) -> Ticket:
    allowed_kinds = set(session.scalars(select(TicketStaff.kind).where(TicketStaff.user_id == staff_id)))
    if not allowed_kinds:
        raise BookingError(403, "Ticket staff permission required")
    ticket = session.scalar(select(Ticket).join(TicketSession).where(
        Ticket.code == str(data.ticket_code), Ticket.session_id == data.session_id,
        TicketSession.kind.in_(allowed_kinds),
    ))
    if ticket is None:
        raise BookingError(404, "Ticket not found for this session or staff permission")
    if ticket.status != "confirmed" or ticket.remaining_uses == 0:
        raise BookingError(409, "Ticket is cancelled or fully used")
    if ticket.session.starts_at.astimezone(ISLAND_TIMEZONE).date() != island_today():
        raise BookingError(409, "Ticket can only be used on its session date")
    if ticket.session.ends_at <= utc_now():
        raise BookingError(409, "Ticket session has ended")
    return ticket


def redeem_ticket(session: Session, staff_id: int, data: TicketRedemption) -> Ticket:
    ticket = validate_ticket(session, staff_id, data)
    with transaction(session):
        changed = session.execute(
            update(Ticket).where(
                Ticket.id == ticket.id, Ticket.status == "confirmed",
                Ticket.used_quantity + data.quantity <= Ticket.quantity,
            ).values(used_quantity=Ticket.used_quantity + data.quantity)
            .execution_options(synchronize_session=False)
        ).rowcount
        if not changed:
            raise BookingError(409, "Ticket has insufficient unused entries or is cancelled")
    session.refresh(ticket)
    return ticket
