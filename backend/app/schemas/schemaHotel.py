from decimal import Decimal
from typing import Literal
from pydantic import BaseModel, ConfigDict

RoomCategory = Literal["beachfront", "ocean_suite", "garden", "family"]
RoomSort = Literal["name", "price_asc", "price_desc"]

class HotelRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    description: str
    location: str

class RoomRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    hotel_id: int
    name: str
    description: str
    category: RoomCategory
    price_per_night: Decimal
    currency: str
    max_guests: int
    size_sqm: int
    bed_type: str
    amenities: list[str]
    image_url: str | None

class HotelPage(BaseModel):
    items: list[HotelRead]
    total: int
    skip: int
    limit: int

class RoomPage(BaseModel):
    items: list[RoomRead]
    total: int
    skip: int
    limit: int
