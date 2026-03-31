from collections.abc import Generator

from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, Session, sessionmaker

from app.config import settings


def _is_sqlite() -> bool:
    return settings.database_url.startswith("sqlite")


def _is_postgres() -> bool:
    return settings.database_url.startswith("postgresql")


def _engine_connect_args() -> dict:
    if _is_sqlite():
        return {"check_same_thread": False}
    if _is_postgres() and settings.db_ssl_mode:
        return {"sslmode": settings.db_ssl_mode}
    return {}


def _engine_kwargs() -> dict:
    kwargs: dict = {
        "pool_pre_ping": True,
    }
    if not _is_sqlite():
        kwargs["pool_size"] = settings.db_pool_size
        kwargs["max_overflow"] = settings.db_max_overflow
    return kwargs


engine = create_engine(
    settings.database_url,
    connect_args=_engine_connect_args(),
    **_engine_kwargs(),
)

SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)


class Base(DeclarativeBase):
    pass


def get_db() -> Generator[Session, None, None]:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
