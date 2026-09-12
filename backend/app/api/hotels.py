from decimal import Decimal
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Path, Query, status
from sqlalchemy.orm import Session

from app.database.sessions import get_database
from app.schemas.schemaHotel import (
    HotelPage,
    HotelRead,
    RoomCategory,
    RoomPage,
    RoomRead,
    RoomSort,
)
from app.services import serviceHotels

router = APIRouter(tags=["Hotels and rooms"])
Database = Annotated[Session, Depends(get_database)]
PositiveId = Annotated[int, Path(gt=0)]
Skip = Annotated[int, Query(ge=0)]
Limit = Annotated[int, Query(ge=1, le=100)]


def room_filters(
    q: Annotated[
        str | None,
        Query(min_length=1, max_length=100, description="Search room name or description"),
    ] = None,
    category: RoomCategory | None = None,
    guests: Annotated[int | None, Query(ge=1)] = None,
    max_price: Annotated[
        Decimal | None,
        Query(ge=0, max_digits=10, decimal_places=2, description="Maximum nightly price in USD"),
    ] = None,
    sort: RoomSort = "name",
    skip: Skip = 0,
    limit: Limit = 20,
):
    return dict(
        q=q, category=category, guests=guests, max_price=max_price,
        sort=sort, skip=skip, limit=limit,
    )


Filters = Annotated[dict, Depends(room_filters)]


@router.get("/hotels", response_model=HotelPage)
def list_hotels(database: Database, skip: Skip = 0, limit: Limit = 20):
    return serviceHotels.list_hotels(database, skip=skip, limit=limit)


@router.get(
    "/hotels/{hotel_id}", response_model=HotelRead,
    responses={404: {"description": "Hotel not found"}},
)
def get_hotel(hotel_id: PositiveId, database: Database):
    hotel = serviceHotels.get_hotel(database, hotel_id)
    if hotel is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Hotel not found")
    return hotel


@router.get(
    "/hotels/{hotel_id}/rooms", response_model=RoomPage,
    responses={404: {"description": "Hotel not found"}},
)
def list_hotel_rooms(hotel_id: PositiveId, database: Database, filters: Filters):
    get_hotel(hotel_id, database)
    return serviceHotels.list_rooms(database, hotel_id=hotel_id, **filters)


@router.get("/rooms", response_model=RoomPage)
def list_rooms(database: Database, filters: Filters):
    return serviceHotels.list_rooms(database, **filters)


@router.get(
    "/rooms/{room_id}", response_model=RoomRead,
    responses={404: {"description": "Room not found"}},
)
def get_room(room_id: PositiveId, database: Database):
    room = serviceHotels.get_room(database, room_id)
    if room is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Room not found")
    return room
