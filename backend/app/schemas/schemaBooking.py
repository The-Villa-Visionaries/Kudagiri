from datetime import date, datetime
from decimal import Decimal
from typing import Annotated, Literal
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field, model_validator

from app.core.dates import validate_stay

TicketKind = Literal["ferry", "theme_park"]
BookingStatus = Literal["confirmed", "cancelled"]
RecordId = Annotated[int, Field(strict=True, gt=0, le=2**63 - 1)]


class BookingCreate(BaseModel):
    model_config = ConfigDict(extra="forbid")

    room_id: RecordId
    check_in: date
    check_out: date
    guests: int = Field(strict=True, ge=1)

    @model_validator(mode="after")
    def check_dates(self):
        validate_stay(self.check_in, self.check_out)
        return self


class TicketCreate(BaseModel):
    model_config = ConfigDict(extra="forbid")

    session_id: RecordId
    quantity: int = Field(strict=True, ge=1, le=100)


class TicketValidation(BaseModel):
    model_config = ConfigDict(extra="forbid")

    ticket_code: UUID
    session_id: RecordId


class TicketRedemption(TicketValidation):
    quantity: int = Field(strict=True, ge=1, le=100)


class BookingRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    reference: str
    user_id: int
    room_id: int
    check_in: date
    check_out: date
    guests: int
    nights: int
    unit_price: Decimal
    total_price: Decimal
    currency: str
    status: BookingStatus
    created_at: datetime


class TicketSessionRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    kind: TicketKind
    name: str
    description: str
    location: str
    starts_at: datetime
    ends_at: datetime
    capacity: int
    remaining_capacity: int
    price: Decimal
    currency: str


class TicketRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    code: str
    user_id: int
    holder_name: str
    session_id: int
    quantity: int
    used_quantity: int
    remaining_uses: int
    unit_price: Decimal
    total_price: Decimal
    currency: str
    status: BookingStatus
    created_at: datetime
    session: TicketSessionRead


class BookingPage(BaseModel):
    items: list[BookingRead]
    total: int
    skip: int
    limit: int


class TicketPage(BaseModel):
    items: list[TicketRead]
    total: int
    skip: int
    limit: int


class TicketSessionPage(BaseModel):
    items: list[TicketSessionRead]
    total: int
    skip: int
    limit: int
