import re
from typing import Any
from uuid import uuid4

from personal_alpha_final_lock.lock_storage import (
    get_final_lock_record,
    list_final_lock_records,
    list_final_lock_records_for_packet,
    store_final_lock_record,
)
from personal_alpha_final_lock.schemas import (
    PersonalAlphaFinalLockCreateRequest,
    PersonalAlphaFinalLockCreateResult,
    PersonalAlphaFinalLockList,
    PersonalAlphaFinalLockReadiness,
    PersonalAlphaFinalLockReadinessRequirements,
    PersonalAlphaFinalLockRecord,
    PersonalAlphaFinalLockSafetyChecklist,
    PersonalAlphaFinalLockStatus,
)
from personal_alpha_lawyer_final_review.review_engine import (
    get_personal_alpha_lawyer_final_review_packet_detail,
    get_personal_alpha_lawyer_final_review_summary,
)
from personal_alpha_workspace.schemas import utc_now

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


def get_personal_alpha_final_lock_status() -> dict[str, Any]:
    return PersonalAlphaFinalLockStatus(
        warnings=[
            "v5.9 final lock is metadata-only.",
            "No final legal opinion is generated.",
            "No final report body is generated.",
            "No real provider is called.",
        ]
    ).model_dump()


def get_personal_alpha_final_lock_readiness(packet_id: str) -> dict[str, Any]:
    return _build_readiness(packet_id).model_dump()


def create_personal_alpha_final_lock(packet_id: str, request: PersonalAlphaFinalLockCreateRequest) -> dict[str, Any]:
    created_at = utc_now()
    lock_id = f"personal_alpha_final_lock_{uuid4().hex[:12]}"
    missing = _missing_confirmations(request)
    if missing:
        return _blocked_create_result(lock_id, packet_id, "", request, missing, created_at)
    if _contains_unsafe_payload(packet_id, lock_id, request):
        return _blocked_create_result(
            lock_id,
            packet_id,
            "",
            request,
            ["Final lock payload contains unsafe raw content or path-like value."],
            created_at,
        )

    readiness = _build_readiness(packet_id)
    if not readiness.can_create_final_lock:
        return _blocked_create_result(
            lock_id,
            packet_id,
            readiness.workspace_run_id,
            request,
            readiness.warnings or ["Latest lawyer final review action must be approve_packet before final lock creation."],
            created_at,
        )

    safety_checklist = PersonalAlphaFinalLockSafetyChecklist().model_dump()
    lock_record = {
        "lock_id": lock_id,
        "packet_id": packet_id,
        "workspace_run_id": readiness.workspace_run_id,
        "locked_metadata": {
            "packet_id": packet_id,
            "latest_lawyer_review_action": readiness.latest_lawyer_review_action,
            "safety_checklist": safety_checklist,
            "lock_type": "metadata_only_personal_alpha_final_lock",
        },
        "mock_or_redacted_only": True,
        "raw_content_included": False,
        "final_legal_opinion_generated": False,
        "final_report_generated": False,
    }
    record = PersonalAlphaFinalLockRecord(
        lock_id=lock_id,
        packet_id=packet_id,
        workspace_run_id=readiness.workspace_run_id,
        status="final_lock_created",
        reviewer_id=request.reviewer_id or "local_demo_lawyer",
        lock_record=lock_record,
        safety_checklist=safety_checklist,
        manual_review_confirmed=True,
        lawyer_review_confirmed=True,
        metadata_only_confirmation=True,
        no_final_legal_opinion_confirmation=True,
        no_final_report_generation_confirmation=True,
        warnings=[
            "Final lock is metadata-only.",
            "No raw content, final legal opinion, or final report body is included.",
        ],
        created_at=created_at,
    ).model_dump()
    storage = store_final_lock_record(record)
    warnings = list(dict.fromkeys([*record.get("warnings", []), *storage.get("warnings", [])]))
    return PersonalAlphaFinalLockCreateResult(
        lock_id=lock_id,
        packet_id=packet_id,
        workspace_run_id=readiness.workspace_run_id,
        status="final_lock_created",
        reviewer_id=request.reviewer_id or "local_demo_lawyer",
        lock_record=lock_record,
        mock_or_redacted_only=True,
        raw_content_included=False,
        final_legal_opinion_generated=False,
        final_report_generated=False,
        manual_review_confirmed=True,
        lawyer_review_confirmed=True,
        metadata_only_confirmation=True,
        no_final_legal_opinion_confirmation=True,
        no_final_report_generation_confirmation=True,
        warnings=warnings,
        created_at=created_at,
    ).model_dump()


def list_personal_alpha_final_locks() -> dict[str, Any]:
    locks = [_list_item(record) for record in list_final_lock_records()]
    return PersonalAlphaFinalLockList(
        locks=locks,
        lock_count=len(locks),
        mock_or_redacted_only=True,
        raw_content_included=False,
        warnings=["Final lock list contains metadata-only records from ignored runtime storage."],
    ).model_dump()


def get_personal_alpha_final_lock(lock_id: str) -> dict[str, Any]:
    if _looks_unsafe(lock_id):
        return _lock_not_found("")
    record = get_final_lock_record(lock_id)
    if not record:
        return _lock_not_found(lock_id)
    return record


def list_personal_alpha_final_locks_for_packet(packet_id: str) -> dict[str, Any]:
    if _looks_unsafe(packet_id):
        return PersonalAlphaFinalLockList(
            locks=[],
            lock_count=0,
            warnings=["packet_id contains unsafe raw content or path-like value."],
        ).model_dump()
    locks = [_list_item(record) for record in list_final_lock_records_for_packet(packet_id)]
    return PersonalAlphaFinalLockList(
        locks=locks,
        lock_count=len(locks),
        mock_or_redacted_only=True,
        raw_content_included=False,
        warnings=["Packet final lock list contains metadata-only records from ignored runtime storage."],
    ).model_dump()


def _build_readiness(packet_id: str) -> PersonalAlphaFinalLockReadiness:
    created_at = utc_now()
    if _looks_unsafe(packet_id):
        return _readiness_result("", "", "blocked", False, None, ["packet_id contains unsafe raw content or path-like value."], created_at)

    detail = get_personal_alpha_lawyer_final_review_packet_detail(packet_id)
    if str(detail.get("status", "")).lower() == "not_found" or not detail.get("packet_id"):
        return _readiness_result(
            packet_id,
            "",
            "not_found",
            False,
            None,
            ["Final review packet not found."],
            created_at,
        )

    summary_response = get_personal_alpha_lawyer_final_review_summary(packet_id)
    summary = summary_response.get("summary", {}) if isinstance(summary_response.get("summary", {}), dict) else {}
    latest_action = str(summary.get("latest_action", "")) or None
    can_create = bool(summary.get("ready_for_controlled_final_lock", False)) and latest_action == "approve_packet"
    warnings = [
        "Final lock readiness is advisory metadata only.",
        "No final legal opinion or final report body is generated.",
    ]
    status = "mock_final_lock_readiness_ready"
    if not can_create:
        status = "blocked_by_lawyer_final_review"
        warnings.append("Latest lawyer final review action must be approve_packet before creating a final lock.")
    return _readiness_result(
        packet_id,
        str(detail.get("workspace_run_id", "")),
        status,
        can_create,
        latest_action,
        warnings,
        created_at,
    )


def _readiness_result(packet_id: str, workspace_run_id: str, status: str, can_create: bool, latest_action: str | None, warnings: list[str], created_at: str) -> PersonalAlphaFinalLockReadiness:
    return PersonalAlphaFinalLockReadiness(
        packet_id=_safe_value(packet_id),
        workspace_run_id=_safe_value(workspace_run_id),
        status=status,
        can_create_final_lock=can_create,
        requires_lawyer_final_review_approval=True,
        latest_lawyer_review_action=latest_action,
        mock_or_redacted_only=True,
        raw_content_included=False,
        final_legal_opinion_generated=False,
        final_report_generated=False,
        readiness_requirements=PersonalAlphaFinalLockReadinessRequirements().model_dump(),
        safety_checklist=PersonalAlphaFinalLockSafetyChecklist().model_dump(),
        warnings=list(dict.fromkeys(warnings)),
        created_at=created_at,
    )


def _blocked_create_result(lock_id: str, packet_id: str, workspace_run_id: str, request: PersonalAlphaFinalLockCreateRequest, warnings: list[str], created_at: str) -> dict[str, Any]:
    return PersonalAlphaFinalLockCreateResult(
        lock_id="",
        packet_id=_safe_value(packet_id),
        workspace_run_id=_safe_value(workspace_run_id),
        status="blocked",
        reviewer_id=_safe_value(request.reviewer_id or "local_demo_lawyer"),
        lock_record={},
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


def _lock_not_found(lock_id: str) -> dict[str, Any]:
    return {
        "lock_id": _safe_value(lock_id),
        "packet_id": "",
        "workspace_run_id": "",
        "status": "not_found",
        "reviewer_id": "",
        "lock_record": {},
        "safety_checklist": PersonalAlphaFinalLockSafetyChecklist().model_dump(),
        "mock_or_redacted_only": True,
        "raw_content_included": False,
        "final_legal_opinion_generated": False,
        "final_report_generated": False,
        "manual_review_confirmed": False,
        "lawyer_review_confirmed": False,
        "metadata_only_confirmation": False,
        "no_final_legal_opinion_confirmation": False,
        "no_final_report_generation_confirmation": False,
        "warnings": ["Final lock not found."],
        "created_at": "",
    }


def _list_item(record: dict[str, Any]) -> dict[str, Any]:
    return {
        "lock_id": str(record.get("lock_id", "")),
        "packet_id": str(record.get("packet_id", "")),
        "workspace_run_id": str(record.get("workspace_run_id", "")),
        "status": str(record.get("status", "")),
        "reviewer_id": str(record.get("reviewer_id", "")),
        "mock_or_redacted_only": True,
        "raw_content_included": False,
        "final_legal_opinion_generated": False,
        "final_report_generated": False,
        "created_at": str(record.get("created_at", "")),
    }


def _missing_confirmations(request: PersonalAlphaFinalLockCreateRequest) -> list[str]:
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


def _contains_unsafe_payload(packet_id: str, lock_id: str, request: PersonalAlphaFinalLockCreateRequest) -> bool:
    values = [packet_id, lock_id, request.reviewer_id]
    return any(_looks_unsafe(str(value or "")) for value in values)


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
