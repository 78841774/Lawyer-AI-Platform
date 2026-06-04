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
    if settings.app_env.lower().strip() != "local":
        return

    import_models()
    Base.metadata.create_all(bind=engine)
    _ensure_sqlite_skill_columns()
    _ensure_sqlite_case_columns()
    _ensure_sqlite_material_columns()
    _seed_local_demo_identity()


def import_models() -> None:
    from app.models import (  # noqa: F401
        auth_token,
        case,
        case_skill_binding,
        experience_package,
        fact,
        legal_analysis,
        material,
        report,
        runtime_run,
        skill,
        skill_registry,
        user,
        workspace
    )


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


def _ensure_sqlite_case_columns() -> None:
    if not settings.database_url.startswith("sqlite"):
        return

    required_columns = {
        "workspace_id": "VARCHAR(64) DEFAULT 'workspace_local_001'",
        "owner_user_id": "VARCHAR(64) DEFAULT 'user_local_001'",
        "description": "TEXT",
        "client_name": "TEXT",
        "counterparty_name": "TEXT",
        "opposing_party": "TEXT",
        "contract_type": "TEXT",
        "dispute_amount": "TEXT",
        "jurisdiction": "TEXT",
        "intake_notes": "TEXT",
        "priority": "VARCHAR(40)",
        "tags": "TEXT"
    }
    with engine.begin() as connection:
        existing_columns = {
            row[1]
            for row in connection.execute(text("PRAGMA table_info(cases)"))
        }
        for column_name, column_type in required_columns.items():
            if column_name not in existing_columns:
                connection.execute(
                    text(f"ALTER TABLE cases ADD COLUMN {column_name} {column_type}")
                )

        connection.execute(
            text(
                "UPDATE cases "
                "SET workspace_id = 'workspace_local_001' "
                "WHERE workspace_id IS NULL OR workspace_id = ''"
            )
        )
        connection.execute(
            text(
                "UPDATE cases "
                "SET owner_user_id = 'user_local_001' "
                "WHERE owner_user_id IS NULL OR owner_user_id = ''"
            )
        )


def _ensure_sqlite_material_columns() -> None:
    if not settings.database_url.startswith("sqlite"):
        return

    required_columns = {
        "original_filename": "VARCHAR(255)",
        "relative_path": "TEXT",
        "folder_path": "TEXT DEFAULT ''",
        "file_ext": "VARCHAR(40)",
        "upload_batch_id": "VARCHAR(80)",
        "display_order": "INTEGER DEFAULT 0"
    }
    with engine.begin() as connection:
        existing_columns = {
            row[1]
            for row in connection.execute(text("PRAGMA table_info(materials)"))
        }
        for column_name, column_type in required_columns.items():
            if column_name not in existing_columns:
                connection.execute(
                    text(f"ALTER TABLE materials ADD COLUMN {column_name} {column_type}")
                )

        connection.execute(
            text(
                "UPDATE materials "
                "SET original_filename = filename "
                "WHERE original_filename IS NULL OR original_filename = ''"
            )
        )
        connection.execute(
            text(
                "UPDATE materials "
                "SET relative_path = filename "
                "WHERE relative_path IS NULL OR relative_path = ''"
            )
        )
        connection.execute(
            text(
                "UPDATE materials "
                "SET folder_path = '' "
                "WHERE folder_path IS NULL"
            )
        )
        connection.execute(
            text(
                "UPDATE materials "
                "SET display_order = 0 "
                "WHERE display_order IS NULL"
            )
        )


def _seed_local_demo_identity() -> None:
    from app.repositories.identity_repository import IdentityRepository
    from app.services.identity_service import ensure_local_demo_identity

    db = SessionLocal()
    try:
        ensure_local_demo_identity(IdentityRepository(db))
        db.commit()
    finally:
        db.close()


def get_db() -> Generator[Session, None, None]:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
