from uuid import uuid4

from personal_production_pilot.safety_engine import default_safety_flags
from personal_production_pilot.schemas import PilotAuditEvent, PilotAuditTimeline
from personal_production_pilot.storage import AUDIT_DIR, read_payloads, write_payload


def record_audit_event(*, action: str, actor: str, object_type: str, object_id: str, timestamp: str) -> None:
    audit_id = f"personal_production_pilot_audit_{uuid4().hex[:12]}"
    event = PilotAuditEvent(
        audit_id=audit_id,
        action=action,
        actor="system" if actor == "system" else "redacted_owner",
        object_type=object_type,
        object_id=object_id,
        timestamp=timestamp,
        safety_flags=default_safety_flags(),
    )
    write_payload(AUDIT_DIR, audit_id, event.model_dump())


def build_audit_timeline() -> dict:
    events = [PilotAuditEvent(**payload) for payload in read_payloads(AUDIT_DIR)]
    events = sorted(events, key=lambda event: event.timestamp, reverse=True)
    return PilotAuditTimeline(events=events, event_count=len(events), warnings=["Audit contains pilot metadata only."]).model_dump()
