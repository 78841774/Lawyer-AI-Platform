from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from app.core.database import Base


class CaseSkillBinding(Base):
    __tablename__ = "case_skill_bindings"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    binding_id: Mapped[str] = mapped_column(String(64), unique=True, index=True)
    case_id: Mapped[str] = mapped_column(
        String(64),
        ForeignKey("cases.case_id", ondelete="CASCADE"),
        index=True
    )
    skill_id: Mapped[str] = mapped_column(
        String(64),
        ForeignKey("skills.skill_id", ondelete="CASCADE"),
        index=True
    )
    package_id: Mapped[str] = mapped_column(
        String(64),
        ForeignKey("experience_packages.package_id", ondelete="CASCADE"),
        index=True
    )
    status: Mapped[str] = mapped_column(String(40), default="applied")
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

