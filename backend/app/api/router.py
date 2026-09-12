from fastapi import APIRouter

from app.api import hotels

api_router = APIRouter(prefix="/api")
api_router.include_router(hotels.router)
