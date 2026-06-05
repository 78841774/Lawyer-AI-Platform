from typing import Any

from fastapi import APIRouter

from personal_alpha_case_os.case_os_engine import (
    get_personal_alpha_case_os_action_eligibility,
    get_personal_alpha_case_os_audit_timeline_filters,
    get_personal_alpha_case_os_audit_timeline_redaction_check,
    get_personal_alpha_case_os_audit_timeline_summary,
    get_personal_alpha_case_os_audit_timeline,
    get_personal_alpha_case_os_blockers,
    get_personal_alpha_case_os_case_detail,
    get_personal_alpha_case_os_next_action,
    get_personal_alpha_case_os_review_state,
    get_personal_alpha_case_os_review_state_history,
    get_personal_alpha_case_os_review_state_summary,
    get_personal_alpha_case_os_review_state_transition_validation,
    get_personal_alpha_case_os_review_state_transitions,
    get_personal_alpha_case_os_safety_checklist,
    get_personal_alpha_case_os_stage_orchestration,
    get_personal_alpha_case_os_stage_transitions,
    get_personal_alpha_case_os_status,
    get_personal_alpha_case_os_unified_audit_timeline,
    list_personal_alpha_case_os_cases,
)

router = APIRouter(prefix="/case-os", tags=["personal-alpha-case-os"])


@router.get("/status")
def personal_alpha_case_os_status() -> dict[str, Any]:
    return get_personal_alpha_case_os_status()


@router.get("")
def personal_alpha_case_os_cases() -> list[dict[str, Any]]:
    return list_personal_alpha_case_os_cases()


@router.get("/{case_id}")
def personal_alpha_case_os_case_detail(case_id: str) -> dict[str, Any]:
    return get_personal_alpha_case_os_case_detail(case_id)


@router.get("/{case_id}/audit-timeline")
def personal_alpha_case_os_audit_timeline(case_id: str) -> dict[str, Any]:
    return get_personal_alpha_case_os_audit_timeline(case_id)


@router.get("/{case_id}/audit-timeline/unified")
def personal_alpha_case_os_unified_audit_timeline(
    case_id: str,
    stage_id: str | None = None,
    event_type: str | None = None,
    result: str | None = None,
    safety_status: str | None = None,
    limit: int | None = None,
    offset: int | None = None,
) -> dict[str, Any]:
    return get_personal_alpha_case_os_unified_audit_timeline(
        case_id,
        stage_id=stage_id,
        event_type=event_type,
        result=result,
        safety_status=safety_status,
        limit=limit,
        offset=offset,
    )


@router.get("/{case_id}/audit-timeline/summary")
def personal_alpha_case_os_audit_timeline_summary(case_id: str) -> dict[str, Any]:
    return get_personal_alpha_case_os_audit_timeline_summary(case_id)


@router.get("/{case_id}/audit-timeline/redaction-check")
def personal_alpha_case_os_audit_timeline_redaction_check(case_id: str) -> dict[str, Any]:
    return get_personal_alpha_case_os_audit_timeline_redaction_check(case_id)


@router.get("/{case_id}/audit-timeline/filters")
def personal_alpha_case_os_audit_timeline_filters(case_id: str) -> dict[str, Any]:
    return get_personal_alpha_case_os_audit_timeline_filters(case_id)


@router.get("/{case_id}/next-action")
def personal_alpha_case_os_next_action(case_id: str) -> dict[str, Any]:
    return get_personal_alpha_case_os_next_action(case_id)


@router.get("/{case_id}/safety-checklist")
def personal_alpha_case_os_safety_checklist(case_id: str) -> dict[str, Any]:
    return get_personal_alpha_case_os_safety_checklist(case_id)


@router.get("/{case_id}/review-state")
def personal_alpha_case_os_review_state(case_id: str) -> dict[str, Any]:
    return get_personal_alpha_case_os_review_state(case_id)


@router.get("/{case_id}/review-state/history")
def personal_alpha_case_os_review_state_history(case_id: str) -> dict[str, Any]:
    return get_personal_alpha_case_os_review_state_history(case_id)


@router.get("/{case_id}/review-state/transitions")
def personal_alpha_case_os_review_state_transitions(case_id: str) -> dict[str, Any]:
    return get_personal_alpha_case_os_review_state_transitions(case_id)


@router.get("/{case_id}/review-state/validate-transition")
def personal_alpha_case_os_review_state_validate_transition(case_id: str, from_state: str, to_state: str) -> dict[str, Any]:
    return get_personal_alpha_case_os_review_state_transition_validation(case_id, from_state, to_state)


@router.get("/{case_id}/review-state/summary")
def personal_alpha_case_os_review_state_summary(case_id: str) -> dict[str, Any]:
    return get_personal_alpha_case_os_review_state_summary(case_id)


@router.get("/{case_id}/stage-orchestration")
def personal_alpha_case_os_stage_orchestration(case_id: str) -> dict[str, Any]:
    return get_personal_alpha_case_os_stage_orchestration(case_id)


@router.get("/{case_id}/stage-transitions")
def personal_alpha_case_os_stage_transitions(case_id: str) -> dict[str, Any]:
    return get_personal_alpha_case_os_stage_transitions(case_id)


@router.get("/{case_id}/action-eligibility")
def personal_alpha_case_os_action_eligibility(case_id: str) -> dict[str, Any]:
    return get_personal_alpha_case_os_action_eligibility(case_id)


@router.get("/{case_id}/blockers")
def personal_alpha_case_os_blockers(case_id: str) -> dict[str, Any]:
    return get_personal_alpha_case_os_blockers(case_id)


@router.get("/{case_id:path}/stage-orchestration")
def personal_alpha_case_os_path_like_stage_orchestration(case_id: str) -> dict[str, Any]:
    return get_personal_alpha_case_os_stage_orchestration(case_id)


@router.get("/{case_id:path}/audit-timeline/unified")
def personal_alpha_case_os_path_like_unified_audit_timeline(
    case_id: str,
    stage_id: str | None = None,
    event_type: str | None = None,
    result: str | None = None,
    safety_status: str | None = None,
    limit: int | None = None,
    offset: int | None = None,
) -> dict[str, Any]:
    return get_personal_alpha_case_os_unified_audit_timeline(
        case_id,
        stage_id=stage_id,
        event_type=event_type,
        result=result,
        safety_status=safety_status,
        limit=limit,
        offset=offset,
    )


@router.get("/{case_id:path}/review-state")
def personal_alpha_case_os_path_like_review_state(case_id: str) -> dict[str, Any]:
    return get_personal_alpha_case_os_review_state(case_id)
