from typing import Any

from personal_alpha_case_os.schemas import PersonalAlphaCaseOSStageState

STAGE_DEFINITIONS = [
    ("workspace", "Workspace Run", "/personal-alpha-workspace"),
    ("source_review", "Source Review", "/personal-alpha-source-review"),
    ("source_review_decision", "Source Review Decision", "/personal-alpha-source-review"),
    ("final_readiness", "Final Readiness", "/personal-alpha-final-readiness"),
    ("final_gate", "Final Gate", "/personal-alpha-final-gate"),
    ("final_packet", "Final Packet", "/personal-alpha-final-packet"),
    ("lawyer_final_review", "Lawyer Final Review", "/personal-alpha-lawyer-final-review"),
    ("final_lock", "Final Lock", "/personal-alpha-final-lock"),
]


def build_stage_summary(context: dict[str, Any], next_action: dict[str, Any]) -> dict[str, Any]:
    latest_run_id = str(context.get("latest_workspace_run_id") or "")
    latest_packet_id = str(context.get("latest_packet_id") or "")
    latest_lock_id = str(context.get("latest_lock_id") or "")
    has_run = bool(latest_run_id)
    has_source_decisions = bool(context.get("source_decisions", []))
    has_gate_decisions = bool(context.get("gate_decisions", []))
    has_packet = bool(latest_packet_id)
    has_lawyer_action = bool(context.get("lawyer_actions", []))
    has_lock = bool(latest_lock_id)
    latest_lawyer_action = str(context.get("latest_lawyer_action") or "")
    states = {
        "workspace": _stage("workspace", "Workspace Run", "metadata_ready" if has_run else "pending", "create_workspace_run" if not has_run else None, "/personal-alpha-workspace", latest_run_id or None),
        "source_review": _stage("source_review", "Source Review", "metadata_ready" if has_run else "pending", "review_sources" if has_run and not has_source_decisions else None, "/personal-alpha-source-review", latest_run_id or None),
        "source_review_decision": _stage("source_review_decision", "Source Review Decision", "metadata_ready" if has_source_decisions else "pending", "submit_source_review_decision" if has_run and not has_source_decisions else None, "/personal-alpha-source-review", latest_run_id or None),
        "final_readiness": _stage("final_readiness", "Final Readiness", "metadata_ready" if has_source_decisions else "pending", "check_final_readiness" if has_source_decisions else None, "/personal-alpha-final-readiness", latest_run_id or None),
        "final_gate": _stage("final_gate", "Final Gate", "metadata_ready" if has_gate_decisions else "pending", "submit_final_gate_decision" if has_source_decisions and not has_gate_decisions else None, "/personal-alpha-final-gate", latest_run_id or None),
        "final_packet": _stage("final_packet", "Final Packet", "metadata_ready" if has_packet else "pending", "create_final_packet" if has_gate_decisions and not has_packet else None, "/personal-alpha-final-packet", latest_run_id or None),
        "lawyer_final_review": _stage("lawyer_final_review", "Lawyer Final Review", "metadata_ready" if has_lawyer_action else "pending", "submit_lawyer_final_review" if has_packet and not has_lawyer_action else None, "/personal-alpha-lawyer-final-review", latest_packet_id or None),
        "final_lock": _stage("final_lock", "Final Lock", "metadata_ready" if has_lock else "pending", "create_final_lock" if latest_lawyer_action == "approve_packet" and not has_lock else None, "/personal-alpha-final-lock", latest_packet_id or None),
    }
    current_stage = str(next_action.get("current_stage", "workspace_run_pending"))
    for stage_id, state in states.items():
        if state.get("next_action") == next_action.get("next_action") or stage_id in current_stage:
            state["status"] = "pending" if state["status"] != "metadata_ready" else state["status"]
    return states


def derive_next_action(context: dict[str, Any]) -> dict[str, Any]:
    if context.get("blocked"):
        return _next("blocked", "resolve_blockers", "Resolve Blockers", "#", None, True, context.get("blocked_reasons", []))
    latest_run_id = context.get("latest_workspace_run_id")
    latest_packet_id = context.get("latest_packet_id")
    latest_lock_id = context.get("latest_lock_id")
    source_decisions = context.get("source_decisions", [])
    gate_decisions = context.get("gate_decisions", [])
    lawyer_actions = context.get("lawyer_actions", [])
    latest_lawyer_action = context.get("latest_lawyer_action")
    if latest_lock_id:
        return _next("completed_metadata_review", "view_completed_metadata_review", "View Completed Metadata Review", "/personal-alpha-final-lock", latest_lock_id)
    if latest_lawyer_action == "approve_packet" and latest_packet_id:
        return _next("final_lock_pending", "create_final_lock", "Create Controlled Final Lock", "/personal-alpha-final-lock", latest_packet_id)
    if latest_lawyer_action in {"request_packet_revision", "reject_packet"}:
        return _next("blocked", "resolve_blockers", "Resolve Lawyer Review Blockers", "/personal-alpha-lawyer-final-review", latest_packet_id, True, ["Latest lawyer final review action blocks final lock."])
    if latest_packet_id and not lawyer_actions:
        return _next("lawyer_final_review_pending", "submit_lawyer_final_review", "Submit Lawyer Final Review", "/personal-alpha-lawyer-final-review", latest_packet_id)
    if gate_decisions and not latest_packet_id:
        return _next("final_packet_pending", "create_final_packet", "Create Final Review Packet", "/personal-alpha-final-packet", latest_run_id)
    if source_decisions and not gate_decisions:
        return _next("final_gate_pending", "submit_final_gate_decision", "Submit Final Gate Decision", "/personal-alpha-final-gate", latest_run_id)
    if latest_run_id and not source_decisions:
        return _next("source_decision_pending", "submit_source_review_decision", "Submit Source Review Decision", "/personal-alpha-source-review", latest_run_id)
    if latest_run_id:
        return _next("final_readiness_pending", "check_final_readiness", "Check Final Readiness", "/personal-alpha-final-readiness", latest_run_id)
    return _next("workspace_run_pending", "create_workspace_run", "Create Workspace Run", "/personal-alpha-workspace", None)


def _stage(stage_id: str, label: str, status: str, next_action: str | None, target_route: str, target_id: str | None) -> dict[str, Any]:
    return PersonalAlphaCaseOSStageState(
        stage_id=stage_id,
        label=label,
        status=status,
        next_action=next_action,
        target_route=target_route,
        target_id=target_id,
        mock_or_redacted_only=True,
        raw_content_included=False,
    ).model_dump()


def _next(current_stage: str, next_action: str, label: str, route: str, target_id: str | None, blocked: bool = False, blocked_reasons: list[str] | None = None) -> dict[str, Any]:
    return {
        "current_stage": current_stage,
        "next_action": next_action,
        "next_action_label": label,
        "target_route": route,
        "target_id": target_id,
        "blocked": blocked,
        "blocked_reasons": blocked_reasons or [],
        "mock_or_redacted_only": True,
        "raw_content_included": False,
        "warnings": ["Case OS next action is metadata-only and advisory."],
    }
