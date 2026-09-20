from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from sqlalchemy import Engine
from app.api.router import api_router
from app.core.config import AuthSettings, CORS_ORIGINS, DATABASE_URL, load_auth_settings
from app.database.base import Base
from app.database.sessions import create_database_engine
from app.services.serviceBookings import BookingError

def create_app(db_engine: Engine | None = None, auth_settings: AuthSettings | None = None) -> FastAPI:
    @asynccontextmanager
    async def lifespan(app: FastAPI):
        app.state.auth_settings = auth_settings if auth_settings is not None else load_auth_settings()
        engine = db_engine if db_engine is not None else create_database_engine(DATABASE_URL)
        app.state.db_engine = engine
        try:
            Base.metadata.create_all(engine)
            yield
        finally:
            if db_engine is None:
                engine.dispose()

    app = FastAPI(title="Kudagiri API", version="0.3.0", lifespan=lifespan)
    app.add_middleware(
        CORSMiddleware,
        allow_origins=CORS_ORIGINS,
        allow_methods=["GET", "POST"],
        allow_headers=["Content-Type", "Authorization"],
    )
    app.include_router(api_router)

    @app.exception_handler(BookingError)
    async def booking_error_handler(request, exc):
        return JSONResponse(
            status_code=exc.status_code, content={"detail": exc.detail},
            headers={"Cache-Control": "no-store"},
        )

    @app.exception_handler(RequestValidationError)
    async def validation_error_handler(request, exc):
        # Validation errors must not echo submitted passwords or request bodies.
        errors = [
            {"type": error["type"], "loc": error["loc"], "msg": error["msg"]}
            for error in exc.errors()
        ]
        return JSONResponse(status_code=422, content={"detail": errors})

    @app.get("/health", tags=["Health"])
    def health():
        return {"status": "ok"}

    return app

app = create_app()
