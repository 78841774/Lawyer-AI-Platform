from typing import Any

from fastapi import APIRouter

from controlled_revision_workflow.audit import list_controlled_revision_audit_logs
from controlled_revision_workflow.revision_engine import (
    create_mock_revision_request,
    get_controlled_revision_status,
    load_controlled_revision,
)
from controlled_revision_workflow.schemas import ControlledRevisionRequest

router = APIRouter(prefix="/controlled-revision", tags=["controlled-revision"])


@router.get("/status")
def controlled_revision_status() -> dict[str, Any]:
    return get_controlled_revision_status()


@router.post("/request")
def controlled_revision_request(request: ControlledRevisionRequest) -> dict[str, Any]:
    return create_mock_revision_request(request)


@router.get("/audit-logs")
def controlled_revision_audit_logs() -> dict[str, Any]:
    return {"audit_logs": list_controlled_revision_audit_logs()}


@router.get("/{revision_id}")
def controlled_revision_record(revision_id: str) -> dict[str, Any]:
    return load_controlled_revision(revision_id)

