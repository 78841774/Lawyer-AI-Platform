from datetime import datetime

from sqlalchemy import DateTime, Float, ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.core.database import Base


class Fact(Base):
    __tablename__ = "facts"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    fact_id: Mapped[str] = mapped_column(String(64), unique=True, index=True)
    case_id: Mapped[str] = mapped_column(
        String(64),
        ForeignKey("cases.case_id", ondelete="CASCADE"),
        index=True
    )
    material_id: Mapped[str] = mapped_column(
        String(64),
        ForeignKey("materials.material_id", ondelete="CASCADE"),
        index=True
    )
    content: Mapped[str] = mapped_column(Text)
    fact_type: Mapped[str] = mapped_column(String(80), default="material_statement")
    confidence: Mapped[float] = mapped_column(Float, default=0.8)
    source_text: Mapped[str | None] = mapped_column(Text, nullable=True)
    status: Mapped[str] = mapped_column(String(40), default="extracted")
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
