from datetime import UTC, datetime

from personal_skill_studio.training_artifacts.schemas import SkillPackageAudit, SkillPackageAuditEvent
from personal_skill_studio.training_artifacts.skill_package_safety_engine import v731d_safety_flags


def build_audit_event(package_id: str, action: str) -> SkillPackageAuditEvent:
    return SkillPackageAuditEvent(
        event_id=f"{package_id}_audit_{action}_{datetime.now(UTC).strftime('%Y%m%d%H%M%S%f')}",
        package_id=package_id,
        action=action,
        timestamp=datetime.now(UTC).isoformat(),
    )


def build_package_audit(package_id: str, events: list[SkillPackageAuditEvent]) -> SkillPackageAudit:
    return SkillPackageAudit(
        package_id=package_id,
        events=events,
        event_count=len(events),
        warnings=["Audit bundle records system metadata events only."],
        **v731d_safety_flags(),
    )
