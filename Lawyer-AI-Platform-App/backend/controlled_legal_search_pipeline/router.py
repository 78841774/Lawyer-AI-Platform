from typing import Any

from fastapi import APIRouter

from controlled_legal_search_pipeline.audit import list_controlled_legal_search_audit_logs
from controlled_legal_search_pipeline.mock_legal_search import (
    get_controlled_legal_search_preview,
    get_controlled_legal_search_status,
    resolve_mock_citation,
    run_mock_legal_search_preview,
)
from controlled_legal_search_pipeline.schemas import ControlledLegalCitationResolutionRequest, ControlledLegalSearchPreviewRequest

router = APIRouter(prefix="/controlled-legal-search", tags=["controlled-legal-search"])


@router.get("/status")
def controlled_legal_search_status() -> dict[str, Any]:
    return get_controlled_legal_search_status()


@router.post("/preview")
def controlled_legal_search_preview(request: ControlledLegalSearchPreviewRequest) -> dict[str, Any]:
    return run_mock_legal_search_preview(request)


@router.get("/preview/{search_preview_id}")
def controlled_legal_search_preview_record(search_preview_id: str) -> dict[str, Any]:
    return get_controlled_legal_search_preview(search_preview_id)


@router.post("/resolve-citation")
def controlled_legal_search_resolve_citation(request: ControlledLegalCitationResolutionRequest) -> dict[str, Any]:
    return resolve_mock_citation(request)


@router.get("/audit-logs")
def controlled_legal_search_audit_logs() -> dict[str, Any]:
    return {"audit_logs": list_controlled_legal_search_audit_logs()}
