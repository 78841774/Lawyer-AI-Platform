from datetime import UTC, datetime

from personal_skill_studio.training_artifacts.experience_lifecycle_safety_engine import v732_safety_flags
from personal_skill_studio.training_artifacts.schemas import ExperiencePackageLineage


def lineage_node(
    root_package_id: str,
    package_id: str,
    package_version: str,
    package_kind: str,
    lineage_status: str,
    parent_package_id: str | None = None,
    derived_from_candidate_pack_id: str | None = None,
    derived_from_feedback_ids: list[str] | None = None,
    derived_from_risk_event_ids: list[str] | None = None,
    loaded_runtime_load_ids: list[str] | None = None,
) -> ExperiencePackageLineage:
    return ExperiencePackageLineage(
        lineage_id=f"lineage_{package_id}_{package_kind}",
        root_package_id=root_package_id,
        package_id=package_id,
        package_version=package_version,
        package_kind=package_kind,
        parent_package_id=parent_package_id,
        derived_from_candidate_pack_id=derived_from_candidate_pack_id,
        derived_from_feedback_ids=derived_from_feedback_ids or [],
        derived_from_risk_event_ids=derived_from_risk_event_ids or [],
        loaded_runtime_load_ids=loaded_runtime_load_ids or [],
        lineage_status=lineage_status,
        created_at=datetime.now(UTC).isoformat(),
        **v732_safety_flags(),
    )
