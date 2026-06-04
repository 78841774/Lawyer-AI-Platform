from typing import Any

from fastapi import APIRouter

from source_refs.citation_resolver import resolve_mock_citation
from source_refs.trace_builder import build_mock_source_trace

router = APIRouter(prefix="/source-refs", tags=["source-refs"])


@router.get("/status")
def get_source_refs_status() -> dict[str, Any]:
    return {
        "source_refs_enabled": True,
        "citation_resolver_enabled": True,
        "source_trace_enabled": True,
        "mock_only": True,
        "real_material_reading_enabled": False,
        "real_ocr_connected": False,
        "real_legal_search_connected": False,
        "notes": "Source refs and citation trace foundation prepared in mock mode."
    }


@router.get("/mock-trace/{report_id}")
def get_mock_source_trace(report_id: str, case_id: str | None = None) -> dict[str, Any]:
    return build_mock_source_trace(report_id=report_id, case_id=case_id)


@router.get("/resolve/{citation_id}")
def resolve_citation(citation_id: str) -> dict[str, Any]:
    return resolve_mock_citation(citation_id)
