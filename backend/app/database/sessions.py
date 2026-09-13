from collections.abc import Generator
from fastapi import Request
from sqlalchemy import Engine, create_engine, event
from sqlalchemy.orm import Session

def create_database_engine(database_url: str) -> Engine:
    connect_args = {"check_same_thread": False} if database_url.startswith("sqlite:") else {}
    engine = create_engine(database_url, connect_args=connect_args)

    if engine.dialect.name == "sqlite":
        @event.listens_for(engine, "connect")
        def enable_foreign_keys(connection, _):
            cursor = connection.cursor()
            cursor.execute("PRAGMA foreign_keys=ON")
            cursor.close()

    return engine

def get_database(request: Request) -> Generator[Session, None, None]:
    with Session(request.app.state.db_engine) as session:
        yield session
