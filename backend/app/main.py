from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import Engine

from app.api.router import api_router
from app.core.config import CORS_ORIGINS, DATABASE_URL
from app.database.base import Base
from app.database.sessions import create_database_engine


def create_app(db_engine: Engine | None = None) -> FastAPI:
    @asynccontextmanager
    async def lifespan(app: FastAPI):
        engine = db_engine if db_engine is not None else create_database_engine(DATABASE_URL)
        app.state.db_engine = engine
        try:
            Base.metadata.create_all(engine)
            yield
        finally:
            if db_engine is None:
                engine.dispose()

    app = FastAPI(title="Kudagiri API", version="0.1.0", lifespan=lifespan)
    app.add_middleware(
        CORSMiddleware,
        allow_origins=CORS_ORIGINS,
        allow_methods=["GET"],
        allow_headers=["Content-Type", "Authorization"],
    )
    app.include_router(api_router)

    @app.get("/health", tags=["Health"])
    def health():
        return {"status": "ok"}

    return app


app = create_app()
