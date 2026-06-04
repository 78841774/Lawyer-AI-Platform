from typing import Any

from fastapi import APIRouter

from local_sandbox.audit_log import list_audit_logs
from local_sandbox.dry_run import run_local_sandbox_dry_run
from local_sandbox.guards import get_all_guards
from local_sandbox.schemas import LocalSandboxDryRunRequest, LocalSandboxStatus

router = APIRouter(prefix="/local-sandbox", tags=["local-sandbox"])


@router.get("/status")
def get_local_sandbox_status() -> dict[str, Any]:
    return LocalSandboxStatus(
        warnings=[
            "v3.9 local sandbox is dry-run only.",
            "Real case processing remains disabled.",
            "Live providers remain disabled.",
            "Manual review is required before any future real case workflow."
        ]
    ).model_dump()


@router.get("/guards")
def get_local_sandbox_guards() -> dict[str, Any]:
    return get_all_guards()


@router.post("/dry-run")
def create_local_sandbox_dry_run(request: LocalSandboxDryRunRequest) -> dict[str, Any]:
    return run_local_sandbox_dry_run(request)


@router.get("/audit-logs")
def get_local_sandbox_audit_logs() -> dict[str, Any]:
    return {"audit_logs": list_audit_logs()}
