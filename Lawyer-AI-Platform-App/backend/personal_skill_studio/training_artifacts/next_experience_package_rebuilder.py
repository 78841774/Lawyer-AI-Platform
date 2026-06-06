from datetime import UTC, datetime

from personal_skill_studio.training_artifacts.candidate_pack_apply_engine import apply_candidate_pack
from personal_skill_studio.training_artifacts.lawyer_review_view_regenerator import regenerate_lawyer_review_view
from personal_skill_studio.training_artifacts.next_package_audit_engine import build_next_package_audit_event
from personal_skill_studio.training_artifacts.next_package_manifest_builder import build_next_package_manifest
from personal_skill_studio.training_artifacts.next_package_safety_engine import next_package_metadata_safe, v731j_safety_flags
from personal_skill_studio.training_artifacts.next_package_source_trace_engine import build_next_package_source_trace
from personal_skill_studio.training_artifacts.next_package_validation_engine import validate_next_package_metadata
from personal_skill_studio.training_artifacts.practice_feedback_candidate_pack import (
    get_candidate_pack_record,
    list_candidate_pack_records,
)
from personal_skill_studio.training_artifacts.schemas import (
    NextExperiencePackageDraft,
    NextExperiencePackageRebuildRequest,
    PracticeFeedbackCandidatePack,
)


def rebuild_next_experience_package(request: NextExperiencePackageRebuildRequest) -> NextExperiencePackageDraft | None:
    if not next_package_metadata_safe(request.model_dump()):
        return None
    candidate_pack = _select_candidate_pack(request.candidate_pack_id)
    if candidate_pack is None or candidate_pack.candidate_status != "ready_for_next_experience_build":
        return None
    next_package_id = f"next_experience_package_{datetime.now(UTC).strftime('%Y%m%d%H%M%S%f')}"
    next_package_name = request.next_package_name or candidate_pack.proposed_next_package_name
    next_package_version = request.next_package_version or candidate_pack.proposed_next_package_version
    applied_changes = apply_candidate_pack(candidate_pack)
    lawyer_review_view = regenerate_lawyer_review_view(next_package_id, candidate_pack, applied_changes)
    manifest = build_next_package_manifest(
        next_package_id=next_package_id,
        candidate_pack=candidate_pack,
        next_package_name=next_package_name,
        next_package_version=next_package_version,
        draft_status="draft_rebuilt",
    )
    validation_result = validate_next_package_metadata(next_package_id, candidate_pack)
    source_trace = build_next_package_source_trace(next_package_id, candidate_pack)
    audit_event = build_next_package_audit_event(
        next_package_id=next_package_id,
        action="next_package_rebuilt",
        actor_id=request.rebuilt_by,
        actor_note="rebuilt draft metadata from ready candidate pack; not loaded into practice runtime",
    )
    return NextExperiencePackageDraft(
        next_package_id=next_package_id,
        source_package_id=candidate_pack.source_package_id,
        source_package_version=candidate_pack.source_package_version,
        candidate_pack_id=candidate_pack.candidate_pack_id,
        next_package_name=next_package_name,
        next_package_version=next_package_version,
        draft_status="draft_rebuilt",
        applied_candidate_ids=manifest.applied_candidate_ids,
        added_experience_cards=applied_changes["added_experience_cards"],
        revised_experience_cards=applied_changes["revised_experience_cards"],
        removed_experience_cards=applied_changes["removed_experience_cards"],
        usage_boundary_changes=applied_changes["usage_boundary_changes"],
        risk_warning_changes=applied_changes["risk_warning_changes"],
        rollback_recommendations=applied_changes["rollback_recommendations"],
        disable_recommendations=applied_changes["disable_recommendations"],
        lawyer_review_view_id=lawyer_review_view.lawyer_review_view_id,
        manifest_id=manifest.manifest_id,
        audit_id=f"{next_package_id}_audit",
        source_trace_id=source_trace.source_trace_id,
        created_at=datetime.now(UTC).isoformat(),
        lawyer_review_view=lawyer_review_view,
        manifest=manifest,
        validation_result=validation_result,
        audit_events=[audit_event],
        source_trace=source_trace,
        warnings=[
            "Next experience package is a draft metadata rebuild only.",
            "It is not loaded into practice runtime and must enter Practice Load Review before future loading.",
        ],
        **v731j_safety_flags(),
    )


def _select_candidate_pack(candidate_pack_id: str | None) -> PracticeFeedbackCandidatePack | None:
    if candidate_pack_id:
        return get_candidate_pack_record(candidate_pack_id)
    ready_packs = [
        pack
        for pack in list_candidate_pack_records()
        if pack.candidate_status == "ready_for_next_experience_build"
    ]
    return ready_packs[0] if ready_packs else None
