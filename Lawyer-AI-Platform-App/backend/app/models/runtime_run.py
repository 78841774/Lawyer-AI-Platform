from datetime import datetime

from sqlalchemy import Boolean, DateTime, ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.core.database import Base


class ExtractionRun(Base):
    __tablename__ = "extraction_runs"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    run_id: Mapped[str] = mapped_column(String(80), unique=True, index=True)
    case_id: Mapped[str] = mapped_column(
        String(64),
        ForeignKey("cases.case_id", ondelete="CASCADE"),
        index=True
    )
    workspace_id: Mapped[str | None] = mapped_column(String(64), nullable=True)
    triggered_by_user_id: Mapped[str | None] = mapped_column(String(64), nullable=True)
    status: Mapped[str] = mapped_column(String(40), default="completed")
    llm_provider: Mapped[str | None] = mapped_column(String(80), nullable=True)
    llm_status: Mapped[str | None] = mapped_column(String(80), nullable=True)
    skill_id: Mapped[str | None] = mapped_column(String(64), nullable=True)
    package_id: Mapped[str | None] = mapped_column(String(80), nullable=True)
    materials_count: Mapped[int] = mapped_column(Integer, default=0)
    facts_created_count: Mapped[int] = mapped_column(Integer, default=0)
    facts_reused_count: Mapped[int] = mapped_column(Integer, default=0)
    facts_skipped_count: Mapped[int] = mapped_column(Integer, default=0)
    source_material_ids: Mapped[str] = mapped_column(Text, default="[]")
    source_refs: Mapped[str] = mapped_column(Text, default="[]")
    error_message: Mapped[str | None] = mapped_column(Text, nullable=True)
    is_latest: Mapped[bool] = mapped_column(Boolean, default=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    completed_at: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)


class AnalysisRun(Base):
    __tablename__ = "analysis_runs"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    run_id: Mapped[str] = mapped_column(String(80), unique=True, index=True)
    case_id: Mapped[str] = mapped_column(
        String(64),
        ForeignKey("cases.case_id", ondelete="CASCADE"),
        index=True
    )
    workspace_id: Mapped[str | None] = mapped_column(String(64), nullable=True)
    triggered_by_user_id: Mapped[str | None] = mapped_column(String(64), nullable=True)
    status: Mapped[str] = mapped_column(String(40), default="completed")
    llm_provider: Mapped[str | None] = mapped_column(String(80), nullable=True)
    llm_status: Mapped[str | None] = mapped_column(String(80), nullable=True)
    skill_id: Mapped[str | None] = mapped_column(String(64), nullable=True)
    package_id: Mapped[str | None] = mapped_column(String(80), nullable=True)
    facts_count: Mapped[int] = mapped_column(Integer, default=0)
    analysis_id: Mapped[str | None] = mapped_column(String(64), nullable=True)
    source_fact_ids: Mapped[str] = mapped_column(Text, default="[]")
    source_refs: Mapped[str] = mapped_column(Text, default="[]")
    error_message: Mapped[str | None] = mapped_column(Text, nullable=True)
    is_latest: Mapped[bool] = mapped_column(Boolean, default=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    completed_at: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)


class ReportRun(Base):
    __tablename__ = "report_runs"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    run_id: Mapped[str] = mapped_column(String(80), unique=True, index=True)
    case_id: Mapped[str] = mapped_column(
        String(64),
        ForeignKey("cases.case_id", ondelete="CASCADE"),
        index=True
    )
    workspace_id: Mapped[str | None] = mapped_column(String(64), nullable=True)
    triggered_by_user_id: Mapped[str | None] = mapped_column(String(64), nullable=True)
    status: Mapped[str] = mapped_column(String(40), default="completed")
    llm_provider: Mapped[str | None] = mapped_column(String(80), nullable=True)
    llm_status: Mapped[str | None] = mapped_column(String(80), nullable=True)
    skill_id: Mapped[str | None] = mapped_column(String(64), nullable=True)
    package_id: Mapped[str | None] = mapped_column(String(80), nullable=True)
    analysis_id: Mapped[str | None] = mapped_column(String(64), nullable=True)
    report_id: Mapped[str | None] = mapped_column(String(64), nullable=True)
    source_refs: Mapped[str] = mapped_column(Text, default="[]")
    error_message: Mapped[str | None] = mapped_column(Text, nullable=True)
    is_latest: Mapped[bool] = mapped_column(Boolean, default=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    completed_at: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
