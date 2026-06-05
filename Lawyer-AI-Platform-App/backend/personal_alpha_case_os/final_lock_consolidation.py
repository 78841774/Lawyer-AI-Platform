from typing import Any

from personal_alpha_case_os.schemas import (
    PersonalAlphaCaseOSFinalLockConsolidation,
    PersonalAlphaCaseOSFinalLockSummary,
    PersonalAlphaCaseOSLinkedMetadata,
    PersonalAlphaCaseOSSafetyChecklist,
)


def build_final_lock_consolidation(
    case_id: str,
    context: dict[str, Any],
    review_state_payload: dict[str, Any],
) -> dict[str, Any]:
    latest_lock = _latest_record(context.get("locks", []))
    latest_action = _latest_record(context.get("lawyer_actions", []))
    final_lock_created = bool(context.get("latest_lock_id"))
    review_state = str(review_state_payload.get("review_state", "blocked"))
    completed_metadata_review = final_lock_created and review_state == "completed_metadata_review"
    if completed_metadata_review:
        consolidation_status = "metadata_closure_ready"
    elif final_lock_created:
        consolidation_status = "blocked"
    else:
        consolidation_status = "final_lock_pending"
    warnings = ["Final lock consolidation is metadata-only and advisory."]
    if context.get("blocked"):
        consolidation_status = "blocked"
        warnings.extend(str(item) for item in context.get("blocked_reasons", []) if item)
    elif not final_lock_created:
        warnings.append("Final lock metadata is missing. No final lock is created by v6.4.")
    return PersonalAlphaCaseOSFinalLockConsolidation(
        case_id=case_id,
        consolidation_status=consolidation_status,
        final_lock_created=final_lock_created,
        latest_lock_id=context.get("latest_lock_id") or None,
        latest_packet_id=context.get("latest_packet_id") or None,
        latest_lawyer_review_action=context.get("latest_lawyer_action") or None,
        review_state=review_state,
        completed_metadata_review=completed_metadata_review,
        final_lock_summary=_final_lock_summary(context, latest_lock),
        linked_metadata=PersonalAlphaCaseOSLinkedMetadata(
            workspace_run_id=context.get("latest_workspace_run_id") or None,
            packet_id=context.get("latest_packet_id") or None,
            lawyer_review_action_id=latest_action.get("action_id") or None,
            lock_id=context.get("latest_lock_id") or None,
        ),
        safety_checklist=PersonalAlphaCaseOSSafetyChecklist(),
        mock_or_redacted_only=True,
        raw_content_included=False,
        warnings=list(dict.fromkeys(warnings)),
    ).model_dump()


def _final_lock_summary(context: dict[str, Any], latest_lock: dict[str, Any]) -> PersonalAlphaCaseOSFinalLockSummary:
    return PersonalAlphaCaseOSFinalLockSummary(
        lock_id=latest_lock.get("lock_id") or context.get("latest_lock_id") or None,
        packet_id=latest_lock.get("packet_id") or context.get("latest_packet_id") or None,
        workspace_run_id=latest_lock.get("workspace_run_id") or context.get("latest_workspace_run_id") or None,
        lock_status=str(latest_lock.get("status") or ("final_lock_created" if context.get("latest_lock_id") else "final_lock_pending")),
        locked_metadata_only=True,
        raw_content_included=False,
        final_legal_opinion_generated=False,
        final_report_generated=False,
        created_at=latest_lock.get("created_at") or None,
    )


def _latest_record(value: Any) -> dict[str, Any]:
    records = [item for item in value if isinstance(item, dict)] if isinstance(value, list) else []
    if not records:
        return {}
    return sorted(records, key=lambda item: str(item.get("created_at", "")))[-1]
