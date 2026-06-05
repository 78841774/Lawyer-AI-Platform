from typing import Any

from personal_alpha_case_os.next_action_engine import build_next_action
from personal_alpha_case_os.review_state_history import build_review_state_history
from personal_alpha_case_os.review_state_rules import (
    RULES_BY_FROM,
    TERMINAL_STATES,
    ReviewTransitionRule,
    is_terminal_state,
    state_label,
)
from personal_alpha_case_os.review_state_validation import validate_review_transition
from personal_alpha_case_os.schemas import (
    PersonalAlphaCaseOSReviewState,
    PersonalAlphaCaseOSReviewStateSummary,
    PersonalAlphaCaseOSReviewStateSummaryStats,
    PersonalAlphaCaseOSReviewStateTransition,
    PersonalAlphaCaseOSReviewStateTransitions,
)
from personal_alpha_case_os.stage_orchestrator import build_stage_orchestration


def build_review_state(case_id: str, context: dict[str, Any]) -> dict[str, Any]:
    next_action = build_next_action(case_id, context)
    state = _derive_review_state(context, next_action)
    blocked_reasons = _blocked_reasons(context, next_action, state)
    return PersonalAlphaCaseOSReviewState(
        case_id=case_id,
        review_state=state,
        review_state_label=state_label(state),
        current_stage=str(next_action.get("current_stage", state)),
        next_action=str(next_action.get("next_action", "resolve_blockers" if state == "blocked" else "create_workspace_run")),
        target_route=str(next_action.get("target_route", "/case-os")),
        blocked=bool(blocked_reasons) or state == "blocked",
        blocked_reasons=blocked_reasons,
        terminal=is_terminal_state(state),
        completed_metadata_review=state == "completed_metadata_review",
        state_source="derived_from_case_os_metadata",
        mock_or_redacted_only=True,
        raw_content_included=False,
        final_legal_opinion_generated=False,
        final_report_generated=False,
        warnings=["Review state is metadata-only and does not represent a formal legal opinion."],
    ).model_dump()


def build_review_state_transitions(case_id: str, context: dict[str, Any]) -> dict[str, Any]:
    state_payload = build_review_state(case_id, context)
    current_state = str(state_payload.get("review_state", "blocked"))
    terminal = current_state in TERMINAL_STATES
    available: list[PersonalAlphaCaseOSReviewStateTransition] = []
    blocked: list[PersonalAlphaCaseOSReviewStateTransition] = []
    if terminal:
        blocked = [
            _transition_payload(rule, False, "Terminal review states do not expose executable transitions in v6.3.")
            for rule in RULES_BY_FROM.get(current_state, [])
        ]
    else:
        for rule in RULES_BY_FROM.get(current_state, []):
            available.append(_transition_payload(rule, True, rule.reason))
        if not available:
            blocked.append(
                PersonalAlphaCaseOSReviewStateTransition(
                    transition=f"{current_state}_to_blocked",
                    from_state=current_state,
                    to_state="blocked",
                    allowed=False,
                    reason="No metadata transition is currently available from this review state.",
                    target_action="resolve_blockers",
                    target_route="/case-os",
                    required_confirmations=[],
                    mock_or_redacted_only=True,
                    raw_content_included=False,
                )
            )
    return PersonalAlphaCaseOSReviewStateTransitions(
        case_id=case_id,
        current_state=current_state,
        available_transitions=available,
        blocked_transitions=blocked,
        terminal=terminal,
        mock_or_redacted_only=True,
        raw_content_included=False,
        warnings=["Available transitions are preview-only and do not execute workflow actions."],
    ).model_dump()


def build_review_state_summary(case_id: str, context: dict[str, Any]) -> dict[str, Any]:
    state_payload = build_review_state(case_id, context)
    history_payload = build_review_state_history(case_id, context)
    transitions_payload = build_review_state_transitions(case_id, context)
    summary = PersonalAlphaCaseOSReviewStateSummaryStats(
        review_state=str(state_payload.get("review_state", "blocked")),
        terminal=bool(state_payload.get("terminal", False)),
        completed_metadata_review=bool(state_payload.get("completed_metadata_review", False)),
        blocked=bool(state_payload.get("blocked", False)),
        history_count=int(history_payload.get("history_count", 0)),
        available_transition_count=len(transitions_payload.get("available_transitions", [])),
        blocked_transition_count=len(transitions_payload.get("blocked_transitions", [])),
        next_action=str(state_payload.get("next_action", "resolve_blockers")),
        target_route=state_payload.get("target_route"),
        requires_manual_review=True,
        requires_lawyer_review=True,
    )
    return PersonalAlphaCaseOSReviewStateSummary(
        case_id=case_id,
        summary=summary,
        mock_or_redacted_only=True,
        raw_content_included=False,
        final_legal_opinion_generated=False,
        final_report_generated=False,
        warnings=["Review state summary is metadata-only and advisory."],
    ).model_dump()


def validate_case_review_transition(case_id: str, from_state: str, to_state: str) -> dict[str, Any]:
    return validate_review_transition(case_id, from_state, to_state)


def _derive_review_state(context: dict[str, Any], next_action: dict[str, Any]) -> str:
    if context.get("blocked") or next_action.get("blocked"):
        latest_lawyer_action = str(context.get("latest_lawyer_action") or "")
        if latest_lawyer_action == "request_packet_revision":
            return "lawyer_review_revision_requested"
        return "blocked"
    if context.get("latest_lock_id"):
        return "completed_metadata_review"
    latest_lawyer_action = str(context.get("latest_lawyer_action") or "")
    if latest_lawyer_action == "approve_packet":
        return "final_lock_pending"
    if latest_lawyer_action == "request_packet_revision":
        return "lawyer_review_revision_requested"
    if latest_lawyer_action == "reject_packet":
        return "blocked"
    if context.get("latest_packet_id"):
        return "lawyer_final_review_pending"
    if context.get("gate_decisions", []):
        return "final_packet_pending"
    if context.get("source_decisions", []):
        return "final_gate_pending"
    if context.get("latest_workspace_run_id"):
        return "source_decision_pending"
    return "intake_ready"


def _blocked_reasons(context: dict[str, Any], next_action: dict[str, Any], state: str) -> list[str]:
    reasons = [str(item) for item in context.get("blocked_reasons", []) if item]
    reasons.extend(str(item) for item in next_action.get("blocked_reasons", []) if item)
    if state == "blocked" and not reasons:
        reasons.append("Review state is blocked by current metadata.")
    return list(dict.fromkeys(reasons))


def _transition_payload(rule: ReviewTransitionRule, allowed: bool, reason: str) -> PersonalAlphaCaseOSReviewStateTransition:
    return PersonalAlphaCaseOSReviewStateTransition(
        transition=rule.transition,
        from_state=rule.from_state,
        to_state=rule.to_state,
        allowed=allowed,
        reason=reason,
        target_action=rule.target_action,
        target_route=rule.target_route,
        required_confirmations=list(rule.required_confirmations),
        mock_or_redacted_only=True,
        raw_content_included=False,
    )
