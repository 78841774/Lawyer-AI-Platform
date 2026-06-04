from datetime import datetime, timezone
from typing import Any, Literal

from pydantic import BaseModel, Field


def utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


class SourceRef(BaseModel):
    source_ref_id: str
    source_type: Literal["material", "ocr", "legal_search", "skill_runtime", "report", "mock"]
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
    provider_mode: str | None = None
    retrieved_at: str | None = None
    mock_only: bool = True


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
    citation_label: str | None = None
    mock_only: bool = True


class SourceTraceNode(BaseModel):
    node_id: str
    node_type: Literal["material", "ocr_result", "legal_search_hit", "fact", "analysis", "report_section", "citation"]
    label: str
    source_ref_id: str | None = None
    metadata: dict[str, Any] = Field(default_factory=dict)


class SourceTraceEdge(BaseModel):
    edge_id: str
    from_node_id: str
    to_node_id: str
    relation: Literal["derived_from", "cited_by", "supports", "referenced_in", "generated_from"]
    metadata: dict[str, Any] = Field(default_factory=dict)


class SourceTrace(BaseModel):
    trace_id: str
    report_id: str
    case_id: str | None = None
    nodes: list[SourceTraceNode]
    edges: list[SourceTraceEdge]
    warnings: list[str]
    created_at: str
    mock_only: bool = True


class CitationResolutionResult(BaseModel):
    citation_id: str
    resolved: bool
    source_ref: SourceRef | None = None
    warnings: list[str]
    mock_only: bool = True


def empty_report_trace() -> dict[str, Any]:
    return {
        "schema_version": "v3.8",
        "source_ref_types": ["material", "ocr", "legal_search", "skill_runtime", "report", "mock"],
        "ocr_adapter": "mock_only_not_connected",
        "legal_search_adapter": "mock_only_not_connected",
        "citation_persistence": "not_enabled",
        "source_trace": "mock_ready"
    }


def mock_source_refs() -> list[dict[str, Any]]:
    return [
        SourceRef(
            source_ref_id="source_ref_mock_material_001",
            source_type="material",
            source_id="material_demo_001",
            material_id="material_demo_001",
            filename="demo.pdf",
            relative_path="demo/demo.pdf",
            page_number=1,
            char_start=0,
            char_end=64,
            quote="Mock material source ref only. No real material content used.",
            provider="mock",
            provider_mode="mock",
            mock_only=True
        ).model_dump(),
        SourceRef(
            source_ref_id="source_ref_mock_ocr_001",
            source_type="ocr",
            source_id="ocr_result_demo_001",
            material_id="material_demo_001",
            filename="demo.pdf",
            relative_path="demo/demo.pdf",
            page_number=1,
            char_start=0,
            char_end=64,
            quote="Mock OCR source ref only. No real OCR provider used.",
            provider="mock_ocr",
            provider_mode="mock",
            mock_only=True
        ).model_dump(),
        SourceRef(
            source_ref_id="source_ref_mock_legal_search_001",
            source_type="legal_search",
            source_id="legal_search_hit_demo_001",
            citation="Mock Citation",
            quote="Mock legal search source ref only. No external legal database queried.",
            provider="mock_legal_search",
            provider_mode="mock",
            mock_only=True
        ).model_dump()
    ]


def mock_report_citations(report_id: str | None = None) -> list[dict[str, Any]]:
    return [
        ReportCitation(
            citation_id="citation_mock_001",
            report_id=report_id,
            section_id="report_section_demo_001",
            source_ref_id="source_ref_mock_material_001",
            citation_label="[Mock-1]",
            quote="Mock citation quote only. No real material content used.",
            explanation="Mock material citation prepared for source trace testing.",
            confidence=0.0,
            created_at=utc_now(),
            mock_only=True
        ).model_dump(),
        ReportCitation(
            citation_id="citation_mock_002",
            report_id=report_id,
            section_id="report_section_demo_001",
            source_ref_id="source_ref_mock_legal_search_001",
            citation_label="[Mock-2]",
            quote="Mock legal search citation only.",
            explanation="Mock legal search citation prepared for source trace testing.",
            confidence=0.0,
            created_at=utc_now(),
            mock_only=True
        ).model_dump()
    ]


def mock_citation_summary() -> dict[str, Any]:
    return {
        "total_source_refs": 3,
        "total_citations": 2,
        "has_material_refs": True,
        "has_ocr_refs": True,
        "has_legal_search_refs": True,
        "mock_only": True,
        "warnings": [
            "Mock citation summary only.",
            "No real material used.",
            "No real OCR provider connected.",
            "No external legal database queried.",
            "No LLM call performed."
        ]
    }
