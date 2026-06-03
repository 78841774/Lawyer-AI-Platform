from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.core.database import Base


class Material(Base):
    __tablename__ = "materials"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    material_id: Mapped[str] = mapped_column(String(64), unique=True, index=True)
    case_id: Mapped[str] = mapped_column(
        String(64),
        ForeignKey("cases.case_id", ondelete="CASCADE"),
        index=True
    )
    filename: Mapped[str] = mapped_column(String(255))
    original_filename: Mapped[str | None] = mapped_column(String(255), nullable=True)
    relative_path: Mapped[str | None] = mapped_column(Text, nullable=True)
    folder_path: Mapped[str | None] = mapped_column(Text, nullable=True, default="")
    file_ext: Mapped[str | None] = mapped_column(String(40), nullable=True)
    upload_batch_id: Mapped[str | None] = mapped_column(String(80), nullable=True, index=True)
    display_order: Mapped[int] = mapped_column(Integer, default=0)
    material_type: Mapped[str] = mapped_column(String(80), default="document")
    storage_path: Mapped[str] = mapped_column(Text)
    status: Mapped[str] = mapped_column(String(40), default="uploaded")
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
