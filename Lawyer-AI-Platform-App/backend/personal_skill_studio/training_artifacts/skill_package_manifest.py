from datetime import UTC, datetime
from uuid import uuid4

from personal_skill_studio.training_artifacts.schemas import CodexSkillDraft, SkillPackageManifest
from personal_skill_studio.training_artifacts.skill_package_safety_engine import v731d_safety_flags


def build_manifest(package_id: str, package_name: str, package_version: str, draft: CodexSkillDraft) -> SkillPackageManifest:
    now = datetime.now(UTC).isoformat()
    return SkillPackageManifest(
        manifest_id=f"skill_package_manifest_v731d_{uuid4().hex[:10]}",
        package_id=package_id,
        package_name=package_name,
        package_version=package_version,
        source_draft_id=draft.draft_id,
        experience_ids=draft.created_from_experience_ids,
        experience_count=len(draft.created_from_experience_ids),
        section_count=len(draft.sections),
        validation_requirements=[
            "experience_redacted",
            "experience_approved",
            "source_trace_present",
            "audit_complete",
            "draft_structure_confirmed",
            "sensitive_field_scan_passed",
        ],
        created_at=now,
        updated_at=now,
        warnings=["Manifest is metadata-only and not a published Skill package."],
        **v731d_safety_flags(),
    )
