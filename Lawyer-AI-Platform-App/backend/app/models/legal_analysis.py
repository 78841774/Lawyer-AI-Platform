from datetime import datetime

from sqlalchemy import DateTime, Float, ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.core.database import Base


class LegalAnalysis(Base):
    __tablename__ = "legal_analyses"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    analysis_id: Mapped[str] = mapped_column(String(64), unique=True, index=True)
    case_id: Mapped[str] = mapped_column(
        String(64),
        ForeignKey("cases.case_id", ondelete="CASCADE"),
        index=True
    )
    issues: Mapped[str] = mapped_column(Text)
    rules: Mapped[str] = mapped_column(Text)
    reasoning: Mapped[str] = mapped_column(Text)
    conclusion: Mapped[str] = mapped_column(Text)
    risk_level: Mapped[str] = mapped_column(String(40), default="medium")
    confidence: Mapped[float] = mapped_column(Float, default=0.75)
    status: Mapped[str] = mapped_column(String(40), default="completed")
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
