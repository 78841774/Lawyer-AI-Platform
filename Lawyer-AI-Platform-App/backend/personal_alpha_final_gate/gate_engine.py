import re
from typing import Any
from uuid import uuid4

from personal_alpha_final_gate.gate_storage import (
    append_final_gate_decision,
    list_final_gate_decisions,
)
from personal_alpha_final_gate.schemas import (
    PersonalAlphaFinalGateDecisionList,
    PersonalAlphaFinalGateDecisionRequest,
    PersonalAlphaFinalGateDecisionResult,
    PersonalAlphaFinalGateDecisionRecord,
    PersonalAlphaFinalGateRequirements,
    PersonalAlphaFinalGateRunDetail,
    PersonalAlphaFinalGateSafetyChecklist,
    PersonalAlphaFinalGateStatus,
    PersonalAlphaFinalGateSummary,
)
from personal_alpha_final_readiness.readiness_engine import get_personal_alpha_final_readiness_run
from personal_alpha_workspace.schemas import utc_now

ALLOWED_GATE_DECISIONS = {"approve_gate", "block_gate", "request_more_review"}
BLOCKING_GATE_DECISIONS = {"block_gate", "request_more_review"}
SENSITIVE_MARKERS = (
    ".env",
    "local.db",
    ".db",
    "storage/runtime",
    "real_cases",
    "sandbox_cases",
    "case_workspaces",
    "Lawyer-AI-Local-Cases",
    "AIHome-Law-Local-Sandbox",
)
RAW_CONTENT_PATTERNS = (
    r"sk-[A-Za-z0-9_-]{12,}",
    r"api[_-]?key",
    r"(?<!\d)1[3-9]\d{9}(?!\d)",
    r"(?<!\d)\d{6}(?:19|20)\d{2}\d{2}\d{2}\d{3}[\dXx](?!\d)",
    r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}",
    r"[（(]\d{4}[）)][\u4e00-\u9fa5A-Za-z0-9第初终再执民商行刑破知号字\-]{4,40}号",
    r"\.(pdf|docx|xlsx|zip|png|jpg|jpeg|txt|md|json)$",
    r"[/\\]",
)


def get_personal_alpha_final_gate_status() -> dict[str, Any]:
    return PersonalAlphaFinalGateStatus(
        warnings=[
            "v5.6 final gate is advisory metadata only.",
            "No final legal opinion is generated.",
            "No real provider is called.",
        ]
    ).model_dump()


def get_personal_alpha_final_gate_run(workspace_run_id: str) -> dict[str, Any]:
    readiness = get_personal_alpha_final_readiness_run(workspace_run_id)
    if _is_not_found(readiness):
        return _not_found(workspace_run_id)
    decisions = _recorded_decisions(workspace_run_id)
    summary = _gate_summary(readiness, decisions)
    warnings = [
        "Final gate is advisory metadata only.",
        "Gate open means the run may receive a manual gate decision; it is not a final legal opinion.",
        "Controlled final review step requires the latest gate decision to be approve_gate.",
        *[str(item) for item in readiness.get("warnings", [])],
    ]
    return PersonalAlphaFinalGateRunDetail(
        workspace_run_id=str(readiness.get("workspace_run_id", workspace_run_id)),
        status="mock_final_gate_ready",
        final_review_ready=bool(summary.final_review_ready),
        gate_open=bool(summary.gate_open),
        requires_additional_review=bool(summary.requires_additional_review),
        blocked=not bool(summary.gate_open),
        can_proceed_to_controlled_final_review=bool(summary.can_proceed_to_controlled_final_review),
        mock_or_redacted_only=True,
        raw_content_included=False,
        final_legal_opinion_generated=False,
        final_report_generated=False,
        readiness_summary=dict(readiness.get("summary", {})),
        gate_requirements=PersonalAlphaFinalGateRequirements().model_dump(),
        safety_checklist=PersonalAlphaFinalGateSafetyChecklist().model_dump(),
        gate_summary=summary.model_dump(),
        warnings=list(dict.fromkeys(warnings)),
        created_at=str(readiness.get("created_at", "")),
    ).model_dump()


def get_personal_alpha_final_gate_summary(workspace_run_id: str) -> dict[str, Any]:
    detail = get_personal_alpha_final_gate_run(workspace_run_id)
    return {
        "workspace_run_id": workspace_run_id,
        "summary": detail.get("gate_summary", {}),
        "mock_or_redacted_only": True,
        "raw_content_included": False,
        "final_legal_opinion_generated": False,
        "final_report_generated": False,
        "warnings": detail.get("warnings", []),
    }


def list_gate_decisions_for_run(workspace_run_id: str) -> dict[str, Any]:
    decisions = _recorded_decisions(workspace_run_id)
    return PersonalAlphaFinalGateDecisionList(
        workspace_run_id=workspace_run_id,
        decisions=decisions,
        decision_count=len(decisions),
        mock_or_redacted_only=True,
        raw_content_included=False,
        warnings=["Final gate decision history is advisory metadata only. No raw content is returned."],
    ).model_dump()


def submit_gate_decision_for_run(workspace_run_id: str, request: PersonalAlphaFinalGateDecisionRequest) -> dict[str, Any]:
    created_at = utc_now()
    gate_decision_id = f"final_gate_decision_{uuid4().hex[:12]}"
    readiness = get_personal_alpha_final_readiness_run(workspace_run_id)
    if _is_not_found(readiness):
        return _blocked_result(gate_decision_id, workspace_run_id, request, "not_found", ["Workspace run not found or not available in runtime storage."], created_at)
    if _normalize(request.decision) not in ALLOWED_GATE_DECISIONS:
        return _blocked_result(gate_decision_id, workspace_run_id, request, "invalid_decision", ["Decision must be one of approve_gate, block_gate, request_more_review."], created_at)
    if not request.manual_review_confirmed:
        return _blocked_result(gate_decision_id, workspace_run_id, request, "blocked", ["manual_review_confirmed must be true."], created_at)
    if not request.metadata_only_confirmation:
        return _blocked_result(gate_decision_id, workspace_run_id, request, "blocked", ["metadata_only_confirmation must be true."], created_at)
    if not request.no_final_legal_opinion_confirmation:
        return _blocked_result(gate_decision_id, workspace_run_id, request, "blocked", ["no_final_legal_opinion_confirmation must be true."], created_at)
    if _contains_unsafe_payload(workspace_run_id, request):
        return _blocked_result(gate_decision_id, workspace_run_id, request, "blocked", ["Final gate payload contains unsafe raw content or path-like value."], created_at)

    prior_decisions = _recorded_decisions(workspace_run_id)
    readiness_gate_summary = _gate_summary(readiness, prior_decisions)
    if _normalize(request.decision) == "approve_gate" and not readiness_gate_summary.gate_open:
        return _blocked_result(
            gate_decision_id,
            workspace_run_id,
            request,
            "blocked",
            ["Final readiness has not passed; approve_gate cannot be recorded."],
            created_at,
        )

    provisional_decisions = [
        *prior_decisions,
        {
            "decision": _normalize(request.decision),
            "status": "gate_decision_recorded",
            "created_at": created_at,
        },
    ]
    can_proceed = _gate_summary(readiness, provisional_decisions).can_proceed_to_controlled_final_review
    record = PersonalAlphaFinalGateDecisionRecord(
        gate_decision_id=gate_decision_id,
        workspace_run_id=workspace_run_id,
        decision=_normalize(request.decision),
        reviewer_id=request.reviewer_id or "local_demo_reviewer",
        reason=request.reason,
        status="gate_decision_recorded",
        can_proceed_to_controlled_final_review=bool(can_proceed),
        mock_or_redacted_only=True,
        raw_content_included=False,
        final_legal_opinion_generated=False,
        final_report_generated=False,
        manual_review_confirmed=True,
        metadata_only_confirmation=True,
        no_final_legal_opinion_confirmation=True,
        warnings=_record_warnings(_normalize(request.decision)),
        created_at=created_at,
    ).model_dump()
    append_final_gate_decision(workspace_run_id, record)
    return record


def _not_found(workspace_run_id: str) -> dict[str, Any]:
    summary = PersonalAlphaFinalGateSummary()
    return PersonalAlphaFinalGateRunDetail(
        workspace_run_id=workspace_run_id,
        status="not_found",
        final_review_ready=False,
        gate_open=False,
        requires_additional_review=True,
        blocked=True,
        can_proceed_to_controlled_final_review=False,
        mock_or_redacted_only=True,
        raw_content_included=False,
        final_legal_opinion_generated=False,
        final_report_generated=False,
        readiness_summary={},
        gate_requirements=PersonalAlphaFinalGateRequirements().model_dump(),
        safety_checklist=PersonalAlphaFinalGateSafetyChecklist().model_dump(),
        gate_summary=summary.model_dump(),
        warnings=["Workspace run not found or not available in runtime storage."],
        created_at="",
    ).model_dump()


def _gate_summary(readiness: dict[str, Any], decisions: list[dict[str, Any]]) -> PersonalAlphaFinalGateSummary:
    readiness_summary = readiness.get("summary", {}) if isinstance(readiness.get("summary", {}), dict) else {}
    final_review_ready = bool(readiness_summary.get("final_review_ready", False))
    requires_additional_review = bool(readiness_summary.get("requires_additional_review", True))
    blocked_stage_count = int(readiness_summary.get("blocked_stage_count", 0) or 0)
    gate_open = final_review_ready and not requires_additional_review and blocked_stage_count == 0
    latest = _latest_decision(decisions)
    latest_decision = str(latest.get("decision", "")) if latest else None
    can_proceed = bool(gate_open and latest_decision == "approve_gate")
    if latest_decision in BLOCKING_GATE_DECISIONS:
        can_proceed = False
    return PersonalAlphaFinalGateSummary(
        gate_open=gate_open,
        final_review_ready=final_review_ready,
        requires_additional_review=requires_additional_review,
        latest_gate_decision=latest_decision,
        gate_decision_count=len(decisions),
        approved_gate_count=_count(decisions, "approve_gate"),
        blocked_gate_count=_count(decisions, "block_gate"),
        more_review_requested_count=_count(decisions, "request_more_review"),
        can_proceed_to_controlled_final_review=can_proceed,
    )


def _recorded_decisions(workspace_run_id: str) -> list[dict[str, Any]]:
    decisions = []
    for item in list_final_gate_decisions(workspace_run_id):
        if not isinstance(item, dict) or str(item.get("status", "")) != "gate_decision_recorded":
            continue
        decisions.append(
            {
                "gate_decision_id": str(item.get("gate_decision_id", "")),
                "workspace_run_id": str(item.get("workspace_run_id", "")),
                "decision": str(item.get("decision", "")).lower(),
                "reviewer_id": str(item.get("reviewer_id", "local_demo_reviewer")),
                "reason": str(item.get("reason", "")),
                "status": "gate_decision_recorded",
                "can_proceed_to_controlled_final_review": bool(item.get("can_proceed_to_controlled_final_review", False)),
                "mock_or_redacted_only": True,
                "raw_content_included": False,
                "final_legal_opinion_generated": False,
                "final_report_generated": False,
                "manual_review_confirmed": bool(item.get("manual_review_confirmed", True)),
                "metadata_only_confirmation": bool(item.get("metadata_only_confirmation", True)),
                "no_final_legal_opinion_confirmation": bool(item.get("no_final_legal_opinion_confirmation", True)),
                "warnings": [str(warning) for warning in item.get("warnings", []) if isinstance(warning, str)],
                "created_at": str(item.get("created_at", "")),
            }
        )
    return decisions


def _blocked_result(gate_decision_id: str, workspace_run_id: str, request: PersonalAlphaFinalGateDecisionRequest, status: str, warnings: list[str], created_at: str) -> dict[str, Any]:
    return PersonalAlphaFinalGateDecisionResult(
        gate_decision_id=gate_decision_id,
        workspace_run_id=_safe_response_value(workspace_run_id),
        decision=_safe_response_value(request.decision),
        reviewer_id=_safe_response_value(request.reviewer_id or "local_demo_reviewer"),
        reason="",
        status=status,
        can_proceed_to_controlled_final_review=False,
        mock_or_redacted_only=True,
        raw_content_included=False,
        final_legal_opinion_generated=False,
        final_report_generated=False,
        manual_review_confirmed=request.manual_review_confirmed,
        metadata_only_confirmation=request.metadata_only_confirmation,
        no_final_legal_opinion_confirmation=request.no_final_legal_opinion_confirmation,
        warnings=warnings,
        created_at=created_at,
    ).model_dump()


def _record_warnings(decision: str) -> list[str]:
    warnings = [
        "Final gate decision is advisory metadata only.",
        "No final legal opinion or final report was generated.",
    ]
    if decision in BLOCKING_GATE_DECISIONS:
        warnings.append("Controlled final review cannot proceed while the latest gate decision blocks or requests more review.")
    return warnings


def _contains_unsafe_payload(workspace_run_id: str, request: PersonalAlphaFinalGateDecisionRequest) -> bool:
    values = [workspace_run_id, request.decision, request.reviewer_id, request.reason]
    return any(_looks_unsafe(str(value or "")) for value in values)


def _looks_unsafe(value: str) -> bool:
    lowered = value.lower()
    if any(marker.lower() in lowered for marker in SENSITIVE_MARKERS):
        return True
    return any(re.search(pattern, value, flags=re.IGNORECASE) for pattern in RAW_CONTENT_PATTERNS)


def _safe_response_value(value: str | None) -> str:
    text = (value or "").strip()
    if _looks_unsafe(text):
        return ""
    return text


def _latest_decision(decisions: list[dict[str, Any]]) -> dict[str, Any] | None:
    return decisions[-1] if decisions else None


def _count(decisions: list[dict[str, Any]], decision: str) -> int:
    return sum(1 for item in decisions if str(item.get("decision", "")).lower() == decision)


def _is_not_found(readiness: dict[str, Any]) -> bool:
    status = str(readiness.get("status", "")).lower()
    warnings = " ".join(str(item).lower() for item in readiness.get("warnings", []))
    return status == "not_found" or ("not found" in warnings and not readiness.get("stages"))


def _normalize(value: str | None) -> str:
    return (value or "").strip().lower()
