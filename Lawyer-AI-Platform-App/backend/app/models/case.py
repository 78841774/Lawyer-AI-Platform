from datetime import datetime

from sqlalchemy import DateTime, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.core.database import Base


class Case(Base):
    __tablename__ = "cases"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    case_id: Mapped[str] = mapped_column(String(64), unique=True, index=True)
    title: Mapped[str] = mapped_column(String(255))
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    client_name: Mapped[str | None] = mapped_column(Text, nullable=True)
    counterparty_name: Mapped[str | None] = mapped_column(Text, nullable=True)
    opposing_party: Mapped[str | None] = mapped_column(Text, nullable=True)
    case_type: Mapped[str | None] = mapped_column(String(80), nullable=True, default="contract_dispute")
    contract_type: Mapped[str | None] = mapped_column(Text, nullable=True)
    dispute_amount: Mapped[str | None] = mapped_column(Text, nullable=True)
    status: Mapped[str] = mapped_column(String(40), default="draft")
    objective: Mapped[str | None] = mapped_column(Text, nullable=True)
    jurisdiction: Mapped[str | None] = mapped_column(Text, nullable=True)
    intake_notes: Mapped[str | None] = mapped_column(Text, nullable=True)
    priority: Mapped[str | None] = mapped_column(String(40), nullable=True)
    tags: Mapped[str | None] = mapped_column(Text, nullable=True)
    workspace_id: Mapped[str] = mapped_column(
        String(64),
        default="workspace_local_001",
        index=True
    )
    owner_user_id: Mapped[str] = mapped_column(
        String(64),
        default="user_local_001",
        index=True
    )
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow
    )
