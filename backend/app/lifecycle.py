from pathlib import Path

from alembic import command
from alembic.config import Config
from sqlalchemy import create_engine, inspect

from app.config import settings
from app.database import Base


def _alembic_config() -> Config:
    project_root = Path(__file__).resolve().parents[1]
    config = Config(str(project_root / "alembic.ini"))
    config.set_main_option("script_location", str(project_root / "migrations"))
    config.set_main_option("sqlalchemy.url", settings.database_url)
    return config


def _connect_args() -> dict:
    if settings.database_url.startswith("sqlite"):
        return {"check_same_thread": False}
    return {}


def _should_stamp_existing_database() -> bool:
    engine = create_engine(settings.database_url, connect_args=_connect_args())
    try:
        with engine.connect() as connection:
            table_names = set(inspect(connection).get_table_names())
            has_alembic_table = "alembic_version" in table_names
            has_app_tables = bool(table_names.intersection(Base.metadata.tables.keys()))
            return has_app_tables and not has_alembic_table
    finally:
        engine.dispose()


def run_db_migrations() -> None:
    config = _alembic_config()
    if _should_stamp_existing_database():
        command.stamp(config, "head")
    command.upgrade(config, "head")
