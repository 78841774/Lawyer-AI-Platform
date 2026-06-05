from uuid import uuid4

from personal_intelligence_gateway.safety_engine import default_safety_flags
from personal_intelligence_gateway.schemas import PersonalIntelligenceAuditEvent, PersonalIntelligenceAuditTimeline
from personal_intelligence_gateway.storage import AUDIT_DIR, read_payloads, write_payload


def record_audit_event(
    *,
    action: str,
    actor: str,
    provider_id: str,
    query_id: str,
    timestamp: str,
    source_trace_id: str | None = None,
) -> None:
    audit_id = f"personal_intelligence_audit_{uuid4().hex[:12]}"
    event = PersonalIntelligenceAuditEvent(
        audit_id=audit_id,
        action=action,
        actor=_redact_actor(actor),
        provider_id=provider_id,
        query_id=query_id,
        source_trace_id=source_trace_id,
        timestamp=timestamp,
        safety_flags=default_safety_flags(),
    )
    write_payload(AUDIT_DIR, audit_id, event.model_dump())


def build_audit_timeline() -> dict:
    events = [PersonalIntelligenceAuditEvent(**payload) for payload in read_payloads(AUDIT_DIR)]
    events = sorted(events, key=lambda event: event.timestamp, reverse=True)
    return PersonalIntelligenceAuditTimeline(
        events=events,
        event_count=len(events),
        warnings=["审计记录仅包含 metadata，不包含外部原文、API key 或本地路径。"],
    ).model_dump()


def _redact_actor(actor: str) -> str:
    if actor == "system":
        return actor
    return "redacted_reviewer"
