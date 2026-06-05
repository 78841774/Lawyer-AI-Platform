from uuid import uuid4

from personal_showcase_pack.safety_engine import default_safety_flags
from personal_showcase_pack.schemas import ShowcaseAuditEvent, ShowcaseAuditTimeline
from personal_showcase_pack.storage import AUDIT_DIR, read_payloads, write_payload


def record_audit_event(action: str, actor: str, object_type: str, object_id: str, timestamp: str) -> None:
    audit_id = f"personal_showcase_audit_{uuid4().hex[:12]}"
    event = ShowcaseAuditEvent(
        audit_id=audit_id,
        action=action,
        actor=actor,
        object_type=object_type,
        object_id=object_id,
        timestamp=timestamp,
        safety_flags=default_safety_flags(),
    )
    write_payload(AUDIT_DIR, audit_id, event.model_dump())


def build_audit_timeline() -> dict:
    events = [ShowcaseAuditEvent(**payload) for payload in read_payloads(AUDIT_DIR)]
    events = sorted(events, key=lambda record: record.timestamp, reverse=True)
    return ShowcaseAuditTimeline(events=events, event_count=len(events), warnings=["审计记录仅包含展示包 mock metadata。"]).model_dump()
