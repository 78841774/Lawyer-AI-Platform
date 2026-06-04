import re
from typing import Any
from uuid import uuid4

from personal_alpha_source_review.decision_storage import (
    append_source_review_decision,
    list_source_review_decisions,
)
from personal_alpha_source_review.schemas import (
    PersonalAlphaSourceReviewDecisionList,
    PersonalAlphaSourceReviewDecisionRequest,
    PersonalAlphaSourceReviewDecisionResult,
    PersonalAlphaSourceReviewDecisionSummary,
    PersonalAlphaSourceReviewDecisionSummaryResponse,
)
from personal_alpha_workspace.schemas import utc_now
from personal_alpha_workspace.workspace_engine import load_personal_alpha_workspace_run

ALLOWED_DECISIONS = {"approve", "reject", "request_revision", "mark_unclear"}
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


def list_decisions_for_run(workspace_run_id: str) -> dict[str, Any]:
    decisions = list_source_review_decisions(workspace_run_id)
    return PersonalAlphaSourceReviewDecisionList(
        workspace_run_id=workspace_run_id,
        decisions=decisions,
        decision_count=len(decisions),
        mock_or_redacted_only=True,
        raw_content_included=False,
        warnings=["Decision history is advisory metadata only. No raw content is returned."],
    ).model_dump()


def submit_decision_for_run(workspace_run_id: str, request: PersonalAlphaSourceReviewDecisionRequest) -> dict[str, Any]:
    created_at = utc_now()
    decision_id = f"source_review_decision_{uuid4().hex[:12]}"
    warnings = _base_warnings()
    loaded = load_personal_alpha_workspace_run(workspace_run_id)
    if _is_not_found(loaded):
        return _blocked_result(decision_id, workspace_run_id, request, "not_found", ["Workspace run not found or not available in runtime storage."], created_at)
    if _normalize(request.decision) not in ALLOWED_DECISIONS:
        return _blocked_result(decision_id, workspace_run_id, request, "invalid_decision", ["Decision must be one of approve, reject, request_revision, mark_unclear."], created_at)
    if not request.source_ref_id.strip():
        return _blocked_result(decision_id, workspace_run_id, request, "blocked", ["source_ref_id is required."], created_at)
    if not request.manual_review_confirmed:
        return _blocked_result(decision_id, workspace_run_id, request, "blocked", ["manual_review_confirmed must be true."], created_at)
    if not request.metadata_only_confirmation:
        return _blocked_result(decision_id, workspace_run_id, request, "blocked", ["metadata_only_confirmation must be true."], created_at)
    if _contains_unsafe_payload(request):
        return _blocked_result(decision_id, workspace_run_id, request, "blocked", ["Decision payload contains unsafe raw content or path-like value."], created_at)

    record = PersonalAlphaSourceReviewDecisionResult(
        decision_id=decision_id,
        workspace_run_id=workspace_run_id,
        source_ref_id=request.source_ref_id,
        decision=_normalize(request.decision),
        reviewer_id=request.reviewer_id or "local_demo_reviewer",
        reason=request.reason,
        status="decision_recorded",
        mock_or_redacted_only=True,
        raw_content_included=False,
        final_legal_opinion_generated=False,
        manual_review_confirmed=True,
        metadata_only_confirmation=True,
        warnings=warnings,
        created_at=created_at,
    ).model_dump()
    append_source_review_decision(workspace_run_id, record)
    return record


def get_decision_summary_for_run(workspace_run_id: str) -> dict[str, Any]:
    loaded = load_personal_alpha_workspace_run(workspace_run_id)
    not_found = _is_not_found(loaded)
    decisions = [] if not_found else list_source_review_decisions(workspace_run_id)
    approved_count = _count(decisions, "approve")
    rejected_count = _count(decisions, "reject")
    revision_requested_count = _count(decisions, "request_revision")
    unclear_count = _count(decisions, "mark_unclear")
    latest_decision_at = str(decisions[-1].get("created_at", "")) if decisions else None
    has_blocking_decision = bool(rejected_count or revision_requested_count or unclear_count)
    ready_for_next_stage = approved_count > 0 and not has_blocking_decision
    warnings = ["Decision summary is advisory metadata only. No final legal opinion is generated."]
    if not_found:
        warnings.append("Workspace run not found or not available in runtime storage.")
    return PersonalAlphaSourceReviewDecisionSummaryResponse(
        workspace_run_id=workspace_run_id,
        summary=PersonalAlphaSourceReviewDecisionSummary(
            total_decisions=len(decisions),
            approved_count=approved_count,
            rejected_count=rejected_count,
            revision_requested_count=revision_requested_count,
            unclear_count=unclear_count,
            latest_decision_at=latest_decision_at,
            ready_for_next_stage=ready_for_next_stage,
            requires_additional_review=not ready_for_next_stage,
        ).model_dump(),
        mock_or_redacted_only=True,
        raw_content_included=False,
        final_legal_opinion_generated=False,
        warnings=warnings,
    ).model_dump()


def _blocked_result(decision_id: str, workspace_run_id: str, request: PersonalAlphaSourceReviewDecisionRequest, status: str, warnings: list[str], created_at: str) -> dict[str, Any]:
    return PersonalAlphaSourceReviewDecisionResult(
        decision_id=decision_id,
        workspace_run_id=workspace_run_id,
        source_ref_id=_safe_response_value(request.source_ref_id),
        decision=_safe_response_value(request.decision),
        reviewer_id=_safe_response_value(request.reviewer_id or "local_demo_reviewer"),
        reason="",
        status=status,
        mock_or_redacted_only=True,
        raw_content_included=False,
        final_legal_opinion_generated=False,
        manual_review_confirmed=request.manual_review_confirmed,
        metadata_only_confirmation=request.metadata_only_confirmation,
        warnings=warnings,
        created_at=created_at,
    ).model_dump()


def _base_warnings() -> list[str]:
    return [
        "Decision is advisory metadata only.",
        "No raw material text, raw OCR text, or raw legal search result text is stored.",
        "No final legal opinion is generated.",
    ]


def _contains_unsafe_payload(request: PersonalAlphaSourceReviewDecisionRequest) -> bool:
    values = [request.source_ref_id, request.reviewer_id, request.reason, request.decision]
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


def _count(decisions: list[dict[str, Any]], decision: str) -> int:
    return sum(1 for item in decisions if str(item.get("decision", "")).lower() == decision)


def _is_not_found(loaded: dict[str, Any]) -> bool:
    warnings = " ".join(str(item).lower() for item in loaded.get("warnings", []))
    return "not found" in warnings and not loaded.get("source_refs") and not loaded.get("stage_statuses")


def _normalize(value: str | None) -> str:
    return (value or "").strip().lower()
