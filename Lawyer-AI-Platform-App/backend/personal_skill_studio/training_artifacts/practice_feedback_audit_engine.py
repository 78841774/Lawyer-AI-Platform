from datetime import UTC, datetime

from personal_skill_studio.training_artifacts.schemas import PracticeFeedbackAuditEvent


def build_feedback_audit_event(
    object_id: str,
    object_type: str,
    action: str,
    actor_id: str | None = None,
    actor_note: str | None = None,
) -> PracticeFeedbackAuditEvent:
    return PracticeFeedbackAuditEvent(
        event_id=f"{object_id}_{object_type}_audit_{action}_{datetime.now(UTC).strftime('%Y%m%d%H%M%S%f')}",
        object_id=object_id,
        object_type=object_type,
        action=action,
        actor_id=actor_id,
        actor_note=actor_note,
        timestamp=datetime.now(UTC).isoformat(),
    )
