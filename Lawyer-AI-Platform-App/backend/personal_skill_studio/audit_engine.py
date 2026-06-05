from uuid import uuid4

from personal_skill_studio.safety_engine import default_safety_flags
from personal_skill_studio.schemas import SkillStudioAuditEvent, SkillStudioAuditTimeline
from personal_skill_studio.storage import AUDIT_DIR, read_payloads, write_payload


def record_audit_event(*, action: str, actor: str, object_type: str, object_id: str, timestamp: str) -> None:
    audit_id = f"personal_skill_studio_audit_{uuid4().hex[:12]}"
    event = SkillStudioAuditEvent(
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
    events = [SkillStudioAuditEvent(**payload) for payload in read_payloads(AUDIT_DIR)]
    events = sorted(events, key=lambda event: event.timestamp, reverse=True)
    return SkillStudioAuditTimeline(
        events=events,
        event_count=len(events),
        warnings=["审计记录仅包含 metadata，不包含案件原文、API key 或本地路径。"],
    ).model_dump()
