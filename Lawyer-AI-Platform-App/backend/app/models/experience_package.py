from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.core.database import Base


class ExperiencePackage(Base):
    __tablename__ = "experience_packages"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    package_id: Mapped[str] = mapped_column(String(64), unique=True, index=True)
    skill_id: Mapped[str] = mapped_column(
        String(64),
        ForeignKey("skills.skill_id", ondelete="CASCADE"),
        index=True
    )
    name: Mapped[str] = mapped_column(String(255))
    domain: Mapped[str] = mapped_column(String(80), default="contract_dispute")
    version: Mapped[str] = mapped_column(String(40), default="0.1.0")
    status: Mapped[str] = mapped_column(String(40), default="built")
    manifest_json: Mapped[str] = mapped_column(Text, default="{}")
    package_path: Mapped[str] = mapped_column(Text)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

