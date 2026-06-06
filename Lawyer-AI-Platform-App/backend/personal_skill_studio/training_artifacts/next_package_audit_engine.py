from datetime import UTC, datetime

from personal_skill_studio.training_artifacts.schemas import NextPackageAuditEvent


def build_next_package_audit_event(
    next_package_id: str,
    action: str,
    actor_id: str | None = None,
    actor_note: str | None = None,
) -> NextPackageAuditEvent:
    return NextPackageAuditEvent(
        event_id=f"{next_package_id}_next_package_audit_{action}_{datetime.now(UTC).strftime('%Y%m%d%H%M%S%f')}",
        next_package_id=next_package_id,
        action=action,
        actor_id=actor_id,
        actor_note=actor_note,
        timestamp=datetime.now(UTC).isoformat(),
    )
