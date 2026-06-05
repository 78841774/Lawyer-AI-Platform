from typing import Any

from personal_alpha_case_os.schemas import PersonalAlphaCaseOSAuditTimelineAvailableFilters, PersonalAlphaCaseOSAuditTimelineFilters

DEFAULT_LIMIT = 100
MAX_LIMIT = 200

AVAILABLE_FILTERS = {
    "stage_id": [
        "workspace_run",
        "source_review",
        "source_review_decision",
        "final_readiness",
        "final_gate",
        "final_packet",
        "lawyer_final_review",
        "final_lock",
        "case_os",
    ],
    "event_type": [
        "metadata_stage_status",
        "decision_recorded",
        "gate_decision_recorded",
        "packet_created",
        "lawyer_review_action_recorded",
        "final_lock_created",
        "blocked",
        "not_found",
        "redacted",
    ],
    "result": [
        "metadata_ready",
        "pending",
        "blocked",
        "safe_not_found",
        "created",
        "approved",
        "rejected",
        "revision_requested",
    ],
    "safety_status": [
        "safe_metadata_only",
        "redacted",
        "blocked_unsafe_input",
        "safe_not_found",
    ],
}


def build_filters(
    stage_id: str | None = None,
    event_type: str | None = None,
    result: str | None = None,
    safety_status: str | None = None,
    limit: int | None = None,
    offset: int | None = None,
) -> PersonalAlphaCaseOSAuditTimelineFilters:
    safe_limit = max(1, min(int(limit or DEFAULT_LIMIT), MAX_LIMIT))
    safe_offset = max(0, int(offset or 0))
    return PersonalAlphaCaseOSAuditTimelineFilters(
        stage_id=_clean_filter(stage_id),
        event_type=_clean_filter(event_type),
        result=_clean_filter(result),
        safety_status=_clean_filter(safety_status),
        limit=safe_limit,
        offset=safe_offset,
    )


def apply_audit_filters(events: list[dict[str, Any]], filters: PersonalAlphaCaseOSAuditTimelineFilters) -> list[dict[str, Any]]:
    filtered = [
        event
        for event in events
        if _matches(event, "stage_id", filters.stage_id)
        and _matches(event, "event_type", filters.event_type)
        and _matches(event, "result", filters.result)
        and _matches(event, "safety_status", filters.safety_status)
    ]
    return filtered[filters.offset : filters.offset + filters.limit]


def available_filters_payload(case_id: str, warnings: list[str] | None = None) -> dict[str, Any]:
    return PersonalAlphaCaseOSAuditTimelineAvailableFilters(
        case_id=case_id,
        available_filters=AVAILABLE_FILTERS,
        mock_or_redacted_only=True,
        raw_content_included=False,
        warnings=warnings or [],
    ).model_dump()


def _matches(event: dict[str, Any], field: str, value: str | None) -> bool:
    return not value or str(event.get(field, "")) == value


def _clean_filter(value: str | None) -> str | None:
    text = str(value or "").strip()
    return text or None
