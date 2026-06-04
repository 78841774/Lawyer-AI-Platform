import re
from typing import Any
from uuid import uuid4

from personal_alpha_final_gate.gate_engine import (
    get_personal_alpha_final_gate_run,
    list_gate_decisions_for_run,
)
from personal_alpha_final_packet.packet_storage import (
    get_final_packet_record,
    list_final_packet_records,
    list_final_packet_records_for_run,
    store_final_packet_record,
)
from personal_alpha_final_packet.schemas import (
    PersonalAlphaFinalPacketCreateRequest,
    PersonalAlphaFinalPacketCreateResult,
    PersonalAlphaFinalPacketList,
    PersonalAlphaFinalPacketPreview,
    PersonalAlphaFinalPacketRecord,
    PersonalAlphaFinalPacketSafetyChecklist,
    PersonalAlphaFinalPacketSection,
    PersonalAlphaFinalPacketStatus,
)
from personal_alpha_final_readiness.readiness_engine import get_personal_alpha_final_readiness_run
from personal_alpha_source_review.decision_engine import (
    get_decision_summary_for_run,
    list_decisions_for_run as list_source_review_decisions_for_run,
)
from personal_alpha_source_review.source_review_engine import (
    get_personal_alpha_evidence_summary,
    get_personal_alpha_source_traces,
)
from personal_alpha_workspace.schemas import utc_now
from personal_alpha_workspace.workspace_engine import load_personal_alpha_workspace_run

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


def get_personal_alpha_final_packet_status() -> dict[str, Any]:
    return PersonalAlphaFinalPacketStatus(
        warnings=[
            "v5.7 final review packet is metadata-only.",
            "No final legal opinion is generated.",
            "No final report body is generated.",
            "No real provider is called.",
        ]
    ).model_dump()


def get_personal_alpha_final_packet_preview(workspace_run_id: str) -> dict[str, Any]:
    return _build_preview(workspace_run_id).model_dump()


def create_personal_alpha_final_packet(workspace_run_id: str, request: PersonalAlphaFinalPacketCreateRequest) -> dict[str, Any]:
    created_at = utc_now()
    packet_id = f"final_review_packet_{uuid4().hex[:12]}"
    confirmations_missing = _missing_confirmations(request)
    if confirmations_missing:
        return _blocked_create_result(packet_id, workspace_run_id, request, confirmations_missing, created_at)
    if _contains_unsafe_payload(workspace_run_id, request):
        return _blocked_create_result(
            packet_id,
            workspace_run_id,
            request,
            ["Final review packet payload contains unsafe raw content or path-like value."],
            created_at,
        )

    preview = _build_preview(workspace_run_id)
    if not preview.can_create_packet:
        return _blocked_create_result(
            packet_id,
            workspace_run_id,
            request,
            preview.warnings or ["Final gate must be approved before packet creation."],
            created_at,
        )

    packet = dict(preview.packet_preview)
    record = PersonalAlphaFinalPacketRecord(
        packet_id=packet_id,
        workspace_run_id=workspace_run_id,
        status="packet_created",
        can_proceed_to_controlled_final_review=True,
        packet=packet,
        reviewer_id=request.reviewer_id or "local_demo_reviewer",
        safety_checklist=PersonalAlphaFinalPacketSafetyChecklist().model_dump(),
        manual_review_confirmed=True,
        metadata_only_confirmation=True,
        no_final_legal_opinion_confirmation=True,
        no_final_report_generation_confirmation=True,
        warnings=[
            "Final review packet is metadata-only.",
            "No raw material, OCR, legal search text, final legal opinion, or final report body is included.",
        ],
        created_at=created_at,
    ).model_dump()
    storage = store_final_packet_record(record)
    warnings = list(dict.fromkeys([*record.get("warnings", []), *storage.get("warnings", [])]))
    return PersonalAlphaFinalPacketCreateResult(
        packet_id=packet_id,
        workspace_run_id=workspace_run_id,
        status="packet_created",
        can_proceed_to_controlled_final_review=True,
        packet=packet,
        reviewer_id=request.reviewer_id or "local_demo_reviewer",
        manual_review_confirmed=True,
        metadata_only_confirmation=True,
        no_final_legal_opinion_confirmation=True,
        no_final_report_generation_confirmation=True,
        warnings=warnings,
        created_at=created_at,
    ).model_dump()


def list_personal_alpha_final_packets() -> dict[str, Any]:
    packets = [_list_item(record) for record in list_final_packet_records()]
    return PersonalAlphaFinalPacketList(
        packets=packets,
        packet_count=len(packets),
        mock_or_redacted_only=True,
        raw_content_included=False,
        warnings=["Final review packet list contains metadata-only records from ignored runtime storage."],
    ).model_dump()


def get_personal_alpha_final_packet(packet_id: str) -> dict[str, Any]:
    if _looks_unsafe(packet_id):
        return _safe_packet_not_found("")
    record = get_final_packet_record(packet_id)
    if not record:
        return _safe_packet_not_found(packet_id)
    return record


def list_personal_alpha_final_packets_for_run(workspace_run_id: str) -> dict[str, Any]:
    if _looks_unsafe(workspace_run_id):
        return PersonalAlphaFinalPacketList(
            packets=[],
            packet_count=0,
            warnings=["workspace_run_id contains unsafe raw content or path-like value."],
        ).model_dump()
    packets = [_list_item(record) for record in list_final_packet_records_for_run(workspace_run_id)]
    return PersonalAlphaFinalPacketList(
        packets=packets,
        packet_count=len(packets),
        mock_or_redacted_only=True,
        raw_content_included=False,
        warnings=["Run packet list contains metadata-only records from ignored runtime storage."],
    ).model_dump()


def _build_preview(workspace_run_id: str) -> PersonalAlphaFinalPacketPreview:
    created_at = utc_now()
    if _looks_unsafe(workspace_run_id):
        return _preview_result(
            "",
            "blocked",
            {},
            False,
            ["workspace_run_id contains unsafe raw content or path-like value."],
            created_at,
        )

    workspace_run = load_personal_alpha_workspace_run(workspace_run_id)
    if _is_workspace_not_found(workspace_run):
        return _preview_result(
            workspace_run_id,
            "not_found",
            {},
            False,
            ["Workspace run not found or not available in runtime storage."],
            created_at,
        )

    gate = get_personal_alpha_final_gate_run(workspace_run_id)
    gate_summary = gate.get("gate_summary", {}) if isinstance(gate.get("gate_summary", {}), dict) else {}
    can_create = bool(gate_summary.get("can_proceed_to_controlled_final_review", False)) and str(gate_summary.get("latest_gate_decision", "")) == "approve_gate"
    readiness = get_personal_alpha_final_readiness_run(workspace_run_id)
    source_decision_summary = get_decision_summary_for_run(workspace_run_id).get("summary", {})
    source_decisions = list_source_review_decisions_for_run(workspace_run_id).get("decisions", [])
    gate_decisions = list_gate_decisions_for_run(workspace_run_id).get("decisions", [])
    source_trace_summary = get_personal_alpha_evidence_summary(workspace_run_id).get("evidence_summary", {})
    source_traces = get_personal_alpha_source_traces(workspace_run_id).get("source_traces", [])
    packet_preview = _packet_preview(
        workspace_run,
        readiness,
        source_decision_summary,
        source_decisions,
        source_trace_summary,
        source_traces,
        gate_summary,
        gate_decisions,
    )
    warnings = [
        "Final review packet preview is metadata-only.",
        "No packet record is created until the create API is called.",
    ]
    status = "mock_packet_preview_ready"
    if not can_create:
        status = "blocked_by_final_gate"
        warnings.append("Final gate must have latest approve_gate before packet creation.")
    return _preview_result(workspace_run_id, status, packet_preview, can_create, warnings, created_at)


def _packet_preview(
    workspace_run: dict[str, Any],
    readiness: dict[str, Any],
    source_decision_summary: dict[str, Any],
    source_decisions: list[dict[str, Any]],
    source_trace_summary: dict[str, Any],
    source_traces: list[dict[str, Any]],
    gate_summary: dict[str, Any],
    gate_decisions: list[dict[str, Any]],
) -> dict[str, Any]:
    return {
        "title": "Personal Alpha Controlled Final Review Packet",
        "case_id": _safe_value(str(workspace_run.get("case_id", ""))),
        "workspace_id": _safe_value(str(workspace_run.get("workspace_id", ""))),
        "workflow_mode": str(workspace_run.get("workflow_mode", "")),
        "packet_sections": [
            _section("run_summary", "Run Summary", [_run_summary(workspace_run)]),
            _section("stage_readiness", "Stage Readiness", _safe_stage_items(readiness)),
            _section(
                "source_review_decisions",
                "Source Review Decisions",
                [
                    _safe_metadata(source_decision_summary),
                    {
                        "source_trace_count": len(source_traces),
                        "evidence_summary": _safe_metadata(source_trace_summary),
                        "decisions": _safe_decisions(source_decisions, "source_review"),
                    },
                ],
            ),
            _section(
                "final_gate_decisions",
                "Final Gate Decisions",
                [
                    _safe_metadata(gate_summary),
                    {"decisions": _safe_decisions(gate_decisions, "final_gate")},
                ],
            ),
            _section("safety_checklist", "Safety Checklist", [PersonalAlphaFinalPacketSafetyChecklist().model_dump()]),
        ],
        "mock_or_redacted_only": True,
        "raw_content_included": False,
        "final_legal_opinion_generated": False,
        "final_report_generated": False,
    }


def _preview_result(workspace_run_id: str, status: str, packet_preview: dict[str, Any], can_create: bool, warnings: list[str], created_at: str) -> PersonalAlphaFinalPacketPreview:
    return PersonalAlphaFinalPacketPreview(
        workspace_run_id=_safe_value(workspace_run_id),
        status=status,
        packet_preview=packet_preview,
        can_create_packet=can_create,
        requires_final_gate_approval=True,
        mock_or_redacted_only=True,
        raw_content_included=False,
        final_legal_opinion_generated=False,
        final_report_generated=False,
        warnings=list(dict.fromkeys(warnings)),
        created_at=created_at,
    )


def _blocked_create_result(packet_id: str, workspace_run_id: str, request: PersonalAlphaFinalPacketCreateRequest, warnings: list[str], created_at: str) -> dict[str, Any]:
    return PersonalAlphaFinalPacketCreateResult(
        packet_id="",
        workspace_run_id=_safe_value(workspace_run_id),
        status="blocked",
        can_proceed_to_controlled_final_review=False,
        packet={},
        reviewer_id=_safe_value(request.reviewer_id or "local_demo_reviewer"),
        manual_review_confirmed=bool(request.manual_review_confirmed),
        metadata_only_confirmation=bool(request.metadata_only_confirmation),
        no_final_legal_opinion_confirmation=bool(request.no_final_legal_opinion_confirmation),
        no_final_report_generation_confirmation=bool(request.no_final_report_generation_confirmation),
        warnings=list(dict.fromkeys(warnings)),
        created_at=created_at,
    ).model_dump()


def _safe_packet_not_found(packet_id: str) -> dict[str, Any]:
    return {
        "packet_id": _safe_value(packet_id),
        "workspace_run_id": "",
        "status": "not_found",
        "can_proceed_to_controlled_final_review": False,
        "packet": {},
        "reviewer_id": "",
        "safety_checklist": PersonalAlphaFinalPacketSafetyChecklist().model_dump(),
        "mock_or_redacted_only": True,
        "raw_content_included": False,
        "final_legal_opinion_generated": False,
        "final_report_generated": False,
        "manual_review_confirmed": False,
        "metadata_only_confirmation": False,
        "no_final_legal_opinion_confirmation": False,
        "no_final_report_generation_confirmation": False,
        "warnings": ["Final review packet not found."],
        "created_at": "",
    }


def _section(section_id: str, title: str, items: list[dict[str, Any]]) -> dict[str, Any]:
    return PersonalAlphaFinalPacketSection(
        section_id=section_id,
        title=title,
        status="metadata_ready",
        mock_or_redacted_only=True,
        raw_content_included=False,
        items=items,
    ).model_dump()


def _run_summary(workspace_run: dict[str, Any]) -> dict[str, Any]:
    return {
        "workspace_run_id": _safe_value(str(workspace_run.get("workspace_run_id", ""))),
        "case_id": _safe_value(str(workspace_run.get("case_id", ""))),
        "workspace_id": _safe_value(str(workspace_run.get("workspace_id", ""))),
        "workflow_mode": str(workspace_run.get("workflow_mode", "")),
        "stage_count": len(_safe_list(workspace_run.get("stage_statuses", []))),
        "source_ref_count": len(_safe_list(workspace_run.get("source_refs", []))),
        "audit_event_count": len(_safe_list(workspace_run.get("unified_audit_timeline", []))),
        "mock_or_redacted_only": True,
        "raw_content_included": False,
    }


def _safe_stage_items(readiness: dict[str, Any]) -> list[dict[str, Any]]:
    items = []
    for stage in _safe_list(readiness.get("stages", [])):
        if not isinstance(stage, dict):
            continue
        items.append(
            {
                "stage_id": _safe_value(str(stage.get("stage_id", ""))),
                "label": str(stage.get("label", "")),
                "required": bool(stage.get("required", True)),
                "latest_decision": str(stage.get("latest_decision", "")),
                "stage_ready": bool(stage.get("stage_ready", False)),
                "blocked": bool(stage.get("blocked", False)),
                "requires_additional_review": bool(stage.get("requires_additional_review", False)),
                "mock_or_redacted_only": True,
                "raw_content_included": False,
            }
        )
    return items


def _safe_decisions(decisions: list[dict[str, Any]], source: str) -> list[dict[str, Any]]:
    safe = []
    for item in decisions:
        if not isinstance(item, dict):
            continue
        safe.append(
            {
                "decision_source": source,
                "decision_id": _safe_value(str(item.get("decision_id", item.get("gate_decision_id", "")))),
                "source_ref_id": _safe_value(str(item.get("source_ref_id", ""))),
                "decision": str(item.get("decision", "")).lower(),
                "status": str(item.get("status", "")),
                "can_proceed_to_controlled_final_review": bool(item.get("can_proceed_to_controlled_final_review", False)),
                "created_at": str(item.get("created_at", "")),
                "mock_or_redacted_only": True,
                "raw_content_included": False,
                "final_legal_opinion_generated": False,
                "final_report_generated": False,
            }
        )
    return safe


def _safe_metadata(value: dict[str, Any]) -> dict[str, Any]:
    safe: dict[str, Any] = {}
    for key, item in value.items():
        if key in {"reason", "quote", "text", "raw_text", "raw_content", "summary_text"}:
            continue
        if isinstance(item, (str, int, float, bool)) or item is None:
            safe[key] = _safe_value(item) if isinstance(item, str) else item
        elif isinstance(item, list):
            safe[key] = len(item)
        elif isinstance(item, dict):
            safe[key] = _safe_metadata(item)
    safe["mock_or_redacted_only"] = True
    safe["raw_content_included"] = False
    return safe


def _list_item(record: dict[str, Any]) -> dict[str, Any]:
    return {
        "packet_id": str(record.get("packet_id", "")),
        "workspace_run_id": str(record.get("workspace_run_id", "")),
        "status": str(record.get("status", "")),
        "can_proceed_to_controlled_final_review": bool(record.get("can_proceed_to_controlled_final_review", False)),
        "reviewer_id": str(record.get("reviewer_id", "")),
        "mock_or_redacted_only": True,
        "raw_content_included": False,
        "final_legal_opinion_generated": False,
        "final_report_generated": False,
        "created_at": str(record.get("created_at", "")),
    }


def _missing_confirmations(request: PersonalAlphaFinalPacketCreateRequest) -> list[str]:
    warnings = []
    if not request.manual_review_confirmed:
        warnings.append("manual_review_confirmed must be true.")
    if not request.metadata_only_confirmation:
        warnings.append("metadata_only_confirmation must be true.")
    if not request.no_final_legal_opinion_confirmation:
        warnings.append("no_final_legal_opinion_confirmation must be true.")
    if not request.no_final_report_generation_confirmation:
        warnings.append("no_final_report_generation_confirmation must be true.")
    return warnings


def _contains_unsafe_payload(workspace_run_id: str, request: PersonalAlphaFinalPacketCreateRequest) -> bool:
    return any(_looks_unsafe(str(value or "")) for value in [workspace_run_id, request.reviewer_id])


def _is_workspace_not_found(loaded: dict[str, Any]) -> bool:
    warnings = " ".join(str(item).lower() for item in loaded.get("warnings", []))
    return "not found" in warnings and not loaded.get("stage_statuses")


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


def _safe_list(value: Any) -> list[Any]:
    return value if isinstance(value, list) else []
