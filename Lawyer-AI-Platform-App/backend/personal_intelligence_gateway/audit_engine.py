from uuid import uuid4

from personal_intelligence_gateway.safety_engine import default_safety_flags
from personal_intelligence_gateway.schemas import (
    PersonalIntelligenceAuditEvent,
    PersonalIntelligenceAuditTimeline,
    PersonalIntelligenceLiveAuditEvent,
    PersonalIntelligenceLiveAuditTimeline,
)
from personal_intelligence_gateway.storage import AUDIT_DIR, LIVE_AUDIT_DIR, read_payloads, write_payload


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


def record_live_audit_event(
    *,
    provider_id: str,
    action: str,
    actor_id: str,
    query_type: str,
    created_at: str,
    run_id: str | None = None,
    review_item_id: str | None = None,
    live_call_requested: bool = False,
    live_call_executed: bool = False,
    blocked_reason: str | None = None,
    source_trace_created: bool = False,
) -> None:
    event_id = f"personal_intelligence_live_audit_{uuid4().hex[:12]}"
    event = PersonalIntelligenceLiveAuditEvent(
        event_id=event_id,
        provider_id=provider_id,
        action=action,
        actor_id=_redact_actor(actor_id),
        query_type=query_type,
        run_id=run_id,
        review_item_id=review_item_id,
        live_call_requested=live_call_requested,
        live_call_executed=live_call_executed,
        blocked_reason=blocked_reason,
        source_trace_created=source_trace_created,
        created_at=created_at,
    )
    write_payload(LIVE_AUDIT_DIR, event_id, event.model_dump())


def build_live_audit_timeline() -> dict:
    events = [PersonalIntelligenceLiveAuditEvent(**payload) for payload in read_payloads(LIVE_AUDIT_DIR)]
    events = sorted(events, key=lambda event: event.created_at, reverse=True)
    return PersonalIntelligenceLiveAuditTimeline(
        events=events,
        event_count=len(events),
        warnings=["Live audit records contain metadata only. No provider raw content, API key, local path, final citation, final legal opinion, or final report is returned."],
    ).model_dump()
