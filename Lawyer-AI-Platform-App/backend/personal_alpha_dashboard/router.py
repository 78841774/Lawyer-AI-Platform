from typing import Any

from fastapi import APIRouter

from personal_alpha_dashboard.dashboard_engine import (
    get_personal_alpha_dashboard_audit_timeline,
    get_personal_alpha_dashboard_source_trace_summary,
    get_personal_alpha_dashboard_stage_health,
    get_personal_alpha_dashboard_status,
    get_personal_alpha_dashboard_summary,
)

router = APIRouter(prefix="/personal-alpha-dashboard", tags=["personal-alpha-dashboard"])


@router.get("/status")
def personal_alpha_dashboard_status() -> dict[str, Any]:
    return get_personal_alpha_dashboard_status()


@router.get("/summary")
def personal_alpha_dashboard_summary() -> dict[str, Any]:
    return get_personal_alpha_dashboard_summary()


@router.get("/stage-health")
def personal_alpha_dashboard_stage_health() -> dict[str, Any]:
    return get_personal_alpha_dashboard_stage_health()


@router.get("/audit-timeline")
def personal_alpha_dashboard_audit_timeline() -> dict[str, Any]:
    return get_personal_alpha_dashboard_audit_timeline()


@router.get("/source-trace-summary")
def personal_alpha_dashboard_source_trace_summary() -> dict[str, Any]:
    return get_personal_alpha_dashboard_source_trace_summary()
