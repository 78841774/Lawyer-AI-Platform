from collections.abc import Generator

from sqlalchemy import create_engine, text
from sqlalchemy.orm import DeclarativeBase, Session, sessionmaker

from app.core.config import settings


class Base(DeclarativeBase):
    pass


connect_args = {}
if settings.database_url.startswith("sqlite"):
    connect_args["check_same_thread"] = False

engine = create_engine(settings.database_url, connect_args=connect_args)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def create_db_and_tables() -> None:
    from app.models import case, fact, legal_analysis, material, report, skill  # noqa: F401

    Base.metadata.create_all(bind=engine)
    _ensure_sqlite_skill_columns()


def _ensure_sqlite_skill_columns() -> None:
    if not settings.database_url.startswith("sqlite"):
        return

    required_columns = {
        "evaluation_details": "TEXT DEFAULT '{}'",
        "validation_status": "VARCHAR(40) DEFAULT 'candidate'",
        "validated_at": "DATETIME"
    }
    with engine.begin() as connection:
        existing_columns = {
            row[1]
            for row in connection.execute(text("PRAGMA table_info(skills)"))
        }
        for column_name, column_type in required_columns.items():
            if column_name not in existing_columns:
                connection.execute(
                    text(f"ALTER TABLE skills ADD COLUMN {column_name} {column_type}")
                )


def get_db() -> Generator[Session, None, None]:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
