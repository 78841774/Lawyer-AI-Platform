import hashlib

from personal_skill_studio.training_artifacts.practice_runtime_registry import (
    count_usage_for_load,
    list_runtime_load_records,
    write_risk_event,
    write_runtime_load,
    write_usage_event,
)
from personal_skill_studio.training_artifacts.practice_runtime_safety_engine import v731g_safety_flags
from personal_skill_studio.training_artifacts.practice_runtime_usage_audit import (
    build_risk_event,
    build_runtime_audit_event,
    build_usage_event,
)
from personal_skill_studio.training_artifacts.schemas import (
    PracticeRuntimeLoadRecord,
    PracticeRuntimePolicyEvaluateRequest,
    PracticeRuntimePolicyEvaluateResult,
)


def evaluate_practice_runtime_policy(request: PracticeRuntimePolicyEvaluateRequest) -> dict:
    candidates = [_with_usage_count(record) for record in list_runtime_load_records()]
    active_candidates = [record for record in candidates if record.load_status in {"loaded_gray", "loaded_active"}]
    matched_scope = [record for record in active_candidates if _matches_scope(record, request)]
    allowed_record, blocked_reason = _select_allowed_record(matched_scope, request)
    allowed = allowed_record is not None
    target_record = allowed_record or (matched_scope[0] if matched_scope else None)
    usage_event = build_usage_event(
        request=request,
        runtime_load_id=target_record.runtime_load_id if target_record else "no_matched_runtime_load",
        package_id=target_record.experience_package_id if target_record else "no_matched_package",
        package_version=target_record.package_version if target_record else "none",
        allowed=allowed,
        block_reason=None if allowed else (blocked_reason or "no_runtime_load_matched_policy"),
        safety_flags=["source_trace_required", "audit_required", "lawyer_review_required", "draft_only"],
    )
    write_usage_event(usage_event)
    if allowed_record:
        updated = allowed_record.model_copy(deep=True)
        updated.usage_count_today = count_usage_for_load(updated.runtime_load_id)
        updated.audit_events.append(
            build_runtime_audit_event(
                updated.runtime_load_id,
                "runtime_policy_allowed",
                request.user_id,
                "policy evaluate allowed approved package metadata",
            )
        )
        write_runtime_load(updated)
    else:
        write_risk_event(build_risk_event(usage_event, severity="low" if matched_scope else "medium"))
    return PracticeRuntimePolicyEvaluateResult(
        allowed=allowed,
        blocked_reason=None if allowed else usage_event.block_reason,
        matched_package_ids=[record.experience_package_id for record in matched_scope],
        active_package_versions=[record.package_version for record in matched_scope],
        usage_boundary=_usage_boundary(allowed_record or target_record),
        audit_id=usage_event.audit_id,
        usage_event=usage_event,
        **v731g_safety_flags(),
    ).model_dump()


def _with_usage_count(record: PracticeRuntimeLoadRecord) -> PracticeRuntimeLoadRecord:
    return record.model_copy(update={"usage_count_today": count_usage_for_load(record.runtime_load_id)})


def _matches_scope(record: PracticeRuntimeLoadRecord, request: PracticeRuntimePolicyEvaluateRequest) -> bool:
    return (
        _matches_list(record.enabled_case_causes, request.case_cause)
        and _matches_list(record.enabled_workspaces, request.workspace_id)
        and _matches_list(record.enabled_runtime_modes, request.runtime_mode)
        and _matches_list(record.enabled_task_types, request.requested_task_type)
    )


def _matches_list(allowed_values: list[str], requested_value: str) -> bool:
    return not allowed_values or requested_value in allowed_values


def _select_allowed_record(
    records: list[PracticeRuntimeLoadRecord],
    request: PracticeRuntimePolicyEvaluateRequest,
) -> tuple[PracticeRuntimeLoadRecord | None, str | None]:
    if not records:
        return None, "no_runtime_load_matched_policy"
    for record in records:
        if record.load_status == "loaded_gray" and not _gray_rollout_allows(record, request):
            continue
        if record.usage_limit_per_day and count_usage_for_load(record.runtime_load_id) >= record.usage_limit_per_day:
            continue
        return record, None
    return None, "rollout_or_usage_limit_blocked"


def _gray_rollout_allows(record: PracticeRuntimeLoadRecord, request: PracticeRuntimePolicyEvaluateRequest) -> bool:
    rollout_percentage = max(0, min(record.rollout_percentage, 100))
    if rollout_percentage <= 0:
        return False
    if rollout_percentage >= 100:
        return True
    seed = f"{record.runtime_load_id}:{request.user_id}:{request.workspace_id}:{request.case_cause}"
    bucket = int(hashlib.sha256(seed.encode("utf-8")).hexdigest()[:8], 16) % 100
    return bucket < rollout_percentage


def _usage_boundary(record: PracticeRuntimeLoadRecord | None) -> dict[str, str | int | bool | list[str]]:
    if record is None:
        return {
            "draft_only": True,
            "lawyer_review_required": True,
            "source_trace_required": True,
            "external_delivery_triggered": False,
            "matched_runtime_load": False,
        }
    return {
        "runtime_load_id": record.runtime_load_id,
        "rollout_mode": record.rollout_mode,
        "rollout_percentage": record.rollout_percentage,
        "usage_limit_per_day": record.usage_limit_per_day,
        "usage_count_today": count_usage_for_load(record.runtime_load_id),
        "enabled_case_causes": record.enabled_case_causes,
        "enabled_workspaces": record.enabled_workspaces,
        "enabled_runtime_modes": record.enabled_runtime_modes,
        "enabled_task_types": record.enabled_task_types,
        "draft_only": True,
        "lawyer_review_required": True,
        "source_trace_required": True,
        "external_delivery_triggered": False,
    }
