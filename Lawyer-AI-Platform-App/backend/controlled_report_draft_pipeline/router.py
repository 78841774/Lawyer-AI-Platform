from typing import Any

from fastapi import APIRouter

from controlled_report_draft_pipeline.audit import list_controlled_report_draft_audit_logs
from controlled_report_draft_pipeline.mock_report_assembler import (
    assemble_mock_controlled_report,
    get_controlled_report_draft_status,
    load_mock_controlled_report,
)
from controlled_report_draft_pipeline.schemas import ControlledReportDraftAssembleRequest

router = APIRouter(prefix="/controlled-report-draft", tags=["controlled-report-draft"])


@router.get("/status")
def controlled_report_draft_status() -> dict[str, Any]:
    return get_controlled_report_draft_status()


@router.post("/assemble")
def controlled_report_draft_assemble(request: ControlledReportDraftAssembleRequest) -> dict[str, Any]:
    return assemble_mock_controlled_report(request)


@router.get("/audit-logs")
def controlled_report_draft_audit_logs() -> dict[str, Any]:
    return {"audit_logs": list_controlled_report_draft_audit_logs()}


@router.get("/{draft_id}")
def controlled_report_draft_record(draft_id: str) -> dict[str, Any]:
    return load_mock_controlled_report(draft_id)

