from datetime import datetime, timezone
from typing import Any, Literal

from pydantic import BaseModel


def utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


class SourceRef(BaseModel):
    source_ref_id: str
    source_type: Literal["material", "ocr", "legal_search", "skill_runtime"]
    source_id: str | None = None
    material_id: str | None = None
    filename: str | None = None
    relative_path: str | None = None
    page_number: int | None = None
    char_start: int | None = None
    char_end: int | None = None
    bbox: dict[str, Any] | None = None
    quote: str | None = None
    citation: str | None = None
    url: str | None = None
    provider: str | None = None
    retrieved_at: str | None = None


class MaterialSourceRef(SourceRef):
    source_type: Literal["material"] = "material"


class OCRSourceRef(SourceRef):
    source_type: Literal["ocr"] = "ocr"


class LegalSearchSourceRef(SourceRef):
    source_type: Literal["legal_search"] = "legal_search"


class ReportCitation(BaseModel):
    citation_id: str
    report_id: str | None = None
    section_id: str | None = None
    source_ref_id: str
    quote: str | None = None
    explanation: str | None = None
    confidence: float = 0.0
    created_at: str


def empty_report_trace() -> dict[str, Any]:
    return {
        "schema_version": "v3.7",
        "source_ref_types": ["material", "ocr", "legal_search", "skill_runtime"],
        "ocr_adapter": "mock_only_not_connected",
        "legal_search_adapter": "mock_only_not_connected",
        "citation_persistence": "not_enabled"
    }
