from uuid import uuid4

from personal_delivery_packet.safety_engine import default_safety_flags
from personal_delivery_packet.schemas import DeliveryPacketAuditEvent, DeliveryPacketAuditTimeline
from personal_delivery_packet.storage import AUDIT_DIR, read_payloads, write_payload


def record_audit_event(*, action: str, actor: str, object_type: str, object_id: str, timestamp: str) -> None:
    audit_id = f"personal_delivery_packet_audit_{uuid4().hex[:12]}"
    event = DeliveryPacketAuditEvent(
        audit_id=audit_id,
        action=action,
        actor="system" if actor == "system" else "redacted_reviewer",
        object_type=object_type,
        object_id=object_id,
        timestamp=timestamp,
        safety_flags=default_safety_flags(),
    )
    write_payload(AUDIT_DIR, audit_id, event.model_dump())


def build_audit_timeline() -> dict:
    events = [DeliveryPacketAuditEvent(**payload) for payload in read_payloads(AUDIT_DIR)]
    events = sorted(events, key=lambda event: event.timestamp, reverse=True)
    return DeliveryPacketAuditTimeline(events=events, event_count=len(events), warnings=["审计记录仅包含交付包 metadata。"]).model_dump()
