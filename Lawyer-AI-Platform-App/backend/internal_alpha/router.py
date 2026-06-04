from typing import Any

from fastapi import APIRouter

from internal_alpha.audit import list_internal_alpha_audit_logs
from internal_alpha.dry_run import run_internal_alpha_dry_run
from internal_alpha.readiness import (
    get_database_readiness_status,
    get_deployment_readiness_checklist,
    get_secret_management_checklist,
)
from internal_alpha.schemas import InternalAlphaDryRunRequest
from internal_alpha.status import get_internal_alpha_status

router = APIRouter(prefix="/internal-alpha", tags=["internal-alpha"])


@router.get("/status")
def internal_alpha_status() -> dict[str, Any]:
    return get_internal_alpha_status()


@router.get("/readiness")
def internal_alpha_readiness() -> dict[str, Any]:
    return get_deployment_readiness_checklist()


@router.get("/secrets")
def internal_alpha_secrets() -> dict[str, Any]:
    return get_secret_management_checklist()


@router.get("/database")
def internal_alpha_database() -> dict[str, Any]:
    return get_database_readiness_status()


@router.get("/audit-logs")
def internal_alpha_audit_logs() -> dict[str, Any]:
    return {"audit_logs": list_internal_alpha_audit_logs()}


@router.post("/dry-run")
def internal_alpha_dry_run(request: InternalAlphaDryRunRequest) -> dict[str, Any]:
    return run_internal_alpha_dry_run(request)
