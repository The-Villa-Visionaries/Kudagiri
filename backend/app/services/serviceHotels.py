from decimal import Decimal
from sqlalchemy import func, or_, select
from sqlalchemy.orm import Session
from app.models.hotel import Hotel, Room
from app.models.booking import RoomNight

def list_hotels(session: Session, *, skip: int, limit: int):
    total = session.scalar(select(func.count()).select_from(Hotel))
    hotels = session.scalars(select(Hotel).order_by(Hotel.id).offset(skip).limit(limit)).all()
    return {"items": hotels, "total": total, "skip": skip, "limit": limit}

def get_hotel(session: Session, hotel_id: int) -> Hotel | None:
    return session.get(Hotel, hotel_id)

def get_room(session: Session, room_id: int) -> Room | None:
    return session.get(Room, room_id)

def list_rooms(
    session: Session,
    *,
    hotel_id: int | None = None,
    q: str | None = None,
    category: str | None = None,
    guests: int | None = None,
    max_price: Decimal | None = None,
    sort: str = "name",
    skip: int = 0,
    limit: int = 20,
    check_in=None,
    check_out=None,
):
    query = select(Room)
    if hotel_id is not None:
        query = query.where(Room.hotel_id == hotel_id)
    if q:
        # Treat % and _ as search text, rather than SQL wildcard characters.
        query = query.where(or_(
            Room.name.icontains(q, autoescape=True),
            Room.description.icontains(q, autoescape=True),
        ))
    if category is not None:
        query = query.where(Room.category == category)
    if guests is not None:
        query = query.where(Room.max_guests >= guests)
    if max_price is not None:
        query = query.where(Room.price_per_night <= max_price)
    if check_in is not None and check_out is not None:
        reserved = select(RoomNight.room_id).where(
            RoomNight.room_id == Room.id,
            RoomNight.stay_date >= check_in,
            RoomNight.stay_date < check_out,
        ).exists()
        query = query.where(~reserved)

    total = session.scalar(select(func.count()).select_from(query.subquery()))
    ordering = {
        "name": Room.name.asc(),
        "price_asc": Room.price_per_night.asc(),
        "price_desc": Room.price_per_night.desc(),
    }
    rooms = session.scalars(
        query.order_by(ordering[sort], Room.id).offset(skip).limit(limit)
    ).all()
    return {"items": rooms, "total": total, "skip": skip, "limit": limit}
