from datetime import UTC, datetime

from personal_skill_studio.training_artifacts.practice_load_review_gate import get_practice_load_package
from personal_skill_studio.training_artifacts.practice_runtime_registry import write_runtime_load
from personal_skill_studio.training_artifacts.practice_runtime_safety_engine import (
    build_runtime_safety_report,
    v731g_safety_flags,
)
from personal_skill_studio.training_artifacts.practice_runtime_source_trace_engine import build_runtime_source_trace
from personal_skill_studio.training_artifacts.practice_runtime_usage_audit import build_runtime_audit_event
from personal_skill_studio.training_artifacts.schemas import (
    PracticeLoadReviewPackage,
    PracticeRuntimeLoadRecord,
    PracticeRuntimeLoadRequest,
)


def load_practice_runtime_package(request: PracticeRuntimeLoadRequest) -> dict | None:
    package_payload = get_practice_load_package(request.experience_package_id)
    if package_payload is None:
        return None
    package = PracticeLoadReviewPackage(**package_payload)
    runtime_load_id = _runtime_load_id(package.package_id)
    safety_report = build_runtime_safety_report(runtime_load_id, package)
    source_trace = build_runtime_source_trace(runtime_load_id, package)
    load_status = _initial_load_status(request.rollout_mode, safety_report.load_allowed)
    audit_action = "runtime_load_blocked" if load_status == "blocked" else f"runtime_{load_status}"
    record = PracticeRuntimeLoadRecord(
        runtime_load_id=runtime_load_id,
        experience_package_id=package.package_id,
        lawyer_approved_package_id=f"{package.package_id}_lawyer_approved_package",
        package_name=package.package_name,
        package_version=package.package_version,
        load_status=load_status,
        load_scope=_load_scope(request),
        enabled_case_causes=request.allowed_case_causes,
        enabled_workspaces=request.allowed_workspaces,
        enabled_runtime_modes=request.allowed_runtime_modes,
        enabled_task_types=request.allowed_task_types,
        rollout_mode=request.rollout_mode if safety_report.load_allowed else "disabled",
        rollout_percentage=_clamp_percentage(request.rollout_percentage) if safety_report.load_allowed else 0,
        usage_limit_per_day=max(request.usage_limit_per_day, 0),
        emergency_disable_enabled=request.emergency_disable_enabled,
        loaded_at=datetime.now(UTC).isoformat(),
        loaded_by=request.loaded_by,
        source_trace_bundle_id=source_trace.source_trace_bundle_id,
        audit_bundle_id=f"{runtime_load_id}_audit_bundle",
        safety_report_id=safety_report.safety_report_id,
        source_trace_bundle=source_trace,
        safety_report=safety_report,
        audit_events=[
            build_runtime_audit_event(runtime_load_id, audit_action, request.loaded_by, "practice runtime load request"),
        ],
        blocked_reasons=safety_report.blocked_reasons,
        warnings=[
            "Practice runtime record contains approved experience package metadata only.",
            "Controlled loading does not call providers or return source content.",
        ],
        **v731g_safety_flags(),
    )
    write_runtime_load(record)
    return record.model_dump()


def _runtime_load_id(package_id: str) -> str:
    return f"{package_id}_runtime_load_{datetime.now(UTC).strftime('%Y%m%d%H%M%S%f')}"


def _initial_load_status(rollout_mode: str, load_allowed: bool) -> str:
    if not load_allowed:
        return "blocked"
    if rollout_mode == "gray":
        return "loaded_gray"
    if rollout_mode == "active":
        return "loaded_active"
    return "loaded_disabled"


def _load_scope(request: PracticeRuntimeLoadRequest) -> dict[str, list[str] | str | int | bool]:
    return {
        "rollout_mode": request.rollout_mode,
        "rollout_percentage": _clamp_percentage(request.rollout_percentage),
        "allowed_case_causes": request.allowed_case_causes,
        "allowed_workspaces": request.allowed_workspaces,
        "allowed_runtime_modes": request.allowed_runtime_modes,
        "allowed_task_types": request.allowed_task_types,
        "usage_limit_per_day": max(request.usage_limit_per_day, 0),
        "emergency_disable_enabled": request.emergency_disable_enabled,
    }


def _clamp_percentage(value: int) -> int:
    return max(0, min(value, 100))
