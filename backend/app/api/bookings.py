from datetime import date
from typing import Annotated

from fastapi import APIRouter, Depends, Path, Query, Response
from sqlalchemy import select

from app.api.auth import CurrentUser, Database
from app.models.booking import TicketStaff
from app.schemas.schemaBooking import (
    BookingCreate, BookingPage, BookingRead, BookingStatus, TicketCreate, TicketKind,
    TicketPage, TicketRead, TicketRedemption, TicketSessionPage, TicketSessionRead,
    TicketValidation,
)
from app.services import serviceBookings


def disable_cache(response: Response):
    response.headers["Cache-Control"] = "no-store"


router = APIRouter(tags=["Bookings and tickets"], dependencies=[Depends(disable_cache)])
PositiveId = Annotated[int, Path(gt=0, le=2**63 - 1)]
Skip = Annotated[int, Query(ge=0)]
Limit = Annotated[int, Query(ge=1, le=100)]
PRIVATE_ERRORS = {
    401: {"description": "Authentication required"},
    404: {"description": "Record not found"},
    409: {"description": "Reservation conflicts with availability or its current status"},
}
STAFF_ERRORS = {**PRIVATE_ERRORS, 403: {"description": "Ticket staff permission required"}}


@router.post("/bookings", response_model=BookingRead, status_code=201, responses=PRIVATE_ERRORS)
def create_booking(data: BookingCreate, user: CurrentUser, database: Database):
    return serviceBookings.create_booking(database, user.id, data)


@router.get("/bookings", response_model=BookingPage, responses=PRIVATE_ERRORS)
def list_bookings(
    user: CurrentUser, database: Database, skip: Skip = 0, limit: Limit = 20,
    status: BookingStatus | None = None,
):
    return serviceBookings.list_bookings(database, user.id, skip, limit, status)


@router.get("/bookings/{booking_id}", response_model=BookingRead, responses=PRIVATE_ERRORS)
def get_booking(booking_id: PositiveId, user: CurrentUser, database: Database):
    return serviceBookings.get_booking(database, user.id, booking_id)


@router.post("/bookings/{booking_id}/cancel", response_model=BookingRead, responses=PRIVATE_ERRORS)
def cancel_booking(booking_id: PositiveId, user: CurrentUser, database: Database):
    return serviceBookings.cancel_booking(database, user.id, booking_id)


@router.get("/ticket-sessions", response_model=TicketSessionPage)
def list_ticket_sessions(
    database: Database, skip: Skip = 0, limit: Limit = 20,
    kind: TicketKind | None = None, session_date: date | None = None,
):
    return serviceBookings.list_ticket_sessions(database, skip, limit, kind, session_date)


@router.get("/ticket-sessions/{session_id}", response_model=TicketSessionRead, responses={404: {"description": "Session not found"}})
def get_ticket_session(session_id: PositiveId, database: Database):
    return serviceBookings.get_ticket_session(database, session_id)


@router.post("/tickets", response_model=TicketRead, status_code=201, responses=PRIVATE_ERRORS)
def create_ticket(data: TicketCreate, user: CurrentUser, database: Database):
    return serviceBookings.create_ticket(database, user.id, data)


@router.get("/tickets", response_model=TicketPage, responses=PRIVATE_ERRORS)
def list_tickets(
    user: CurrentUser, database: Database, skip: Skip = 0, limit: Limit = 20,
    status: BookingStatus | None = None,
):
    return serviceBookings.list_tickets(database, user.id, skip, limit, status)


@router.get("/tickets/staff-permissions", response_model=list[TicketKind])
def staff_permissions(user: CurrentUser, database: Database):
    return database.scalars(
        select(TicketStaff.kind).where(TicketStaff.user_id == user.id).order_by(TicketStaff.kind)
    ).all()


@router.post("/tickets/validate", response_model=TicketRead, responses=STAFF_ERRORS)
def validate_ticket(data: TicketValidation, user: CurrentUser, database: Database):
    return serviceBookings.validate_ticket(database, user.id, data)


@router.post("/tickets/redeem", response_model=TicketRead, responses=STAFF_ERRORS)
def redeem_ticket(data: TicketRedemption, user: CurrentUser, database: Database):
    return serviceBookings.redeem_ticket(database, user.id, data)


@router.get("/tickets/{ticket_id}", response_model=TicketRead, responses=PRIVATE_ERRORS)
def get_ticket(ticket_id: PositiveId, user: CurrentUser, database: Database):
    return serviceBookings.get_ticket(database, user.id, ticket_id)


@router.post("/tickets/{ticket_id}/cancel", response_model=TicketRead, responses=PRIVATE_ERRORS)
def cancel_ticket(ticket_id: PositiveId, user: CurrentUser, database: Database):
    return serviceBookings.cancel_ticket(database, user.id, ticket_id)
