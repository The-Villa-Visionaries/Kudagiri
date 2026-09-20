from fastapi import APIRouter
from app.api import auth, bookings, hotels

api_router = APIRouter(prefix="/api")
api_router.include_router(hotels.router)
api_router.include_router(auth.router)
api_router.include_router(bookings.router)
