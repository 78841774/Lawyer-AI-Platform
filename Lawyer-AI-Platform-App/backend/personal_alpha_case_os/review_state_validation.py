from typing import Any

from personal_alpha_case_os.audit_redaction import unsafe_reason
from personal_alpha_case_os.review_state_rules import RULE_BY_PAIR, transition_name
from personal_alpha_case_os.schemas import PersonalAlphaCaseOSReviewStateTransitionValidation


def validate_review_transition(case_id: str, from_state: str, to_state: str) -> dict[str, Any]:
    unsafe_fields = []
    if unsafe_reason(from_state):
        unsafe_fields.append("from_state")
    if unsafe_reason(to_state):
        unsafe_fields.append("to_state")
    if unsafe_fields:
        return PersonalAlphaCaseOSReviewStateTransitionValidation(
            case_id=case_id,
            from_state="",
            to_state="",
            transition="",
            allowed=False,
            valid_transition=False,
            would_execute_action=False,
            blocked_reasons=[f"{field} contains unsafe raw content or path-like value." for field in unsafe_fields],
            mock_or_redacted_only=True,
            raw_content_included=False,
            warnings=["v6.3 validates transitions only. It does not execute workflow actions."],
        ).model_dump()

    rule = RULE_BY_PAIR.get((from_state, to_state))
    if not rule:
        return PersonalAlphaCaseOSReviewStateTransitionValidation(
            case_id=case_id,
            from_state=from_state,
            to_state=to_state,
            transition=transition_name(from_state, to_state),
            allowed=False,
            valid_transition=False,
            would_execute_action=False,
            target_action=None,
            target_route=None,
            blocked_reasons=["Transition is not allowed by v6.3 review state rules."],
            required_confirmations=[],
            mock_or_redacted_only=True,
            raw_content_included=False,
            warnings=["v6.3 validates transitions only. It does not execute workflow actions."],
        ).model_dump()

    return PersonalAlphaCaseOSReviewStateTransitionValidation(
        case_id=case_id,
        from_state=from_state,
        to_state=to_state,
        transition=rule.transition,
        allowed=True,
        valid_transition=True,
        would_execute_action=False,
        target_action=rule.target_action,
        target_route=rule.target_route,
        blocked_reasons=[],
        required_confirmations=list(rule.required_confirmations),
        mock_or_redacted_only=True,
        raw_content_included=False,
        warnings=["v6.3 validates transitions only. It does not execute workflow actions."],
    ).model_dump()
