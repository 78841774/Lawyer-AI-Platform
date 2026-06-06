from datetime import datetime, timezone
from uuid import uuid4

from personal_legal_enterprise_gateway.schemas import AuditEvent, AuditTimeline
from personal_legal_enterprise_gateway.storage import AUDIT_DIR, read_payloads, write_payload


def now_iso() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def record_audit_event(provider_id: str, action: str, run_id: str | None = None) -> None:
    event_id = f"legal_enterprise_audit_{uuid4().hex[:12]}"
    event = AuditEvent(event_id=event_id, provider_id=provider_id, action=action, run_id=run_id, created_at=now_iso())
    write_payload(AUDIT_DIR, event_id, event.model_dump())


def build_audit_timeline() -> dict:
    events = [AuditEvent(**payload) for payload in read_payloads(AUDIT_DIR)]
    return AuditTimeline(events=sorted(events, key=lambda event: event.created_at, reverse=True), event_count=len(events)).model_dump()

