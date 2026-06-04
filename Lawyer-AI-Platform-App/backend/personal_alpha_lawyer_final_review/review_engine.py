import re
from typing import Any
from uuid import uuid4

from personal_alpha_final_packet.packet_engine import get_personal_alpha_final_packet
from personal_alpha_lawyer_final_review.review_storage import (
    get_lawyer_final_review_action,
    list_lawyer_final_review_actions,
    store_lawyer_final_review_action,
)
from personal_alpha_lawyer_final_review.schemas import (
    PersonalAlphaLawyerFinalReviewActionList,
    PersonalAlphaLawyerFinalReviewActionRecord,
    PersonalAlphaLawyerFinalReviewActionRequest,
    PersonalAlphaLawyerFinalReviewActionResult,
    PersonalAlphaLawyerFinalReviewPacketDetail,
    PersonalAlphaLawyerFinalReviewSafetyChecklist,
    PersonalAlphaLawyerFinalReviewStatus,
    PersonalAlphaLawyerFinalReviewSummary,
)
from personal_alpha_workspace.schemas import utc_now

ALLOWED_ACTIONS = {"approve_packet", "request_packet_revision", "reject_packet"}
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


def get_personal_alpha_lawyer_final_review_status() -> dict[str, Any]:
    return PersonalAlphaLawyerFinalReviewStatus(
        warnings=[
            "v5.8 lawyer final review is advisory metadata only.",
            "No final legal opinion is generated.",
            "No final report body is generated.",
            "No real provider is called.",
        ]
    ).model_dump()


def get_personal_alpha_lawyer_final_review_packet_detail(packet_id: str) -> dict[str, Any]:
    if _looks_unsafe(packet_id):
        return _packet_not_found("")
    packet = get_personal_alpha_final_packet(packet_id)
    if _is_packet_not_found(packet):
        return _packet_not_found(packet_id)

    actions = _actions_for_packet(packet_id)
    summary = _summary(actions)
    packet_summary = _packet_summary(packet)
    return PersonalAlphaLawyerFinalReviewPacketDetail(
        packet_id=str(packet.get("packet_id", packet_id)),
        workspace_run_id=str(packet.get("workspace_run_id", "")),
        status="mock_lawyer_final_review_ready",
        packet_status=str(packet.get("status", "packet_created")),
        review_status=summary.review_status,
        latest_action=summary.latest_action,
        can_submit_review_action=True,
        mock_or_redacted_only=True,
        raw_content_included=False,
        final_legal_opinion_generated=False,
        final_report_generated=False,
        packet_summary=packet_summary,
        review_actions=actions,
        safety_checklist=PersonalAlphaLawyerFinalReviewSafetyChecklist().model_dump(),
        warnings=[
            "Lawyer final review detail is advisory metadata only.",
            "No final legal opinion or final report body is generated.",
        ],
        created_at=str(packet.get("created_at", "")),
    ).model_dump()


def get_personal_alpha_lawyer_final_review_summary(packet_id: str) -> dict[str, Any]:
    if _looks_unsafe(packet_id):
        return _summary_response("", "", [], ["packet_id contains unsafe raw content or path-like value."])
    packet = get_personal_alpha_final_packet(packet_id)
    if _is_packet_not_found(packet):
        return _summary_response(packet_id, "", [], ["Final review packet not found."])
    actions = _actions_for_packet(packet_id)
    return _summary_response(packet_id, str(packet.get("workspace_run_id", "")), actions, ["Lawyer final review summary is advisory metadata only."])


def list_personal_alpha_lawyer_final_review_actions(packet_id: str) -> dict[str, Any]:
    if _looks_unsafe(packet_id):
        return PersonalAlphaLawyerFinalReviewActionList(
            packet_id="",
            actions=[],
            action_count=0,
            warnings=["packet_id contains unsafe raw content or path-like value."],
        ).model_dump()
    packet = get_personal_alpha_final_packet(packet_id)
    if _is_packet_not_found(packet):
        return PersonalAlphaLawyerFinalReviewActionList(
            packet_id=packet_id,
            actions=[],
            action_count=0,
            warnings=["Final review packet not found."],
        ).model_dump()
    actions = _actions_for_packet(packet_id)
    return PersonalAlphaLawyerFinalReviewActionList(
        packet_id=packet_id,
        actions=actions,
        action_count=len(actions),
        mock_or_redacted_only=True,
        raw_content_included=False,
        warnings=["Review action history is advisory metadata only. No raw content is returned."],
    ).model_dump()


def submit_personal_alpha_lawyer_final_review_action(packet_id: str, request: PersonalAlphaLawyerFinalReviewActionRequest) -> dict[str, Any]:
    created_at = utc_now()
    action_id = f"lawyer_final_review_action_{uuid4().hex[:12]}"
    packet = get_personal_alpha_final_packet(packet_id)
    if _looks_unsafe(packet_id) or _is_packet_not_found(packet):
        return _blocked_action_result(action_id, packet_id, "", request, "not_found", ["Final review packet not found."], created_at)
    if _normalize(request.action) not in ALLOWED_ACTIONS:
        return _blocked_action_result(action_id, packet_id, str(packet.get("workspace_run_id", "")), request, "invalid_action", ["Action must be one of approve_packet, request_packet_revision, reject_packet."], created_at)

    missing = _missing_confirmations(request)
    if missing:
        return _blocked_action_result(action_id, packet_id, str(packet.get("workspace_run_id", "")), request, "blocked", missing, created_at)
    if _contains_unsafe_payload(packet_id, action_id, request):
        return _blocked_action_result(
            action_id,
            packet_id,
            str(packet.get("workspace_run_id", "")),
            request,
            "blocked",
            ["Lawyer final review payload contains unsafe raw content or path-like value."],
            created_at,
        )

    action = _normalize(request.action)
    record = PersonalAlphaLawyerFinalReviewActionRecord(
        action_id=action_id,
        packet_id=packet_id,
        workspace_run_id=str(packet.get("workspace_run_id", "")),
        action=action,
        reviewer_id=request.reviewer_id or "local_demo_lawyer",
        reason=request.reason or "",
        status="lawyer_final_review_action_recorded",
        ready_for_controlled_final_lock=action == "approve_packet",
        manual_review_confirmed=True,
        lawyer_review_confirmed=True,
        metadata_only_confirmation=True,
        no_final_legal_opinion_confirmation=True,
        no_final_report_generation_confirmation=True,
        warnings=_record_warnings(action),
        created_at=created_at,
    ).model_dump()
    storage = store_lawyer_final_review_action(record)
    warnings = list(dict.fromkeys([*record.get("warnings", []), *storage.get("warnings", [])]))
    return PersonalAlphaLawyerFinalReviewActionResult(**{**record, "warnings": warnings}).model_dump()


def get_personal_alpha_lawyer_final_review_action(action_id: str) -> dict[str, Any]:
    if _looks_unsafe(action_id):
        return _action_not_found("")
    record = get_lawyer_final_review_action(action_id)
    if not record:
        return _action_not_found(action_id)
    return record


def _summary_response(packet_id: str, workspace_run_id: str, actions: list[dict[str, Any]], warnings: list[str]) -> dict[str, Any]:
    return {
        "packet_id": _safe_value(packet_id),
        "workspace_run_id": _safe_value(workspace_run_id),
        "summary": _summary(actions).model_dump(),
        "mock_or_redacted_only": True,
        "raw_content_included": False,
        "final_legal_opinion_generated": False,
        "final_report_generated": False,
        "warnings": list(dict.fromkeys(warnings)),
    }


def _summary(actions: list[dict[str, Any]]) -> PersonalAlphaLawyerFinalReviewSummary:
    latest = actions[-1] if actions else {}
    latest_action = str(latest.get("action", "")) or None
    review_status = "pending_lawyer_review"
    if latest_action == "approve_packet":
        review_status = "packet_approved"
    elif latest_action == "request_packet_revision":
        review_status = "packet_revision_requested"
    elif latest_action == "reject_packet":
        review_status = "packet_rejected"
    return PersonalAlphaLawyerFinalReviewSummary(
        review_status=review_status,
        action_count=len(actions),
        approved_packet_count=_count(actions, "approve_packet"),
        revision_requested_count=_count(actions, "request_packet_revision"),
        rejected_packet_count=_count(actions, "reject_packet"),
        latest_action=latest_action,
        ready_for_controlled_final_lock=latest_action == "approve_packet",
        requires_packet_revision=latest_action == "request_packet_revision",
        requires_additional_lawyer_review=latest_action != "approve_packet",
    )


def _packet_summary(packet: dict[str, Any]) -> dict[str, Any]:
    packet_data = packet.get("packet", {}) if isinstance(packet.get("packet", {}), dict) else {}
    sections = packet_data.get("packet_sections", []) if isinstance(packet_data.get("packet_sections", []), list) else []
    return {
        "packet_id": str(packet.get("packet_id", "")),
        "workspace_run_id": str(packet.get("workspace_run_id", "")),
        "packet_status": str(packet.get("status", "")),
        "title": str(packet_data.get("title", "Personal Alpha Controlled Final Review Packet")),
        "section_count": len(sections),
        "section_ids": [str(section.get("section_id", "")) for section in sections if isinstance(section, dict)],
        "reviewer_id": str(packet.get("reviewer_id", "")),
        "created_at": str(packet.get("created_at", "")),
        "mock_or_redacted_only": True,
        "raw_content_included": False,
        "final_legal_opinion_generated": False,
        "final_report_generated": False,
    }


def _actions_for_packet(packet_id: str) -> list[dict[str, Any]]:
    return [
        action
        for action in list_lawyer_final_review_actions(packet_id)
        if str(action.get("status", "")) == "lawyer_final_review_action_recorded"
    ]


def _blocked_action_result(action_id: str, packet_id: str, workspace_run_id: str, request: PersonalAlphaLawyerFinalReviewActionRequest, status: str, warnings: list[str], created_at: str) -> dict[str, Any]:
    return PersonalAlphaLawyerFinalReviewActionResult(
        action_id=action_id,
        packet_id=_safe_value(packet_id),
        workspace_run_id=_safe_value(workspace_run_id),
        action=_safe_value(request.action),
        reviewer_id=_safe_value(request.reviewer_id or "local_demo_lawyer"),
        reason="",
        status=status,
        ready_for_controlled_final_lock=False,
        mock_or_redacted_only=True,
        raw_content_included=False,
        final_legal_opinion_generated=False,
        final_report_generated=False,
        manual_review_confirmed=bool(request.manual_review_confirmed),
        lawyer_review_confirmed=bool(request.lawyer_review_confirmed),
        metadata_only_confirmation=bool(request.metadata_only_confirmation),
        no_final_legal_opinion_confirmation=bool(request.no_final_legal_opinion_confirmation),
        no_final_report_generation_confirmation=bool(request.no_final_report_generation_confirmation),
        warnings=list(dict.fromkeys(warnings)),
        created_at=created_at,
    ).model_dump()


def _packet_not_found(packet_id: str) -> dict[str, Any]:
    return PersonalAlphaLawyerFinalReviewPacketDetail(
        packet_id=_safe_value(packet_id),
        workspace_run_id="",
        status="not_found",
        packet_status="not_found",
        review_status="not_found",
        latest_action=None,
        can_submit_review_action=False,
        mock_or_redacted_only=True,
        raw_content_included=False,
        final_legal_opinion_generated=False,
        final_report_generated=False,
        packet_summary={},
        review_actions=[],
        safety_checklist=PersonalAlphaLawyerFinalReviewSafetyChecklist().model_dump(),
        warnings=["Final review packet not found."],
        created_at="",
    ).model_dump()


def _action_not_found(action_id: str) -> dict[str, Any]:
    return {
        "action_id": _safe_value(action_id),
        "packet_id": "",
        "workspace_run_id": "",
        "action": "",
        "reviewer_id": "",
        "reason": "",
        "status": "not_found",
        "ready_for_controlled_final_lock": False,
        "mock_or_redacted_only": True,
        "raw_content_included": False,
        "final_legal_opinion_generated": False,
        "final_report_generated": False,
        "manual_review_confirmed": False,
        "lawyer_review_confirmed": False,
        "metadata_only_confirmation": False,
        "no_final_legal_opinion_confirmation": False,
        "no_final_report_generation_confirmation": False,
        "warnings": ["Lawyer final review action not found."],
        "created_at": "",
    }


def _missing_confirmations(request: PersonalAlphaLawyerFinalReviewActionRequest) -> list[str]:
    warnings = []
    if not request.manual_review_confirmed:
        warnings.append("manual_review_confirmed must be true.")
    if not request.lawyer_review_confirmed:
        warnings.append("lawyer_review_confirmed must be true.")
    if not request.metadata_only_confirmation:
        warnings.append("metadata_only_confirmation must be true.")
    if not request.no_final_legal_opinion_confirmation:
        warnings.append("no_final_legal_opinion_confirmation must be true.")
    if not request.no_final_report_generation_confirmation:
        warnings.append("no_final_report_generation_confirmation must be true.")
    return warnings


def _record_warnings(action: str) -> list[str]:
    warnings = [
        "Lawyer final review action is advisory metadata only.",
        "No final legal opinion or final report body was generated.",
    ]
    if action == "request_packet_revision":
        warnings.append("Packet metadata requires revision before controlled final lock.")
    if action == "reject_packet":
        warnings.append("Packet metadata was rejected for controlled final lock.")
    return warnings


def _contains_unsafe_payload(packet_id: str, action_id: str, request: PersonalAlphaLawyerFinalReviewActionRequest) -> bool:
    values = [packet_id, action_id, request.action, request.reviewer_id, request.reason]
    return any(_looks_unsafe(str(value or "")) for value in values)


def _is_packet_not_found(packet: dict[str, Any]) -> bool:
    return str(packet.get("status", "")).lower() == "not_found" or not packet.get("packet_id")


def _count(actions: list[dict[str, Any]], action: str) -> int:
    return sum(1 for item in actions if str(item.get("action", "")).lower() == action)


def _normalize(value: str | None) -> str:
    return (value or "").strip().lower()


def _looks_unsafe(value: str) -> bool:
    lowered = value.lower()
    if any(marker.lower() in lowered for marker in SENSITIVE_MARKERS):
        return True
    return any(re.search(pattern, value, flags=re.IGNORECASE) for pattern in RAW_CONTENT_PATTERNS)


def _safe_value(value: Any) -> str:
    text = str(value or "").strip()
    if _looks_unsafe(text):
        return ""
    return text
