from typing import Any

from personal_alpha_final_readiness.readiness_storage import store_final_readiness_snapshot
from personal_alpha_final_readiness.schemas import (
    PersonalAlphaFinalReadinessRunDetail,
    PersonalAlphaFinalReadinessSafetyChecklist,
    PersonalAlphaFinalReadinessStage,
    PersonalAlphaFinalReadinessStatus,
    PersonalAlphaFinalReadinessSummary,
)
from personal_alpha_source_review.decision_storage import list_source_review_decisions
from personal_alpha_workspace.workspace_engine import load_personal_alpha_workspace_run

READY_DECISIONS = {"approve", "mark_ready"}
BLOCKING_DECISIONS = {"reject", "request_revision", "mark_unclear"}


def get_personal_alpha_final_readiness_status() -> dict[str, Any]:
    return PersonalAlphaFinalReadinessStatus(
        warnings=[
            "v5.5 final review readiness is advisory metadata only.",
            "It aggregates workspace metadata, stage health, and source review decisions.",
            "No real LLM, DeepSeek live, OCR, or legal database provider is called.",
            "No raw material text, raw OCR text, raw legal search result text, or final legal opinion is returned.",
        ]
    ).model_dump()


def get_personal_alpha_final_readiness_run(workspace_run_id: str) -> dict[str, Any]:
    loaded = load_personal_alpha_workspace_run(workspace_run_id)
    if _is_not_found(loaded):
        return _not_found(workspace_run_id)

    decisions = _safe_decisions(list_source_review_decisions(workspace_run_id))
    stages = _readiness_stages(loaded, decisions)
    blocked_stages = [stage for stage in stages if bool(stage.get("blocked", False))]
    summary = _summary(workspace_run_id, stages, decisions)
    decision_metadata = _decision_metadata(decisions)
    warnings = [
        "Final review readiness is advisory metadata only.",
        "All mandatory stages require approve or mark_ready decision metadata before final readiness.",
        "Reject, request_revision, and mark_unclear decisions require additional review.",
        "No final legal opinion is generated.",
        *[str(item) for item in loaded.get("warnings", [])],
    ]
    detail = PersonalAlphaFinalReadinessRunDetail(
        workspace_run_id=str(loaded.get("workspace_run_id", workspace_run_id)),
        case_id=str(loaded.get("case_id", "")),
        workspace_id=str(loaded.get("workspace_id", "")),
        workflow_mode=str(loaded.get("workflow_mode", "")),
        status="mock_final_readiness_ready",
        mock_or_redacted_only=True,
        raw_content_included=False,
        final_legal_opinion_generated=False,
        advisory_only=True,
        summary=summary.model_dump(),
        stages=stages,
        blocked_stages=blocked_stages,
        safety_checklist=PersonalAlphaFinalReadinessSafetyChecklist().model_dump(),
        decision_metadata=decision_metadata,
        run_metadata=_run_metadata(loaded),
        warnings=list(dict.fromkeys(warnings)),
        created_at=str(loaded.get("created_at", "")),
    ).model_dump()
    storage = store_final_readiness_snapshot(workspace_run_id, detail)
    detail["runtime_storage"] = storage
    detail["warnings"] = list(dict.fromkeys([*detail["warnings"], *storage.get("warnings", [])]))
    return detail


def get_personal_alpha_final_readiness_summary(workspace_run_id: str) -> dict[str, Any]:
    detail = get_personal_alpha_final_readiness_run(workspace_run_id)
    return {
        "workspace_run_id": workspace_run_id,
        "summary": detail.get("summary", {}),
        "blocked_stages": detail.get("blocked_stages", []),
        "mock_or_redacted_only": True,
        "raw_content_included": False,
        "final_legal_opinion_generated": False,
        "advisory_only": True,
        "warnings": detail.get("warnings", []),
    }


def _not_found(workspace_run_id: str) -> dict[str, Any]:
    summary = PersonalAlphaFinalReadinessSummary(
        workspace_run_id=workspace_run_id,
        warnings=["Workspace run not found or not available in runtime storage."],
    )
    return PersonalAlphaFinalReadinessRunDetail(
        workspace_run_id=workspace_run_id,
        status="not_found",
        mock_or_redacted_only=True,
        raw_content_included=False,
        final_legal_opinion_generated=False,
        advisory_only=True,
        summary=summary.model_dump(),
        stages=[],
        blocked_stages=[],
        safety_checklist=PersonalAlphaFinalReadinessSafetyChecklist().model_dump(),
        decision_metadata=_decision_metadata([]),
        run_metadata={"workspace_run_id": workspace_run_id},
        warnings=["Workspace run not found or not available in runtime storage."],
        created_at="",
    ).model_dump()


def _readiness_stages(loaded: dict[str, Any], decisions: list[dict[str, Any]]) -> list[dict[str, Any]]:
    decisions_by_source_ref = _decisions_by_source_ref(decisions)
    stages = []
    for stage in _safe_list(loaded.get("stage_statuses", [])):
        if not isinstance(stage, dict):
            continue
        source_ref_id = str(stage.get("source_ref_id", ""))
        stage_decisions = decisions_by_source_ref.get(source_ref_id, [])
        decision_values = [str(item.get("decision", "")).lower() for item in stage_decisions]
        latest_decision = decision_values[-1] if decision_values else "pending_review"
        blocked = any(decision in BLOCKING_DECISIONS for decision in decision_values)
        ready_decision = any(decision in READY_DECISIONS for decision in decision_values)
        required = bool(stage.get("required", True))
        workspace_stage_ready = "ready" in str(stage.get("status", "")).lower()
        stage_ready = bool(workspace_stage_ready and (ready_decision or not required) and not blocked)
        stages.append(
            PersonalAlphaFinalReadinessStage(
                stage_id=str(stage.get("stage_id", "")),
                label=str(stage.get("label", "")),
                required=required,
                source_ref_id=source_ref_id,
                workspace_stage_status=str(stage.get("status", "mock_pending_reference")),
                latest_decision=latest_decision,
                decision_count=len(stage_decisions),
                stage_ready=stage_ready,
                blocked=blocked,
                requires_additional_review=required and not stage_ready,
                mock_or_redacted_only=True,
                raw_content_included=False,
                notes=_stage_notes(stage_ready, blocked, latest_decision),
            ).model_dump()
        )
    return stages


def _summary(workspace_run_id: str, stages: list[dict[str, Any]], decisions: list[dict[str, Any]]) -> PersonalAlphaFinalReadinessSummary:
    mandatory = [stage for stage in stages if bool(stage.get("required", True))]
    ready_count = sum(1 for stage in stages if bool(stage.get("stage_ready", False)))
    blocked_count = sum(1 for stage in stages if bool(stage.get("blocked", False)))
    pending_count = sum(1 for stage in mandatory if not bool(stage.get("stage_ready", False)) and not bool(stage.get("blocked", False)))
    stage_ready = bool(mandatory) and all(bool(stage.get("stage_ready", False)) for stage in mandatory)
    requires_additional_review = not stage_ready or blocked_count > 0
    return PersonalAlphaFinalReadinessSummary(
        workspace_run_id=workspace_run_id,
        total_stages=len(stages),
        mandatory_stage_count=len(mandatory),
        ready_stage_count=ready_count,
        blocked_stage_count=blocked_count,
        pending_stage_count=pending_count,
        decision_count=len(decisions),
        approved_decision_count=_count(decisions, "approve") + _count(decisions, "mark_ready"),
        rejected_decision_count=_count(decisions, "reject"),
        revision_requested_count=_count(decisions, "request_revision"),
        unclear_decision_count=_count(decisions, "mark_unclear"),
        stage_ready=stage_ready,
        requires_additional_review=requires_additional_review,
        final_review_ready=stage_ready and not requires_additional_review,
        final_legal_opinion_generated=False,
        mock_or_redacted_only=True,
        raw_content_included=False,
        warnings=["Readiness summary is metadata-only and advisory. It is not a final legal opinion."],
    )


def _decision_metadata(decisions: list[dict[str, Any]]) -> dict[str, Any]:
    return {
        "decision_count": len(decisions),
        "approved_decision_count": _count(decisions, "approve") + _count(decisions, "mark_ready"),
        "rejected_decision_count": _count(decisions, "reject"),
        "revision_requested_count": _count(decisions, "request_revision"),
        "unclear_decision_count": _count(decisions, "mark_unclear"),
        "mock_or_redacted_only": True,
        "raw_content_included": False,
        "advisory_only": True,
    }


def _run_metadata(loaded: dict[str, Any]) -> dict[str, Any]:
    return {
        "workspace_run_id": str(loaded.get("workspace_run_id", "")),
        "case_id": str(loaded.get("case_id", "")),
        "workspace_id": str(loaded.get("workspace_id", "")),
        "workflow_mode": str(loaded.get("workflow_mode", "")),
        "stage_count": len(_safe_list(loaded.get("stage_statuses", []))),
        "source_ref_count": len(_safe_list(loaded.get("source_refs", []))),
        "audit_event_count": len(_safe_list(loaded.get("unified_audit_timeline", []))),
        "mock_or_redacted_only": True,
        "raw_content_included": False,
    }


def _decisions_by_source_ref(decisions: list[dict[str, Any]]) -> dict[str, list[dict[str, Any]]]:
    grouped: dict[str, list[dict[str, Any]]] = {}
    for decision in decisions:
        grouped.setdefault(str(decision.get("source_ref_id", "")), []).append(decision)
    return grouped


def _safe_decisions(decisions: list[dict[str, Any]]) -> list[dict[str, Any]]:
    safe = []
    for item in decisions:
        if not isinstance(item, dict) or str(item.get("status", "")) != "decision_recorded":
            continue
        safe.append(
            {
                "decision_id": str(item.get("decision_id", "")),
                "workspace_run_id": str(item.get("workspace_run_id", "")),
                "source_ref_id": str(item.get("source_ref_id", "")),
                "decision": str(item.get("decision", "")).lower(),
                "created_at": str(item.get("created_at", "")),
                "mock_or_redacted_only": True,
                "raw_content_included": False,
                "final_legal_opinion_generated": False,
            }
        )
    return safe


def _stage_notes(stage_ready: bool, blocked: bool, latest_decision: str) -> str:
    if blocked:
        return "Blocked by source review decision metadata. Additional review required."
    if stage_ready:
        return "Ready for final review readiness checklist. Advisory metadata only."
    if latest_decision == "pending_review":
        return "Pending source review decision metadata."
    return "Additional review required before final readiness."


def _count(decisions: list[dict[str, Any]], decision: str) -> int:
    return sum(1 for item in decisions if str(item.get("decision", "")).lower() == decision)


def _is_not_found(loaded: dict[str, Any]) -> bool:
    warnings = " ".join(str(item).lower() for item in loaded.get("warnings", []))
    return "not found" in warnings and not loaded.get("stage_statuses")


def _safe_list(value: Any) -> list[Any]:
    return value if isinstance(value, list) else []
