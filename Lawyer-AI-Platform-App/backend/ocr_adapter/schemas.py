from datetime import datetime, timezone
from typing import Any

from pydantic import BaseModel


def utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


class OCRRequest(BaseModel):
    material_id: str
    filename: str
    relative_path: str | None = None
    provider: str = "mock_ocr"
    mode: str = "mock"
    mock_only: bool = True


class OCRSourceRef(BaseModel):
    source_ref_id: str
    source_type: str = "ocr"
    material_id: str
    filename: str
    relative_path: str | None = None
    page_number: int
    char_start: int
    char_end: int
    bbox: dict[str, Any] | None = None
    quote: str
    provider: str = "mock_ocr"
    provider_mode: str = "mock"
    mock_only: bool = True


class OCRPageResult(BaseModel):
    page_number: int
    text: str
    confidence: float
    source_ref: OCRSourceRef


class OCRResult(BaseModel):
    ocr_run_id: str
    material_id: str
    filename: str
    relative_path: str | None = None
    provider: str
    provider_mode: str
    status: str
    text_available: bool
    pages: list[OCRPageResult]
    source_refs: list[OCRSourceRef]
    warnings: list[str]
    created_at: str


class OCRProviderStatus(BaseModel):
    provider: str
    connected: bool
    mock_only: bool
    supports_pdf: bool
    supports_images: bool
    notes: str
