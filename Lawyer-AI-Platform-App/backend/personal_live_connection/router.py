from typing import Any

from fastapi import APIRouter, HTTPException

from personal_live_connection.audit_engine import build_audit_timeline
from personal_live_connection.health_engine import build_health_dry_run
from personal_live_connection.live_gate_engine import build_live_gate
from personal_live_connection.provider_registry import build_provider, build_provider_list
from personal_live_connection.readiness_engine import build_status
from personal_live_connection.router_helpers import ensure_provider
from personal_live_connection.run_engine import create_run, get_run, list_runs, record_action
from personal_live_connection.runtime_registry import build_runtimes
from personal_live_connection.safety_engine import build_safety_status
from personal_live_connection.schemas import LiveConnectionRunActionRequest, LiveConnectionRunRequest
from personal_live_connection.secret_boundary import build_secret_boundary
from personal_live_connection.usage_policy_engine import build_usage_policy


router = APIRouter(prefix="/personal-live-connection", tags=["personal-live-connection"])


@router.get("/status")
def status() -> dict[str, Any]:
    return build_status()


@router.get("/runtimes")
def runtimes() -> dict[str, Any]:
    return build_runtimes()


@router.get("/providers")
def providers() -> dict[str, Any]:
    return build_provider_list()


@router.get("/providers/{provider_id}")
def provider_detail(provider_id: str) -> dict[str, Any]:
    return ensure_provider(build_provider(provider_id)).model_dump()


@router.get("/providers/{provider_id}/secret-boundary")
def provider_secret_boundary(provider_id: str) -> dict[str, Any]:
    return ensure_provider(build_secret_boundary(provider_id)).model_dump()


@router.get("/providers/{provider_id}/live-gate")
def provider_live_gate(provider_id: str) -> dict[str, Any]:
    return ensure_provider(build_live_gate(provider_id)).model_dump()


@router.get("/providers/{provider_id}/usage-policy")
def provider_usage_policy(provider_id: str) -> dict[str, Any]:
    return ensure_provider(build_usage_policy(provider_id)).model_dump()


@router.get("/providers/{provider_id}/health/dry-run")
def provider_health_dry_run(provider_id: str) -> dict[str, Any]:
    return ensure_provider(build_health_dry_run(provider_id)).model_dump()


@router.post("/runs/dry-run")
def runs_dry_run(request: LiveConnectionRunRequest) -> dict[str, Any]:
    return create_run(request, dry_run=True)


@router.post("/runs")
def runs_live_attempt(request: LiveConnectionRunRequest) -> dict[str, Any]:
    return create_run(request, dry_run=False)


@router.get("/runs")
def runs() -> dict[str, Any]:
    return list_runs()


@router.get("/runs/{run_id}")
def run_detail(run_id: str) -> dict[str, Any]:
    run = get_run(run_id)
    if run is None:
        raise HTTPException(status_code=404, detail="run_id not found")
    return run.model_dump()


@router.post("/runs/{run_id}/actions")
def run_actions(run_id: str, request: LiveConnectionRunActionRequest) -> dict[str, Any]:
    return record_action(run_id, request)


@router.get("/audit")
def audit() -> dict[str, Any]:
    return build_audit_timeline()


@router.get("/safety")
def safety() -> dict[str, Any]:
    return build_safety_status()

