from typing import Any

from fastapi import APIRouter

from controlled_material_processing.audit import list_controlled_material_audit_logs
from controlled_material_processing.processor import (
    generate_controlled_report_draft,
    get_controlled_material_status,
    run_controlled_material_read,
)
from controlled_material_processing.schemas import ControlledMaterialReadRequest, ControlledReportDraftRequest

router = APIRouter(prefix="/controlled-material", tags=["controlled-material"])


@router.get("/status")
def controlled_material_status() -> dict[str, Any]:
    return get_controlled_material_status()


@router.post("/read-confirmed")
def controlled_material_read_confirmed(request: ControlledMaterialReadRequest) -> dict[str, Any]:
    return run_controlled_material_read(request)


@router.post("/report-draft")
def controlled_material_report_draft(request: ControlledReportDraftRequest) -> dict[str, Any]:
    return generate_controlled_report_draft(request)


@router.get("/audit-logs")
def controlled_material_audit_logs() -> dict[str, Any]:
    return {"audit_logs": list_controlled_material_audit_logs()}
