import json
import re
from pathlib import Path
from typing import Any

from personal_alpha_case_os.audit_engine import build_case_os_audit_timeline
from personal_alpha_case_os.next_action_engine import build_next_action
from personal_alpha_case_os.schemas import (
    PersonalAlphaCaseOSCaseDetail,
    PersonalAlphaCaseOSCaseListItem,
    PersonalAlphaCaseOSProfile,
    PersonalAlphaCaseOSSafetyChecklist,
    PersonalAlphaCaseOSStatus,
)
from personal_alpha_case_os.stage_eligibility import build_action_eligibility
from personal_alpha_case_os.stage_orchestrator import (
    build_blockers,
    build_stage_orchestration,
    build_stage_transitions,
)
from personal_alpha_case_os.state_machine import build_stage_summary
from personal_alpha_case_os.audit_filters import available_filters_payload
from personal_alpha_case_os.review_state_history import build_review_state_history
from personal_alpha_case_os.review_state_machine import (
    build_review_state,
    build_review_state_summary,
    build_review_state_transitions,
    validate_case_review_transition,
)
from personal_alpha_case_os.unified_audit_engine import (
    build_unified_audit_summary,
    build_unified_audit_timeline,
    build_unified_redaction_check,
    legacy_audit_timeline_from_unified,
)
from personal_alpha_final_gate.gate_storage import list_final_gate_decisions
from personal_alpha_final_lock.lock_storage import list_final_lock_records
from personal_alpha_final_packet.packet_storage import list_final_packet_records
from personal_alpha_lawyer_final_review.review_storage import list_all_lawyer_final_review_actions
from personal_alpha_source_review.decision_storage import list_source_review_decisions
from personal_alpha_workspace.schemas import utc_now

REPO_ROOT = Path("/Users/wazhen/Lawyer-AI-Platform")
WORKSPACE_RUNTIME_DIR = REPO_ROOT / "storage/runtime/personal_alpha_workspace"
AGGREGATED_VERSIONS = [
    "v5.0-personal-alpha-workspace",
    "v5.1-personal-alpha-dashboard",
    "v5.2-personal-alpha-run-detail",
    "v5.3-personal-alpha-source-review",
    "v5.4-personal-alpha-source-review-decision",
    "v5.5-personal-alpha-final-readiness",
    "v5.6-personal-alpha-final-gate",
    "v5.7-personal-alpha-final-packet",
    "v5.8-personal-alpha-lawyer-final-review",
    "v5.9-personal-alpha-final-lock",
]
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


def get_personal_alpha_case_os_status() -> dict[str, Any]:
    return PersonalAlphaCaseOSStatus(
        aggregated_versions=AGGREGATED_VERSIONS,
        warnings=[
            "v6.0 Case OS is a metadata-only personal alpha view.",
            "No final legal opinion is generated.",
            "No final report body is generated.",
            "No real provider is called.",
        ],
    ).model_dump()


def list_personal_alpha_case_os_cases() -> list[dict[str, Any]]:
    contexts = _case_contexts()
    if not contexts:
        contexts = [_demo_context()]
    return [_case_list_item(context).model_dump() for context in contexts]


def get_personal_alpha_case_os_case_detail(case_id: str) -> dict[str, Any]:
    if _looks_unsafe(case_id):
        return _not_found("")
    context = _context_for_case(case_id)
    if not context:
        return _not_found(case_id)
    next_action = build_next_action(case_id, context)
    stage_summary = build_stage_summary(context, next_action)
    audit_timeline = build_case_os_audit_timeline(case_id, context)
    return PersonalAlphaCaseOSCaseDetail(
        case_id=_safe_value(case_id),
        title=_case_title(case_id),
        workspace_id=str(context.get("workspace_id", "")),
        current_stage=str(next_action.get("current_stage", "workspace_run_pending")),
        blocked=bool(next_action.get("blocked", False)),
        blocked_reasons=[str(item) for item in next_action.get("blocked_reasons", [])],
        next_action=str(next_action.get("next_action", "create_workspace_run")),
        profile=_profile(case_id).model_dump(),
        workspace_runs=_safe_workspace_runs(context.get("workspace_runs", [])),
        stage_summary=stage_summary,
        source_review=_source_review_summary(context),
        source_review_decision=_decision_counts(context.get("source_decisions", []), "source_review"),
        final_readiness=_simple_stage_payload(context, "final_readiness"),
        final_gate=_decision_counts(context.get("gate_decisions", []), "final_gate"),
        final_packet=_packet_summary(context),
        lawyer_final_review=_lawyer_review_summary(context),
        final_lock=_lock_summary(context),
        audit_timeline=audit_timeline.get("timeline", []),
        safety_checklist=PersonalAlphaCaseOSSafetyChecklist().model_dump(),
        mock_or_redacted_only=True,
        raw_content_included=False,
        final_legal_opinion_generated=False,
        final_report_generated=False,
        warnings=["Case OS detail is metadata-only and advisory. No raw content is returned."],
    ).model_dump()


def get_personal_alpha_case_os_audit_timeline(case_id: str) -> dict[str, Any]:
    context = _safe_audit_context(case_id)
    return legacy_audit_timeline_from_unified(_safe_value(case_id), context)


def get_personal_alpha_case_os_next_action(case_id: str) -> dict[str, Any]:
    context = _context_for_case(case_id)
    if not context or _looks_unsafe(case_id):
        return build_next_action(_safe_value(case_id), {"blocked": True, "blocked_reasons": ["Case not found."]})
    return build_next_action(case_id, context)


def get_personal_alpha_case_os_safety_checklist(case_id: str) -> dict[str, Any]:
    if _looks_unsafe(case_id):
        safe_case_id = ""
        warnings = ["case_id contains unsafe raw content or path-like value."]
    elif not _context_for_case(case_id):
        safe_case_id = _safe_value(case_id)
        warnings = ["Case not found."]
    else:
        safe_case_id = case_id
        warnings = ["Case OS safety checklist is metadata-only."]
    return {
        "case_id": safe_case_id,
        "safety_checklist": PersonalAlphaCaseOSSafetyChecklist().model_dump(),
        "mock_or_redacted_only": True,
        "raw_content_included": False,
        "warnings": warnings,
    }


def get_personal_alpha_case_os_stage_orchestration(case_id: str) -> dict[str, Any]:
    context, next_action = _safe_orchestration_context(case_id)
    return build_stage_orchestration(_safe_value(case_id), context, next_action)


def get_personal_alpha_case_os_stage_transitions(case_id: str) -> dict[str, Any]:
    context, next_action = _safe_orchestration_context(case_id)
    return build_stage_transitions(_safe_value(case_id), context, next_action)


def get_personal_alpha_case_os_action_eligibility(case_id: str) -> dict[str, Any]:
    context, next_action = _safe_orchestration_context(case_id)
    return build_action_eligibility(_safe_value(case_id), context, next_action)


def get_personal_alpha_case_os_blockers(case_id: str) -> dict[str, Any]:
    context, next_action = _safe_orchestration_context(case_id)
    return build_blockers(_safe_value(case_id), context, next_action)


def get_personal_alpha_case_os_unified_audit_timeline(
    case_id: str,
    stage_id: str | None = None,
    event_type: str | None = None,
    result: str | None = None,
    safety_status: str | None = None,
    limit: int | None = None,
    offset: int | None = None,
) -> dict[str, Any]:
    context = _safe_audit_context(case_id)
    return build_unified_audit_timeline(
        _safe_value(case_id),
        context,
        stage_id=stage_id,
        event_type=event_type,
        result=result,
        safety_status=safety_status,
        limit=limit,
        offset=offset,
    )


def get_personal_alpha_case_os_audit_timeline_summary(case_id: str) -> dict[str, Any]:
    context = _safe_audit_context(case_id)
    return build_unified_audit_summary(_safe_value(case_id), context)


def get_personal_alpha_case_os_audit_timeline_redaction_check(case_id: str) -> dict[str, Any]:
    context = _safe_audit_context(case_id)
    return build_unified_redaction_check(_safe_value(case_id), context)


def get_personal_alpha_case_os_audit_timeline_filters(case_id: str) -> dict[str, Any]:
    if _looks_unsafe(case_id):
        return available_filters_payload("", ["case_id contains unsafe raw content or path-like value."])
    warnings = [] if _context_for_case(case_id) else ["Case not found."]
    return available_filters_payload(_safe_value(case_id), warnings)


def get_personal_alpha_case_os_review_state(case_id: str) -> dict[str, Any]:
    context = _safe_audit_context(case_id)
    return build_review_state(_safe_value(case_id), context)


def get_personal_alpha_case_os_review_state_history(case_id: str) -> dict[str, Any]:
    context = _safe_audit_context(case_id)
    return build_review_state_history(_safe_value(case_id), context)


def get_personal_alpha_case_os_review_state_transitions(case_id: str) -> dict[str, Any]:
    context = _safe_audit_context(case_id)
    return build_review_state_transitions(_safe_value(case_id), context)


def get_personal_alpha_case_os_review_state_transition_validation(case_id: str, from_state: str, to_state: str) -> dict[str, Any]:
    return validate_case_review_transition(_safe_value(case_id), from_state, to_state)


def get_personal_alpha_case_os_review_state_summary(case_id: str) -> dict[str, Any]:
    context = _safe_audit_context(case_id)
    return build_review_state_summary(_safe_value(case_id), context)


def _case_contexts() -> list[dict[str, Any]]:
    workspace_runs = _load_workspace_records()
    packets = list_final_packet_records()
    locks = list_final_lock_records()
    lawyer_actions = list_all_lawyer_final_review_actions()
    contexts: dict[str, dict[str, Any]] = {}
    for run in workspace_runs:
        case_id = _safe_value(str(run.get("case_id", "")))
        if not case_id:
            continue
        context = contexts.setdefault(case_id, _empty_context(case_id))
        context["workspace_id"] = str(run.get("workspace_id", context.get("workspace_id", "")))
        context["workspace_runs"].append(run)
    for context in contexts.values():
        latest_run = _latest_by_created_at(context["workspace_runs"])
        latest_run_id = str(latest_run.get("workspace_run_id", "")) if latest_run else ""
        context["latest_workspace_run_id"] = latest_run_id
        context["source_decisions"] = list_source_review_decisions(latest_run_id) if latest_run_id else []
        context["gate_decisions"] = list_final_gate_decisions(latest_run_id) if latest_run_id else []
        context["packets"] = [packet for packet in packets if str(packet.get("workspace_run_id", "")) == latest_run_id]
        latest_packet = _latest_by_created_at(context["packets"])
        context["latest_packet_id"] = str(latest_packet.get("packet_id", "")) if latest_packet else ""
        context["lawyer_actions"] = [action for action in lawyer_actions if str(action.get("packet_id", "")) == context["latest_packet_id"]]
        latest_action = _latest_by_created_at(context["lawyer_actions"])
        context["latest_lawyer_action"] = str(latest_action.get("action", "")) if latest_action else ""
        context["locks"] = [lock for lock in locks if str(lock.get("packet_id", "")) == context["latest_packet_id"]]
        latest_lock = _latest_by_created_at(context["locks"])
        context["latest_lock_id"] = str(latest_lock.get("lock_id", "")) if latest_lock else ""
    return list(contexts.values())


def _context_for_case(case_id: str) -> dict[str, Any] | None:
    safe_case_id = _safe_value(case_id)
    if not safe_case_id:
        return None
    for context in _case_contexts():
        if str(context.get("case_id", "")) == safe_case_id:
            return context
    if safe_case_id == "case_v60_demo_001":
        return _demo_context()
    return None


def _safe_orchestration_context(case_id: str) -> tuple[dict[str, Any], dict[str, Any]]:
    safe_case_id = _safe_value(case_id)
    if _looks_unsafe(case_id):
        context = _empty_context("")
        context["blocked"] = True
        context["blocked_reasons"] = ["case_id contains unsafe raw content or path-like value."]
        return context, _blocked_next_action("", "case_id contains unsafe raw content or path-like value.")
    context = _context_for_case(case_id)
    if not context:
        context = _empty_context(safe_case_id)
        context["blocked"] = True
        context["blocked_reasons"] = ["Case not found."]
        return context, _blocked_next_action(safe_case_id, "Case not found.")
    return context, build_next_action(safe_case_id, context)


def _safe_audit_context(case_id: str) -> dict[str, Any]:
    safe_case_id = _safe_value(case_id)
    if _looks_unsafe(case_id):
        context = _empty_context("")
        context["blocked"] = True
        context["blocked_reasons"] = ["case_id contains unsafe raw content or path-like value."]
        return context
    context = _context_for_case(case_id)
    if not context:
        context = _empty_context(safe_case_id)
        context["blocked"] = True
        context["blocked_reasons"] = ["Case not found."]
        return context
    return context


def _blocked_next_action(case_id: str, reason: str) -> dict[str, Any]:
    target_route = f"/case-os/{case_id}" if case_id else "/case-os"
    return {
        "case_id": case_id,
        "current_stage": "blocked",
        "next_action": "resolve_blockers",
        "next_action_label": "Resolve Blockers",
        "target_route": target_route,
        "target_id": None,
        "blocked": True,
        "blocked_reasons": [reason],
        "mock_or_redacted_only": True,
        "raw_content_included": False,
        "warnings": [reason],
    }


def _load_workspace_records() -> list[dict[str, Any]]:
    if not WORKSPACE_RUNTIME_DIR.exists():
        return []
    records: list[dict[str, Any]] = []
    for file_path in sorted(WORKSPACE_RUNTIME_DIR.glob("*.json")):
        try:
            parsed = json.loads(file_path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError):
            continue
        if isinstance(parsed, dict):
            records.append(_safe_workspace_run(parsed))
    return records


def _safe_workspace_run(record: dict[str, Any]) -> dict[str, Any]:
    return {
        "workspace_run_id": _safe_value(str(record.get("workspace_run_id", ""))),
        "case_id": _safe_value(str(record.get("case_id", ""))),
        "workspace_id": _safe_value(str(record.get("workspace_id", ""))),
        "workflow_mode": str(record.get("workflow_mode", "")),
        "stage_statuses": _safe_stage_statuses(record.get("stage_statuses", [])),
        "unified_audit_timeline": _safe_timeline(record.get("unified_audit_timeline", [])),
        "source_refs": [],
        "created_at": str(record.get("created_at", "")),
        "mock_or_redacted_only": True,
        "raw_content_included": False,
    }


def _safe_workspace_runs(records: list[dict[str, Any]]) -> list[dict[str, Any]]:
    return [_safe_workspace_run(record) for record in records if isinstance(record, dict)]


def _safe_stage_statuses(value: Any) -> list[dict[str, Any]]:
    stages = []
    for item in value if isinstance(value, list) else []:
        if isinstance(item, dict):
            stages.append(
                {
                    "stage_id": _safe_value(str(item.get("stage_id", ""))),
                    "label": str(item.get("label", "")),
                    "status": str(item.get("status", "")),
                    "required": bool(item.get("required", True)),
                    "mock_or_redacted_only": True,
                    "raw_content_included": False,
                }
            )
    return stages


def _safe_timeline(value: Any) -> list[dict[str, Any]]:
    timeline = []
    for item in value if isinstance(value, list) else []:
        if isinstance(item, dict):
            timeline.append(
                {
                    "timeline_event_id": _safe_value(str(item.get("timeline_event_id", ""))),
                    "workspace_run_id": _safe_value(str(item.get("workspace_run_id", ""))),
                    "case_id": _safe_value(str(item.get("case_id", ""))),
                    "workspace_id": _safe_value(str(item.get("workspace_id", ""))),
                    "stage_id": _safe_value(str(item.get("stage_id", ""))),
                    "event_type": str(item.get("event_type", "metadata_stage_status")),
                    "result": str(item.get("result", "metadata_ready")),
                    "mock_or_redacted_only": True,
                    "raw_content_included": False,
                    "created_at": str(item.get("created_at", "")),
                }
            )
    return timeline


def _case_list_item(context: dict[str, Any]) -> PersonalAlphaCaseOSCaseListItem:
    case_id = str(context.get("case_id", "case_v60_demo_001"))
    action = build_next_action(case_id, context)
    return PersonalAlphaCaseOSCaseListItem(
        case_id=case_id,
        title=_case_title(case_id),
        workspace_id=str(context.get("workspace_id", "")),
        current_stage=str(action.get("current_stage", "workspace_run_pending")),
        blocked=bool(action.get("blocked", False)),
        blocked_reasons=[str(item) for item in action.get("blocked_reasons", [])],
        next_action=str(action.get("next_action", "create_workspace_run")),
        latest_workspace_run_id=context.get("latest_workspace_run_id") or None,
        latest_packet_id=context.get("latest_packet_id") or None,
        latest_lock_id=context.get("latest_lock_id") or None,
        mock_or_redacted_only=True,
        raw_content_included=False,
        updated_at=_context_updated_at(context),
    )


def _empty_context(case_id: str) -> dict[str, Any]:
    return {
        "case_id": case_id,
        "workspace_id": "",
        "workspace_runs": [],
        "source_decisions": [],
        "gate_decisions": [],
        "packets": [],
        "lawyer_actions": [],
        "locks": [],
        "latest_workspace_run_id": "",
        "latest_packet_id": "",
        "latest_lock_id": "",
        "latest_lawyer_action": "",
        "blocked": False,
        "blocked_reasons": [],
    }


def _demo_context() -> dict[str, Any]:
    context = _empty_context("case_v60_demo_001")
    context["workspace_id"] = "workspace_demo_001"
    return context


def _profile(case_id: str) -> PersonalAlphaCaseOSProfile:
    return PersonalAlphaCaseOSProfile(case_id=case_id, title=_case_title(case_id))


def _case_title(case_id: str) -> str:
    if case_id == "case_v60_demo_001":
        return "Personal Alpha Demo Case"
    suffix = case_id[-8:] if len(case_id) > 8 else case_id
    return f"Personal Alpha Case {suffix}"


def _source_review_summary(context: dict[str, Any]) -> dict[str, Any]:
    latest_run_id = str(context.get("latest_workspace_run_id", ""))
    return {
        "workspace_run_id": latest_run_id,
        "source_review_ready": bool(latest_run_id),
        "source_ref_count": sum(len(run.get("stage_statuses", [])) for run in context.get("workspace_runs", []) if isinstance(run, dict)),
        "mock_or_redacted_only": True,
        "raw_content_included": False,
    }


def _decision_counts(decisions: list[dict[str, Any]], decision_source: str) -> dict[str, Any]:
    return {
        "decision_source": decision_source,
        "decision_count": len(decisions),
        "latest_decision": str(decisions[-1].get("decision", "")) if decisions else None,
        "mock_or_redacted_only": True,
        "raw_content_included": False,
        "final_legal_opinion_generated": False,
    }


def _simple_stage_payload(context: dict[str, Any], stage_id: str) -> dict[str, Any]:
    return {
        "stage_id": stage_id,
        "workspace_run_id": str(context.get("latest_workspace_run_id", "")),
        "metadata_ready": bool(context.get("latest_workspace_run_id")),
        "mock_or_redacted_only": True,
        "raw_content_included": False,
    }


def _packet_summary(context: dict[str, Any]) -> dict[str, Any]:
    packets = context.get("packets", [])
    return {
        "packet_count": len(packets),
        "latest_packet_id": context.get("latest_packet_id") or None,
        "mock_or_redacted_only": True,
        "raw_content_included": False,
        "final_legal_opinion_generated": False,
        "final_report_generated": False,
    }


def _lawyer_review_summary(context: dict[str, Any]) -> dict[str, Any]:
    actions = context.get("lawyer_actions", [])
    return {
        "action_count": len(actions),
        "latest_action": context.get("latest_lawyer_action") or None,
        "ready_for_controlled_final_lock": context.get("latest_lawyer_action") == "approve_packet",
        "mock_or_redacted_only": True,
        "raw_content_included": False,
        "final_legal_opinion_generated": False,
        "final_report_generated": False,
    }


def _lock_summary(context: dict[str, Any]) -> dict[str, Any]:
    locks = context.get("locks", [])
    return {
        "lock_count": len(locks),
        "latest_lock_id": context.get("latest_lock_id") or None,
        "metadata_review_completed": bool(context.get("latest_lock_id")),
        "mock_or_redacted_only": True,
        "raw_content_included": False,
        "final_legal_opinion_generated": False,
        "final_report_generated": False,
    }


def _latest_by_created_at(items: list[dict[str, Any]]) -> dict[str, Any]:
    if not items:
        return {}
    return sorted(items, key=lambda item: str(item.get("created_at", "")))[-1]


def _context_updated_at(context: dict[str, Any]) -> str:
    dates = []
    for key in ["workspace_runs", "source_decisions", "gate_decisions", "packets", "lawyer_actions", "locks"]:
        for item in context.get(key, []):
            if isinstance(item, dict) and item.get("created_at"):
                dates.append(str(item.get("created_at")))
    return sorted(dates)[-1] if dates else utc_now()


def _not_found(case_id: str) -> dict[str, Any]:
    return PersonalAlphaCaseOSCaseDetail(
        case_id=_safe_value(case_id),
        title="Case OS case not found",
        workspace_id="",
        current_stage="blocked",
        blocked=True,
        blocked_reasons=["Case not found."],
        next_action="resolve_blockers",
        profile={},
        workspace_runs=[],
        stage_summary={},
        audit_timeline=[],
        safety_checklist=PersonalAlphaCaseOSSafetyChecklist().model_dump(),
        mock_or_redacted_only=True,
        raw_content_included=False,
        final_legal_opinion_generated=False,
        final_report_generated=False,
        warnings=["Case not found."],
    ).model_dump()


def _looks_unsafe(value: str) -> bool:
    lowered = value.lower()
    if any(marker.lower() in lowered for marker in SENSITIVE_MARKERS):
        return True
    return any(re.search(pattern, value, flags=re.IGNORECASE) for pattern in RAW_CONTENT_PATTERNS)


def _safe_value(value: str) -> str:
    text = str(value or "").strip()
    if _looks_unsafe(text):
        return ""
    return text
