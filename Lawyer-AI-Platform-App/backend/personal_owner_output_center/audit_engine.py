from datetime import datetime, timezone

from personal_owner_output_center.schemas import OwnerOutputAuditEvent, OwnerOutputAuditTimeline


AUDIT_EVENTS: list[OwnerOutputAuditEvent] = [
    OwnerOutputAuditEvent(
        event_id="owner_output_audit_registry_loaded",
        action="output_registry_loaded",
        object_type="owner_output_center",
        object_id="personal_owner_output_center",
        created_at="2026-06-06T10:23:00Z",
        warnings=["Audit event is metadata only."],
    )
]


def record_audit_event(action: str, object_type: str, object_id: str) -> None:
    created_at = datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")
    AUDIT_EVENTS.append(
        OwnerOutputAuditEvent(
            event_id=f"owner_output_audit_{len(AUDIT_EVENTS) + 1}",
            action=action,
            object_type=object_type,
            object_id=object_id,
            created_at=created_at,
            warnings=["Audit event is metadata only."],
        )
    )


def build_audit_timeline() -> dict:
    return OwnerOutputAuditTimeline(
        events=AUDIT_EVENTS,
        event_count=len(AUDIT_EVENTS),
        warnings=["Audit timeline excludes raw content, local paths, and provider credentials."],
    ).model_dump()
