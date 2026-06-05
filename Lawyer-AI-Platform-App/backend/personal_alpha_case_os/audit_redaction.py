import re
from typing import Any

CHECKED_FIELDS = [
    "case_id",
    "workspace_run_id",
    "packet_id",
    "lock_id",
    "message",
    "warnings",
    "target_id",
    "actor_id",
    "action",
    "event_type",
    "result",
    "module",
    "stage_id",
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

UNSAFE_PATTERNS = {
    "api_key_like_value": (r"sk-[A-Za-z0-9_-]{12,}", r"api[_-]?key"),
    "personal_identifier_like_value": (
        r"(?<!\d)1[3-9]\d{9}(?!\d)",
        r"(?<!\d)\d{6}(?:19|20)\d{2}\d{2}\d{2}\d{3}[\dXx](?!\d)",
        r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}",
        r"[（(]\d{4}[）)][\u4e00-\u9fa5A-Za-z0-9第初终再执民商行刑破知号字\-]{4,40}号",
    ),
    "path_like_value": (
        r"\.(pdf|docx|xlsx|zip|png|jpg|jpeg|txt|md|json)$",
        r"[/\\]",
    ),
}


def redact_audit_event(event: dict[str, Any]) -> tuple[dict[str, Any], list[dict[str, str]]]:
    redacted_event = dict(event)
    unsafe_summaries: list[dict[str, str]] = []
    for field_name in CHECKED_FIELDS:
        value = redacted_event.get(field_name)
        reason = unsafe_reason(value)
        if not reason:
            continue
        unsafe_summaries.append(
            {
                "timeline_event_id": str(redacted_event.get("timeline_event_id", "")),
                "field_name": field_name,
                "reason": reason,
            }
        )
        redacted_event[field_name] = [] if isinstance(value, list) else ""
        redacted_event["redacted"] = True
        redacted_event["safety_status"] = "redacted"
        warnings = redacted_event.get("warnings", [])
        if isinstance(warnings, list):
            redacted_event["warnings"] = list(dict.fromkeys([*warnings, f"{field_name} redacted by audit guard."]))
    redacted_event["mock_or_redacted_only"] = True
    redacted_event["raw_content_included"] = False
    return redacted_event, unsafe_summaries


def redact_audit_events(events: list[dict[str, Any]]) -> tuple[list[dict[str, Any]], list[dict[str, str]]]:
    safe_events = []
    unsafe_summaries = []
    for event in events:
        redacted_event, event_unsafe = redact_audit_event(event)
        safe_events.append(redacted_event)
        unsafe_summaries.extend(event_unsafe)
    return safe_events, unsafe_summaries


def unsafe_reason(value: Any) -> str:
    values = value if isinstance(value, list) else [value]
    for item in values:
        text = str(item or "")
        lowered = text.lower()
        if any(marker.lower() in lowered for marker in SENSITIVE_MARKERS):
            return "path_like_value"
        for reason, patterns in UNSAFE_PATTERNS.items():
            if any(re.search(pattern, text, flags=re.IGNORECASE) for pattern in patterns):
                return reason
    return ""
