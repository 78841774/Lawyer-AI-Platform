from typing import Any

from personal_alpha_case_os.schemas import (
    PersonalAlphaCaseOSActionEligibility,
    PersonalAlphaCaseOSActionEligibilityItem,
)
from personal_alpha_case_os.stage_routes import route_for_action

ACTION_DEFINITIONS = [
    (
        "create_workspace_run",
        "Create Workspace Run",
        ["explicit_workspace_confirmation", "manual_review_confirmed"],
        ["no existing workspace run metadata for this case"],
    ),
    (
        "review_sources",
        "Review Source Metadata",
        ["manual_review_confirmed", "metadata_only_confirmation"],
        ["latest workspace run metadata must exist"],
    ),
    (
        "submit_source_review_decision",
        "Submit Source Review Decision",
        ["manual_review_confirmed", "metadata_only_confirmation"],
        ["latest workspace run metadata must exist"],
    ),
    (
        "check_final_readiness",
        "Check Final Readiness",
        ["manual_review_confirmed", "metadata_only_confirmation"],
        ["source review decision metadata must exist"],
    ),
    (
        "submit_final_gate_decision",
        "Submit Final Gate Decision",
        ["manual_review_confirmed", "lawyer_review_confirmed", "metadata_only_confirmation"],
        ["source review decision metadata must exist"],
    ),
    (
        "create_final_packet",
        "Create Final Review Packet",
        ["manual_review_confirmed", "lawyer_review_confirmed", "metadata_only_confirmation"],
        ["final gate decision metadata must exist"],
    ),
    (
        "submit_lawyer_final_review",
        "Submit Lawyer Final Review",
        ["manual_review_confirmed", "lawyer_review_confirmed", "metadata_only_confirmation"],
        ["final packet metadata must exist"],
    ),
    (
        "create_final_lock",
        "Create Controlled Final Lock",
        [
            "manual_review_confirmed",
            "lawyer_review_confirmed",
            "metadata_only_confirmation",
            "no_final_legal_opinion_confirmation",
            "no_final_report_generation_confirmation",
        ],
        [
            "latest lawyer final review action must be approve_packet",
            "metadata only confirmations required",
        ],
    ),
]


def build_action_eligibility(case_id: str, context: dict[str, Any], next_action: dict[str, Any]) -> dict[str, Any]:
    blocked = bool(next_action.get("blocked", False))
    current_action = str(next_action.get("next_action", "create_workspace_run"))
    metadata = {
        "case_id": case_id,
        "workspace_run_id": str(context.get("latest_workspace_run_id") or ""),
    }
    items = [
        _eligibility_item(action, label, confirmations, requires, context, current_action, blocked, metadata)
        for action, label, confirmations, requires in ACTION_DEFINITIONS
    ]
    selected = next((item for item in items if item.action == current_action), None)
    return PersonalAlphaCaseOSActionEligibility(
        case_id=case_id,
        actions=items,
        action=selected.action if selected else current_action,
        eligible=bool(selected.eligible) if selected else False,
        requires=list(selected.requires) if selected else [],
        blocked_reasons=list(selected.blocked_reasons) if selected else ["Action is not available for the current stage."],
        current_stage=str(next_action.get("current_stage", "workspace_run_pending")),
        next_action=current_action,
        mock_or_redacted_only=True,
        raw_content_included=False,
        warnings=["Action eligibility is metadata-only, preview-only, and requires manual lawyer review."],
    ).model_dump()


def _eligibility_item(
    action: str,
    label: str,
    confirmations: list[str],
    requires: list[str],
    context: dict[str, Any],
    current_action: str,
    globally_blocked: bool,
    metadata: dict[str, Any],
) -> PersonalAlphaCaseOSActionEligibilityItem:
    reasons = _action_blockers(action, context)
    if globally_blocked and action == current_action:
        reasons.extend(str(item) for item in context.get("blocked_reasons", []) if item)
    if action != current_action and not reasons:
        reasons.append("Action is not the current Case OS next action.")
    return PersonalAlphaCaseOSActionEligibilityItem(
        action=action,
        label=label,
        eligible=action == current_action and not reasons and not globally_blocked,
        target_route=route_for_action(action, metadata),
        blocked_reasons=reasons,
        required_confirmations=confirmations,
        requires=requires,
        mock_or_redacted_only=True,
        raw_content_included=False,
    )


def _action_blockers(action: str, context: dict[str, Any]) -> list[str]:
    has_run = bool(context.get("latest_workspace_run_id"))
    has_source_decision = bool(context.get("source_decisions", []))
    has_gate_decision = bool(context.get("gate_decisions", []))
    has_packet = bool(context.get("latest_packet_id"))
    latest_lawyer_action = str(context.get("latest_lawyer_action") or "")
    has_lock = bool(context.get("latest_lock_id"))

    if action == "create_workspace_run":
        return ["Workspace run already exists or current stage is later."] if has_run else []
    if action in {"review_sources", "submit_source_review_decision"}:
        return [] if has_run and not has_source_decision else ["Workspace run metadata is missing or source decision already exists."]
    if action == "check_final_readiness":
        return [] if has_source_decision else ["Source review decision metadata is missing."]
    if action == "submit_final_gate_decision":
        return [] if has_source_decision and not has_gate_decision else ["Source decision is missing or final gate decision already exists."]
    if action == "create_final_packet":
        return [] if has_gate_decision and not has_packet else ["Final gate decision is missing or final packet already exists."]
    if action == "submit_lawyer_final_review":
        return [] if has_packet and not latest_lawyer_action else ["Final packet is missing or lawyer review action already exists."]
    if action == "create_final_lock":
        if has_lock:
            return ["Controlled final lock metadata already exists."]
        if latest_lawyer_action != "approve_packet":
            return ["Latest lawyer final review action must be approve_packet."]
        return []
    return ["Action is not recognized by the Case OS stage orchestrator."]
