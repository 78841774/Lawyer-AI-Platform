from datetime import UTC, datetime

from personal_skill_studio.training_artifacts.practice_runtime_registry import (
    list_runtime_load_records,
    write_runtime_load,
)
from personal_skill_studio.training_artifacts.practice_runtime_usage_audit import build_runtime_audit_event
from personal_skill_studio.training_artifacts.schemas import (
    PracticeRuntimeDisableRequest,
    PracticeRuntimeLoadRecord,
    PracticeRuntimeRollbackRequest,
    PracticeRuntimeRolloutRequest,
)


def enable_runtime_load_gray(runtime_load_id: str, request: PracticeRuntimeRolloutRequest) -> dict | None:
    return _set_runtime_rollout(runtime_load_id, "loaded_gray", "gray", request)


def enable_runtime_load_active(runtime_load_id: str, request: PracticeRuntimeRolloutRequest) -> dict | None:
    return _set_runtime_rollout(runtime_load_id, "loaded_active", "active", request)


def disable_runtime_load(runtime_load_id: str, request: PracticeRuntimeDisableRequest) -> dict | None:
    record = _get_load_record(runtime_load_id)
    if record is None:
        return None
    updated = record.model_copy(deep=True)
    updated.load_status = "blocked" if request.mark_blocked else "disabled"
    updated.rollout_mode = "disabled"
    updated.rollout_percentage = 0
    updated.disabled_at = datetime.now(UTC).isoformat()
    updated.audit_events.append(
        build_runtime_audit_event(
            runtime_load_id,
            "runtime_load_blocked" if request.mark_blocked else "runtime_load_disabled",
            request.operator_id,
            request.operator_note,
        )
    )
    write_runtime_load(updated)
    return updated.model_dump()


def rollback_runtime_load(runtime_load_id: str, request: PracticeRuntimeRollbackRequest) -> dict | None:
    current = _get_load_record(runtime_load_id)
    if current is None:
        return None
    target = _get_load_record(request.rollback_to_load_id) if request.rollback_to_load_id else _find_rollback_target(current)
    updated_current = current.model_copy(deep=True)
    updated_current.load_status = "rolled_back"
    updated_current.rollout_mode = "disabled"
    updated_current.rollout_percentage = 0
    updated_current.disabled_at = datetime.now(UTC).isoformat()
    updated_current.rollback_to_load_id = target.runtime_load_id if target else None
    updated_current.audit_events.append(
        build_runtime_audit_event(runtime_load_id, "runtime_load_rolled_back", request.operator_id, request.operator_note)
    )
    write_runtime_load(updated_current)
    response = updated_current.model_dump()
    if target:
        updated_target = target.model_copy(deep=True)
        updated_target.load_status = "loaded_active"
        updated_target.rollout_mode = "active"
        updated_target.rollout_percentage = 100
        updated_target.rollback_from_load_id = runtime_load_id
        updated_target.audit_events.append(
            build_runtime_audit_event(
                updated_target.runtime_load_id,
                "runtime_load_restored_by_rollback",
                request.operator_id,
                request.operator_note,
            )
        )
        write_runtime_load(updated_target)
        response["rollback_target"] = updated_target.model_dump()
    else:
        response["rollback_target"] = None
    return response


def list_rollback_candidates(runtime_load_id: str) -> list[dict]:
    current = _get_load_record(runtime_load_id)
    if current is None:
        return []
    return [
        record.model_dump()
        for record in list_runtime_load_records()
        if record.runtime_load_id != runtime_load_id
        and record.experience_package_id == current.experience_package_id
        and record.load_status in {"loaded_disabled", "loaded_gray", "loaded_active", "disabled", "rollback_ready"}
    ]


def _set_runtime_rollout(
    runtime_load_id: str,
    load_status: str,
    rollout_mode: str,
    request: PracticeRuntimeRolloutRequest,
) -> dict | None:
    record = _get_load_record(runtime_load_id)
    if record is None or record.load_status in {"blocked", "rolled_back"}:
        return None
    updated = record.model_copy(deep=True)
    updated.load_status = load_status
    updated.rollout_mode = rollout_mode
    updated.rollout_percentage = 100 if rollout_mode == "active" else max(0, min(request.rollout_percentage, 100))
    if request.usage_limit_per_day is not None:
        updated.usage_limit_per_day = max(request.usage_limit_per_day, 0)
    updated.disabled_at = None
    updated.audit_events.append(
        build_runtime_audit_event(runtime_load_id, f"runtime_{rollout_mode}_enabled", request.operator_id, request.operator_note)
    )
    write_runtime_load(updated)
    return updated.model_dump()


def _get_load_record(runtime_load_id: str | None) -> PracticeRuntimeLoadRecord | None:
    if not runtime_load_id:
        return None
    for record in list_runtime_load_records():
        if record.runtime_load_id == runtime_load_id:
            return record
    return None


def _find_rollback_target(current: PracticeRuntimeLoadRecord) -> PracticeRuntimeLoadRecord | None:
    candidates = [
        record
        for record in list_runtime_load_records()
        if record.runtime_load_id != current.runtime_load_id
        and record.experience_package_id == current.experience_package_id
        and record.load_status in {"loaded_disabled", "loaded_gray", "loaded_active", "disabled", "rollback_ready"}
    ]
    return candidates[0] if candidates else None
