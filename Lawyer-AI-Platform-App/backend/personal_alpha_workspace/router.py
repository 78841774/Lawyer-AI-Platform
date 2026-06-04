from typing import Any

from fastapi import APIRouter

from personal_alpha_workspace.schemas import PersonalAlphaWorkspaceRequest
from personal_alpha_workspace.workspace_engine import (
    get_personal_alpha_workspace_status,
    list_personal_alpha_workspace_audit_logs,
    load_personal_alpha_workspace_run,
    run_personal_alpha_workspace,
)

router = APIRouter(prefix="/personal-alpha-workspace", tags=["personal-alpha-workspace"])


@router.get("/status")
def personal_alpha_workspace_status() -> dict[str, Any]:
    return get_personal_alpha_workspace_status()


@router.post("/run")
def personal_alpha_workspace_run(request: PersonalAlphaWorkspaceRequest) -> dict[str, Any]:
    return run_personal_alpha_workspace(request)


@router.get("/audit-logs")
def personal_alpha_workspace_audit_logs() -> dict[str, Any]:
    return list_personal_alpha_workspace_audit_logs()


@router.get("/{workspace_run_id}")
def personal_alpha_workspace_run_record(workspace_run_id: str) -> dict[str, Any]:
    return load_personal_alpha_workspace_run(workspace_run_id)
