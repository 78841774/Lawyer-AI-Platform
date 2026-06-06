from datetime import UTC, datetime

from personal_skill_studio.training_artifacts.practice_runtime_safety_engine import v731g_safety_flags
from personal_skill_studio.training_artifacts.schemas import (
    PracticeRuntimeAuditEvent,
    PracticeRuntimePolicyEvaluateRequest,
    PracticeRuntimeRiskEvent,
    PracticeRuntimeUsageEvent,
)


def build_runtime_audit_event(
    runtime_load_id: str,
    action: str,
    operator_id: str | None = None,
    operator_note: str | None = None,
) -> PracticeRuntimeAuditEvent:
    return PracticeRuntimeAuditEvent(
        event_id=f"{runtime_load_id}_runtime_audit_{action}_{datetime.now(UTC).strftime('%Y%m%d%H%M%S%f')}",
        runtime_load_id=runtime_load_id,
        action=action,
        operator_id=operator_id,
        operator_note=operator_note,
        timestamp=datetime.now(UTC).isoformat(),
    )


def build_usage_event(
    request: PracticeRuntimePolicyEvaluateRequest,
    runtime_load_id: str,
    package_id: str,
    package_version: str,
    allowed: bool,
    block_reason: str | None,
    safety_flags: list[str],
) -> PracticeRuntimeUsageEvent:
    usage_event_id = f"practice_runtime_usage_{datetime.now(UTC).strftime('%Y%m%d%H%M%S%f')}"
    return PracticeRuntimeUsageEvent(
        usage_event_id=usage_event_id,
        package_id=package_id,
        package_version=package_version,
        runtime_load_id=runtime_load_id,
        runtime_mode=request.runtime_mode,
        case_cause=request.case_cause,
        task_type=request.requested_task_type,
        user_id=request.user_id,
        owner_id=request.user_id,
        workspace_id=request.workspace_id,
        timestamp=datetime.now(UTC).isoformat(),
        allowed=allowed,
        block_reason=block_reason,
        safety_flags=safety_flags,
        audit_id=f"{usage_event_id}_audit",
        **v731g_safety_flags(),
    )


def build_risk_event(usage_event: PracticeRuntimeUsageEvent, severity: str = "medium") -> PracticeRuntimeRiskEvent:
    return PracticeRuntimeRiskEvent(
        risk_event_id=f"{usage_event.usage_event_id}_risk",
        usage_event_id=usage_event.usage_event_id,
        runtime_load_id=usage_event.runtime_load_id,
        package_id=usage_event.package_id,
        severity=severity,
        risk_type="policy_block",
        risk_summary=usage_event.block_reason or "Practice runtime request was blocked by metadata policy.",
        created_at=datetime.now(UTC).isoformat(),
        audit_id=f"{usage_event.usage_event_id}_risk_audit",
        **v731g_safety_flags(),
    )
