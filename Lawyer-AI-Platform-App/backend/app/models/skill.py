from datetime import datetime

from sqlalchemy import DateTime, Float, ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.core.database import Base


class Skill(Base):
    __tablename__ = "skills"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    skill_id: Mapped[str] = mapped_column(String(64), unique=True, index=True)
    case_id: Mapped[str] = mapped_column(
        String(64),
        ForeignKey("cases.case_id", ondelete="CASCADE"),
        index=True
    )
    skill_name: Mapped[str] = mapped_column(String(255))
    domain: Mapped[str] = mapped_column(String(80), default="contract_dispute")
    version: Mapped[str] = mapped_column(String(40), default="0.1.0")
    status: Mapped[str] = mapped_column(String(40), default="candidate")
    fact_patterns: Mapped[str] = mapped_column(Text, default="[]")
    reasoning_patterns: Mapped[str] = mapped_column(Text, default="[]")
    prompts: Mapped[str] = mapped_column(Text, default="{}")
    templates: Mapped[str] = mapped_column(Text, default="{}")
    evaluation_score: Mapped[float] = mapped_column(Float, default=0.0)
    evaluation_details: Mapped[str] = mapped_column(Text, default="{}")
    validation_status: Mapped[str] = mapped_column(String(40), default="candidate")
    package_path: Mapped[str | None] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    validated_at: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
