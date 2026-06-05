from typing import Any
from uuid import uuid4

from personal_alpha_case_os.audit_filters import apply_audit_filters, build_filters
from personal_alpha_case_os.audit_redaction import CHECKED_FIELDS, redact_audit_events
from personal_alpha_case_os.audit_stats import build_audit_summary
from personal_alpha_case_os.schemas import (
    PersonalAlphaCaseOSAuditTimelineRedactionCheck,
    PersonalAlphaCaseOSAuditTimelineRedactionStats,
    PersonalAlphaCaseOSUnifiedAuditEvent,
    PersonalAlphaCaseOSUnifiedAuditTimeline,
    PersonalAlphaCaseOSUnsafeAuditEventSummary,
)
from personal_alpha_workspace.schemas import utc_now

WORKSPACE_STAGE_MAP = {
    "controlled_material_preview": "workspace_run",
    "controlled_ocr_preview": "workspace_run",
    "controlled_legal_search_preview": "workspace_run",
    "controlled_report_draft": "workspace_run",
    "controlled_lawyer_review": "workspace_run",
    "controlled_revision": "workspace_run",
    "controlled_final_review_lock": "workspace_run",
}


def build_unified_audit_timeline(
    case_id: str,
    context: dict[str, Any],
    *,
    stage_id: str | None = None,
    event_type: str | None = None,
    result: str | None = None,
    safety_status: str | None = None,
    limit: int | None = None,
    offset: int | None = None,
) -> dict[str, Any]:
    filters = build_filters(stage_id, event_type, result, safety_status, limit, offset)
    events, warnings = _safe_events_for_context(case_id, context)
    filtered = apply_audit_filters(events, filters)
    return PersonalAlphaCaseOSUnifiedAuditTimeline(
        case_id=case_id,
        filters=filters,
        timeline=[PersonalAlphaCaseOSUnifiedAuditEvent(**event) for event in filtered],
        event_count=len(events),
        returned_count=len(filtered),
        mock_or_redacted_only=True,
        raw_content_included=False,
        final_legal_opinion_generated=False,
        final_report_generated=False,
        warnings=warnings,
    ).model_dump()


def build_unified_audit_summary(case_id: str, context: dict[str, Any]) -> dict[str, Any]:
    events, warnings = _safe_events_for_context(case_id, context)
    return build_audit_summary(case_id, events, warnings)


def build_unified_redaction_check(case_id: str, context: dict[str, Any]) -> dict[str, Any]:
    events, warnings = _safe_events_for_context(case_id, context)
    unsafe_events = [unsafe for event in events for unsafe in event.get("_unsafe_summaries", [])]
    unique_unsafe_events = [
        PersonalAlphaCaseOSUnsafeAuditEventSummary(**item)
        for item in {f"{item['timeline_event_id']}::{item['field_name']}::{item['reason']}": item for item in unsafe_events}.values()
    ]
    stats = PersonalAlphaCaseOSAuditTimelineRedactionStats(
        passed=not unique_unsafe_events and not any(event.get("raw_content_included") for event in events),
        unsafe_event_count=len({item.timeline_event_id for item in unique_unsafe_events}),
        raw_content_event_count=sum(1 for event in events if event.get("raw_content_included")),
        path_like_value_count=sum(1 for item in unique_unsafe_events if item.reason == "path_like_value"),
        api_key_like_value_count=sum(1 for item in unique_unsafe_events if item.reason == "api_key_like_value"),
        personal_identifier_like_value_count=sum(1 for item in unique_unsafe_events if item.reason == "personal_identifier_like_value"),
        redacted_event_count=sum(1 for event in events if event.get("redacted")),
        checked_fields=CHECKED_FIELDS,
    )
    return PersonalAlphaCaseOSAuditTimelineRedactionCheck(
        case_id=case_id,
        redaction_check=stats,
        unsafe_events=unique_unsafe_events,
        mock_or_redacted_only=True,
        raw_content_included=False,
        warnings=warnings,
    ).model_dump()


def legacy_audit_timeline_from_unified(case_id: str, context: dict[str, Any]) -> dict[str, Any]:
    events, warnings = _safe_events_for_context(case_id, context)
    legacy = [
        {
            "timeline_event_id": event["timeline_event_id"],
            "case_id": event["case_id"],
            "workspace_run_id": event.get("workspace_run_id") or "",
            "stage_id": event["stage_id"],
            "event_type": event["event_type"],
            "result": event["result"],
            "mock_or_redacted_only": True,
            "raw_content_included": False,
            "created_at": event["created_at"],
        }
        for event in events
    ]
    return {
        "case_id": case_id,
        "timeline": legacy,
        "event_count": len(legacy),
        "mock_or_redacted_only": True,
        "raw_content_included": False,
        "warnings": warnings or ["Case OS audit timeline is metadata-only. No raw content is returned."],
    }


def _safe_events_for_context(case_id: str, context: dict[str, Any]) -> tuple[list[dict[str, Any]], list[str]]:
    warnings = ["Unified audit timeline is metadata-only, redacted-only, and advisory."]
    raw_events = _raw_events_for_context(case_id, context)
    events, unsafe_summaries = redact_audit_events(raw_events)
    safe_events = []
    for event in events:
        event["_unsafe_summaries"] = [
            item for item in unsafe_summaries if item["timeline_event_id"] == event.get("timeline_event_id")
        ]
        safe_events.append(event)
    safe_events.sort(key=lambda event: str(event.get("created_at", "")))
    return safe_events, warnings


def _raw_events_for_context(case_id: str, context: dict[str, Any]) -> list[dict[str, Any]]:
    if context.get("blocked"):
        reason = "blocked_unsafe_input" if not case_id else "safe_not_found"
        event_type = "blocked" if not case_id else "not_found"
        result = "blocked" if not case_id else "safe_not_found"
        return [
            _event(
                case_id=case_id,
                stage_id="case_os",
                module="personal_alpha_case_os",
                event_type=event_type,
                result=result,
                safety_status=reason,
                action="resolve_blockers",
                target_id=case_id or None,
                message="Case OS audit timeline request was safely blocked or not found.",
                warnings=[str(item) for item in context.get("blocked_reasons", []) if item],
            )
        ]

    events: list[dict[str, Any]] = []
    for run in context.get("workspace_runs", []):
        if not isinstance(run, dict):
            continue
        run_id = str(run.get("workspace_run_id", ""))
        run_created_at = str(run.get("created_at", utc_now()))
        events.append(
            _event(
                case_id=case_id,
                workspace_run_id=run_id,
                stage_id="workspace_run",
                module="personal_alpha_workspace",
                event_type="metadata_stage_status",
                result="metadata_ready",
                action="create_workspace_run",
                target_id=run_id,
                message="Workspace run metadata recorded.",
                created_at=run_created_at,
            )
        )
        for source_event in run.get("unified_audit_timeline", []):
            if not isinstance(source_event, dict):
                continue
            raw_stage_id = str(source_event.get("stage_id", "workspace_run"))
            events.append(
                _event(
                    case_id=case_id,
                    workspace_run_id=run_id,
                    stage_id=WORKSPACE_STAGE_MAP.get(raw_stage_id, "workspace_run"),
                    module="personal_alpha_workspace",
                    event_type=str(source_event.get("event_type", "metadata_stage_status")),
                    result=_normalize_result(str(source_event.get("result", "metadata_ready"))),
                    action=raw_stage_id,
                    target_id=run_id,
                    message="Workspace stage metadata event recorded.",
                    created_at=str(source_event.get("created_at", run_created_at)),
                )
            )

    for item in context.get("source_decisions", []):
        if isinstance(item, dict):
            events.append(_decision_event(case_id, context, item, "source_review_decision", "personal_alpha_source_review", "decision_recorded"))
    for item in context.get("gate_decisions", []):
        if isinstance(item, dict):
            events.append(_decision_event(case_id, context, item, "final_gate", "personal_alpha_final_gate", "gate_decision_recorded"))
    for item in context.get("packets", []):
        if isinstance(item, dict):
            packet_id = str(item.get("packet_id", ""))
            events.append(
                _event(
                    case_id=case_id,
                    workspace_run_id=str(item.get("workspace_run_id", context.get("latest_workspace_run_id", ""))),
                    packet_id=packet_id,
                    stage_id="final_packet",
                    module="personal_alpha_final_packet",
                    event_type="packet_created",
                    result="created",
                    action="create_final_packet",
                    target_id=packet_id,
                    message="Final review packet metadata created.",
                    created_at=str(item.get("created_at", utc_now())),
                )
            )
    for item in context.get("lawyer_actions", []):
        if isinstance(item, dict):
            action = str(item.get("action", ""))
            events.append(
                _event(
                    case_id=case_id,
                    workspace_run_id=str(context.get("latest_workspace_run_id", "")),
                    packet_id=str(item.get("packet_id", context.get("latest_packet_id", ""))),
                    stage_id="lawyer_final_review",
                    module="personal_alpha_lawyer_final_review",
                    event_type="lawyer_review_action_recorded",
                    result=_normalize_result(action),
                    action=action or "submit_lawyer_final_review",
                    target_id=str(item.get("action_id", "")),
                    message="Lawyer final review metadata action recorded.",
                    created_at=str(item.get("created_at", utc_now())),
                )
            )
    for item in context.get("locks", []):
        if isinstance(item, dict):
            lock_id = str(item.get("lock_id", ""))
            events.append(
                _event(
                    case_id=case_id,
                    workspace_run_id=str(context.get("latest_workspace_run_id", "")),
                    packet_id=str(item.get("packet_id", context.get("latest_packet_id", ""))),
                    lock_id=lock_id,
                    stage_id="final_lock",
                    module="personal_alpha_final_lock",
                    event_type="final_lock_created",
                    result="created",
                    action="create_final_lock",
                    target_id=lock_id,
                    message="Controlled final lock metadata created.",
                    created_at=str(item.get("created_at", utc_now())),
                )
            )

    events.append(
        _event(
            case_id=case_id,
            workspace_run_id=str(context.get("latest_workspace_run_id", "")),
            packet_id=str(context.get("latest_packet_id", "")) or None,
            lock_id=str(context.get("latest_lock_id", "")) or None,
            stage_id="case_os",
            module="personal_alpha_case_os",
            event_type="metadata_stage_status",
            result="metadata_ready",
            action="aggregate_case_os_metadata",
            target_id=case_id,
            message="Case OS metadata aggregation completed.",
            created_at=utc_now(),
        )
    )
    return events


def _decision_event(
    case_id: str,
    context: dict[str, Any],
    item: dict[str, Any],
    stage_id: str,
    module: str,
    event_type: str,
) -> dict[str, Any]:
    decision = str(item.get("decision", item.get("status", "metadata_ready")))
    target_id = str(item.get("decision_id", item.get("gate_decision_id", "")))
    return _event(
        case_id=case_id,
        workspace_run_id=str(item.get("workspace_run_id", context.get("latest_workspace_run_id", ""))),
        stage_id=stage_id,
        module=module,
        event_type=event_type,
        result=_normalize_result(decision),
        action=decision,
        target_id=target_id,
        message=f"{stage_id.replace('_', ' ').title()} metadata decision recorded.",
        created_at=str(item.get("created_at", utc_now())),
    )


def _event(
    *,
    case_id: str,
    stage_id: str,
    module: str,
    event_type: str,
    result: str,
    safety_status: str = "safe_metadata_only",
    workspace_run_id: str | None = None,
    packet_id: str | None = None,
    lock_id: str | None = None,
    actor_id: str = "local_metadata_reviewer",
    action: str | None = None,
    target_id: str | None = None,
    message: str = "",
    warnings: list[str] | None = None,
    created_at: str | None = None,
) -> dict[str, Any]:
    return PersonalAlphaCaseOSUnifiedAuditEvent(
        timeline_event_id=f"case_os_audit_event_{uuid4().hex[:12]}",
        case_id=case_id,
        workspace_run_id=workspace_run_id or None,
        packet_id=packet_id or None,
        lock_id=lock_id or None,
        stage_id=stage_id,
        module=module,
        event_type=event_type,
        result=result,
        safety_status=safety_status,
        actor_id=actor_id,
        action=action,
        target_id=target_id,
        message=message,
        mock_or_redacted_only=True,
        raw_content_included=False,
        redacted=False,
        warnings=warnings or [],
        created_at=created_at or utc_now(),
    ).model_dump()


def _normalize_result(value: str) -> str:
    normalized = str(value or "").strip().lower()
    if normalized in {"approve", "approve_packet", "approved", "mock_ready"}:
        return "approved" if normalized != "mock_ready" else "metadata_ready"
    if normalized in {"reject", "reject_packet", "rejected"}:
        return "rejected"
    if normalized in {"request_revision", "request_packet_revision", "revision_requested"}:
        return "revision_requested"
    if normalized in {"created", "metadata_ready", "pending", "blocked", "safe_not_found"}:
        return normalized
    return "metadata_ready"
