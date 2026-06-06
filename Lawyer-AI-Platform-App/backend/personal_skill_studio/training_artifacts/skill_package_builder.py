from datetime import UTC, datetime
from uuid import uuid4

from personal_skill_studio.training_artifacts.schemas import (
    CodexSkillDraft,
    SkillPackage,
    SkillPackageBuildRequest,
)
from personal_skill_studio.training_artifacts.skill_package_audit_engine import build_audit_event
from personal_skill_studio.training_artifacts.skill_package_manifest import build_manifest
from personal_skill_studio.training_artifacts.skill_package_safety_engine import v731d_safety_flags
from personal_skill_studio.training_artifacts.skill_package_source_trace_engine import build_source_trace_bundle
from personal_skill_studio.training_artifacts.storage import CODEX_SKILL_DRAFTS_DIR, read_payload, read_payloads


CONFIRMED_STATUSES = {"structure_approved_requires_pre_publish_gate"}


def build_skill_package(request: SkillPackageBuildRequest) -> SkillPackage | None:
    draft = _resolve_draft(request.source_draft_id)
    if draft is None or draft.confirmation_status not in CONFIRMED_STATUSES:
        return None
    if not draft.created_from_experience_ids:
        return None

    now = datetime.now(UTC).isoformat()
    package_id = f"skill_package_v731d_{uuid4().hex[:10]}"
    manifest = build_manifest(package_id, request.package_name, request.package_version, draft)
    source_trace_bundle = build_source_trace_bundle(package_id, draft)
    audit_events = [build_audit_event(package_id, "skill_package_build")]
    return SkillPackage(
        package_id=package_id,
        package_name=request.package_name,
        package_version=request.package_version,
        source_draft_id=draft.draft_id,
        experience_ids=draft.created_from_experience_ids,
        experience_count=len(draft.created_from_experience_ids),
        manifest_id=manifest.manifest_id,
        source_trace_bundle_id=source_trace_bundle.source_trace_bundle_id,
        audit_bundle_id=f"{package_id}_audit_bundle",
        pre_publish_gate_status="draft",
        package_status="draft_package",
        created_at=now,
        updated_at=now,
        supersedes_package_id=request.supersedes_package_id,
        rollback_available=bool(request.supersedes_package_id),
        manifest=manifest,
        source_trace_bundle=source_trace_bundle,
        audit_events=audit_events,
        warnings=[
            "Package is versioned metadata only.",
            "Final review is not applicable in v7.31d; practice load review is deferred to v7.31f.",
        ],
        **v731d_safety_flags(),
    )


def _resolve_draft(draft_id: str | None) -> CodexSkillDraft | None:
    if draft_id:
        payload = read_payload(CODEX_SKILL_DRAFTS_DIR, draft_id)
        return CodexSkillDraft(**payload) if payload else None
    drafts = [CodexSkillDraft(**payload) for payload in reversed(read_payloads(CODEX_SKILL_DRAFTS_DIR))]
    return next((draft for draft in drafts if draft.confirmation_status in CONFIRMED_STATUSES), None)
