from typing import Any

from personal_alpha_case_os.schemas import (
    PersonalAlphaCaseOSBlockers,
    PersonalAlphaCaseOSStageBlocker,
    PersonalAlphaCaseOSStageOrchestration,
    PersonalAlphaCaseOSStageState,
    PersonalAlphaCaseOSStageTransition,
    PersonalAlphaCaseOSStageTransitions,
)
from personal_alpha_case_os.stage_eligibility import build_action_eligibility
from personal_alpha_case_os.stage_routes import route_for_stage

STAGE_ORDER = [
    "workspace_run",
    "source_review",
    "source_review_decision",
    "final_readiness",
    "final_gate",
    "final_packet",
    "lawyer_final_review",
    "final_lock",
]

STAGE_LABELS = {
    "workspace_run": "Workspace Run",
    "source_review": "Source Review",
    "source_review_decision": "Source Review Decision",
    "final_readiness": "Final Readiness",
    "final_gate": "Final Gate",
    "final_packet": "Final Packet",
    "lawyer_final_review": "Lawyer Final Review",
    "final_lock": "Final Lock",
}

NEXT_ACTION_STAGE = {
    "create_workspace_run": "workspace_run",
    "review_sources": "source_review",
    "submit_source_review_decision": "source_review_decision",
    "check_final_readiness": "final_readiness",
    "submit_final_gate_decision": "final_gate",
    "create_final_packet": "final_packet",
    "submit_lawyer_final_review": "lawyer_final_review",
    "create_final_lock": "final_lock",
    "view_completed_metadata_review": "final_lock",
}


def build_stage_orchestration(case_id: str, context: dict[str, Any], next_action: dict[str, Any]) -> dict[str, Any]:
    action_eligibility = build_action_eligibility(case_id, context, next_action)
    stages = build_orchestrated_stages(case_id, context, next_action)
    blockers = build_blockers(case_id, context, next_action)
    return PersonalAlphaCaseOSStageOrchestration(
        case_id=case_id,
        current_stage=str(next_action.get("current_stage", "workspace_run_pending")),
        next_action=str(next_action.get("next_action", "create_workspace_run")),
        next_action_label=str(next_action.get("next_action_label", "Create Workspace Run")),
        target_route=str(next_action.get("target_route", "/personal-alpha-workspace")),
        blocked=bool(blockers.get("blocked", False)),
        blocked_reasons=[str(item) for item in blockers.get("blocked_reasons", [])],
        stage_order=STAGE_ORDER,
        stages=stages,
        action_eligibility=action_eligibility,
        mock_or_redacted_only=True,
        raw_content_included=False,
        final_legal_opinion_generated=False,
        final_report_generated=False,
        warnings=["Stage orchestration is metadata-only, preview-only, and advisory."],
    ).model_dump()


def build_stage_transitions(case_id: str, context: dict[str, Any], next_action: dict[str, Any]) -> dict[str, Any]:
    stages = {stage.stage_id: stage for stage in build_orchestrated_stages(case_id, context, next_action)}
    stage_blockers = {item.stage_id: item for item in _stage_blocker_items(context, next_action)}
    transitions = []
    for index, from_stage in enumerate(STAGE_ORDER[:-1]):
        to_stage = STAGE_ORDER[index + 1]
        from_state = stages[from_stage]
        to_state = stages[to_stage]
        blocker = stage_blockers[to_stage]
        if blocker.blocked:
            status = "blocked"
            allowed = False
            reason = blocker.blocked_reasons[0] if blocker.blocked_reasons else "Stage is blocked."
        elif from_state.ready and to_state.ready:
            status = "completed"
            allowed = True
            reason = f"{STAGE_LABELS[from_stage]} metadata exists."
        elif to_state.next_action == next_action.get("next_action"):
            status = "available"
            allowed = True
            reason = _transition_reason(to_stage)
        else:
            status = "pending"
            allowed = False
            reason = f"{STAGE_LABELS[to_stage]} is waiting for prior metadata."
        transitions.append(
            PersonalAlphaCaseOSStageTransition(
                from_stage=from_stage,
                to_stage=to_stage,
                transition_status=status,
                allowed=allowed,
                reason=reason,
                mock_or_redacted_only=True,
                raw_content_included=False,
            )
        )
    return PersonalAlphaCaseOSStageTransitions(
        case_id=case_id,
        transitions=transitions,
        current_stage=str(next_action.get("current_stage", "workspace_run_pending")),
        next_action=str(next_action.get("next_action", "create_workspace_run")),
        mock_or_redacted_only=True,
        raw_content_included=False,
        warnings=["Stage transitions are preview-only and do not execute workflow actions."],
    ).model_dump()


def build_blockers(case_id: str, context: dict[str, Any], next_action: dict[str, Any]) -> dict[str, Any]:
    stage_blockers = _stage_blocker_items(context, next_action)
    blocked_reasons = [reason for item in stage_blockers for reason in item.blocked_reasons]
    blocked_reasons.extend(str(item) for item in next_action.get("blocked_reasons", []) if item)
    unique_reasons = list(dict.fromkeys(blocked_reasons))
    return PersonalAlphaCaseOSBlockers(
        case_id=case_id,
        blocked=bool(unique_reasons),
        blocked_reasons=unique_reasons,
        stage_blockers=stage_blockers,
        mock_or_redacted_only=True,
        raw_content_included=False,
        warnings=["Blocker summary uses metadata only and does not include raw source content."],
    ).model_dump()


def build_orchestrated_stages(case_id: str, context: dict[str, Any], next_action: dict[str, Any]) -> list[PersonalAlphaCaseOSStageState]:
    readiness = _readiness(context)
    blockers = {item.stage_id: item for item in _stage_blocker_items(context, next_action)}
    next_stage = NEXT_ACTION_STAGE.get(str(next_action.get("next_action", "")), "")
    metadata = {
        "case_id": case_id,
        "workspace_run_id": str(context.get("latest_workspace_run_id") or ""),
    }
    stages = []
    for stage_id in STAGE_ORDER:
        ready = readiness[stage_id]
        blocker = blockers[stage_id]
        status = "metadata_ready" if ready else "pending"
        if blocker.blocked:
            status = "blocked"
        action = str(next_action.get("next_action", "")) if stage_id == next_stage and not ready and not blocker.blocked else None
        stages.append(
            PersonalAlphaCaseOSStageState(
                stage_id=stage_id,
                label=STAGE_LABELS[stage_id],
                status=status,
                ready=ready,
                blocked=blocker.blocked,
                required=True,
                next_action=action,
                target_route=route_for_stage(stage_id, metadata),
                target_id=_target_id_for_stage(stage_id, context),
                mock_or_redacted_only=True,
                raw_content_included=False,
            )
        )
    return stages


def _readiness(context: dict[str, Any]) -> dict[str, bool]:
    has_run = bool(context.get("latest_workspace_run_id"))
    has_source_decisions = bool(context.get("source_decisions", []))
    has_gate_decisions = bool(context.get("gate_decisions", []))
    has_packet = bool(context.get("latest_packet_id"))
    has_lawyer_action = bool(context.get("lawyer_actions", []))
    has_lock = bool(context.get("latest_lock_id"))
    return {
        "workspace_run": has_run,
        "source_review": has_run,
        "source_review_decision": has_source_decisions,
        "final_readiness": has_source_decisions,
        "final_gate": has_gate_decisions,
        "final_packet": has_packet,
        "lawyer_final_review": has_lawyer_action,
        "final_lock": has_lock,
    }


def _stage_blocker_items(context: dict[str, Any], next_action: dict[str, Any]) -> list[PersonalAlphaCaseOSStageBlocker]:
    blocked_reasons = {stage_id: [] for stage_id in STAGE_ORDER}
    latest_lawyer_action = str(context.get("latest_lawyer_action") or "")
    if context.get("blocked"):
        reason = "Case context is blocked by prior metadata checks."
        for stage_id in STAGE_ORDER:
            blocked_reasons[stage_id].append(reason)
    if latest_lawyer_action in {"request_packet_revision", "reject_packet"}:
        blocked_reasons["final_lock"].append("Latest lawyer final review action blocks final lock.")
    if next_action.get("next_action") == "resolve_blockers":
        for reason in next_action.get("blocked_reasons", []):
            blocked_reasons["final_lock"].append(str(reason))
    return [
        PersonalAlphaCaseOSStageBlocker(
            stage_id=stage_id,
            blocked=bool(reasons),
            blocked_reasons=list(dict.fromkeys(reasons)),
            mock_or_redacted_only=True,
            raw_content_included=False,
        )
        for stage_id, reasons in blocked_reasons.items()
    ]


def _target_id_for_stage(stage_id: str, context: dict[str, Any]) -> str | None:
    if stage_id in {"lawyer_final_review", "final_lock"}:
        return context.get("latest_packet_id") or None
    return context.get("latest_workspace_run_id") or None


def _transition_reason(to_stage: str) -> str:
    if to_stage == "final_lock":
        return "Latest lawyer final review action is approve_packet."
    return f"{STAGE_LABELS[to_stage]} action is available from current metadata."
