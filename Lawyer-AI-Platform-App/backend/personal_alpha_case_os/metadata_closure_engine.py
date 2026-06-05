from typing import Any

from personal_alpha_case_os.metadata_closure_checklist import build_metadata_closure_summary
from personal_alpha_case_os.next_action_engine import build_next_action
from personal_alpha_case_os.schemas import (
    PersonalAlphaCaseOSMetadataClosure,
    PersonalAlphaCaseOSMetadataClosureBlocker,
    PersonalAlphaCaseOSMetadataClosureBlockers,
)

BLOCKER_ROUTES = {
    "workspace_run_ready": ("workspace_run_missing", "workspace_run", "create_workspace_run", "/personal-alpha-workspace"),
    "source_review_completed": ("source_review_missing", "source_review", "review_sources", "/personal-alpha-source-review"),
    "source_decision_completed": ("source_decision_missing", "source_review_decision", "submit_source_review_decision", "/personal-alpha-source-review"),
    "final_readiness_ready": ("final_readiness_missing", "final_readiness", "check_final_readiness", "/personal-alpha-final-readiness"),
    "final_gate_approved": ("final_gate_missing", "final_gate", "submit_final_gate_decision", "/personal-alpha-final-gate"),
    "final_packet_created": ("final_packet_missing", "final_packet", "create_final_packet", "/personal-alpha-final-packet"),
    "lawyer_review_approved": ("lawyer_review_approval_missing", "lawyer_final_review", "submit_lawyer_final_review", "/personal-alpha-lawyer-final-review"),
    "final_lock_created": ("final_lock_missing", "final_lock", "create_final_lock", "/personal-alpha-final-lock"),
    "audit_timeline_available": ("audit_timeline_missing", "audit_timeline", "review_audit_timeline", "/case-os"),
    "redaction_check_passed": ("redaction_check_failed", "audit_timeline", "review_redaction_check", "/case-os"),
}


def build_metadata_closure(
    case_id: str,
    context: dict[str, Any],
    review_state_payload: dict[str, Any],
    audit_summary: dict[str, Any],
    redaction_check: dict[str, Any],
    checklist_payload: dict[str, Any],
) -> dict[str, Any]:
    blockers_payload = build_metadata_closure_blockers(case_id, context, checklist_payload)
    closure_summary = build_metadata_closure_summary(context, audit_summary, redaction_check)
    closure_ready = bool(checklist_payload.get("closure_ready", False)) and not bool(blockers_payload.get("blocked", False))
    completed_metadata_review = closure_ready and str(review_state_payload.get("review_state", "")) == "completed_metadata_review"
    if completed_metadata_review:
        closure_status = "completed_metadata_review"
    elif blockers_payload.get("blocked"):
        closure_status = "blocked"
    else:
        closure_status = "pending"
    next_action = build_next_action(case_id, context)
    target_route = f"/case-os/{case_id}" if completed_metadata_review and case_id else str(next_action.get("target_route", "/case-os"))
    if not case_id:
        target_route = "/case-os"
    return PersonalAlphaCaseOSMetadataClosure(
        case_id=case_id,
        closure_status=closure_status,
        completed_metadata_review=completed_metadata_review,
        closure_ready=closure_ready,
        review_state=str(review_state_payload.get("review_state", "blocked")),
        terminal=bool(review_state_payload.get("terminal", False)),
        blocked=bool(blockers_payload.get("blocked", False)),
        blocked_reasons=[str(item) for item in blockers_payload.get("blocked_reasons", [])],
        closure_summary=closure_summary,
        next_action="view_completed_metadata_review" if completed_metadata_review else str(next_action.get("next_action", "resolve_blockers")),
        target_route=target_route,
        mock_or_redacted_only=True,
        raw_content_included=False,
        final_legal_opinion_generated=False,
        final_report_generated=False,
        warnings=["Metadata closure is metadata-only and does not create a final report."],
    ).model_dump()


def build_metadata_closure_blockers(
    case_id: str,
    context: dict[str, Any],
    checklist_payload: dict[str, Any],
) -> dict[str, Any]:
    blockers: list[PersonalAlphaCaseOSMetadataClosureBlocker] = []
    for item in checklist_payload.get("checklist", []):
        if not isinstance(item, dict) or not item.get("required", True) or item.get("passed", False):
            continue
        check_id = str(item.get("check_id", "metadata_check_failed"))
        blocker_id, stage_id, required_action, target_route = BLOCKER_ROUTES.get(
            check_id,
            (f"{check_id}_failed", "metadata_closure", "resolve_metadata_closure_blocker", "/case-os"),
        )
        blockers.append(
            PersonalAlphaCaseOSMetadataClosureBlocker(
                blocker_id=blocker_id,
                stage_id=stage_id,
                blocked=True,
                reason=f"{check_id} is required for metadata closure.",
                required_action=required_action,
                target_route=target_route,
                mock_or_redacted_only=True,
            )
        )
    for reason in context.get("blocked_reasons", []) if context.get("blocked") else []:
        blockers.insert(
            0,
            PersonalAlphaCaseOSMetadataClosureBlocker(
                blocker_id="case_context_blocked",
                stage_id="case_os",
                blocked=True,
                reason=str(reason),
                required_action="resolve_blockers",
                target_route="/case-os",
                mock_or_redacted_only=True,
            ),
        )
    blocked_reasons = [str(item.reason) for item in blockers if item.reason]
    return PersonalAlphaCaseOSMetadataClosureBlockers(
        case_id=case_id,
        blocked=bool(blockers),
        blocked_reasons=list(dict.fromkeys(blocked_reasons)),
        closure_blockers=blockers,
        required_blocker_count=sum(1 for item in blockers if item.blocked),
        mock_or_redacted_only=True,
        raw_content_included=False,
        warnings=["Closure blockers are metadata-only and advisory."],
    ).model_dump()
