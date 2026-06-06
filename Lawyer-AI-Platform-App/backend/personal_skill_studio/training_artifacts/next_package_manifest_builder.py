from personal_skill_studio.training_artifacts.next_package_safety_engine import v731j_safety_flags
from personal_skill_studio.training_artifacts.schemas import NextPackageManifest, PracticeFeedbackCandidatePack


def build_next_package_manifest(
    next_package_id: str,
    candidate_pack: PracticeFeedbackCandidatePack,
    next_package_name: str,
    next_package_version: str,
    draft_status: str,
) -> NextPackageManifest:
    return NextPackageManifest(
        manifest_id=f"{next_package_id}_manifest",
        next_package_id=next_package_id,
        candidate_pack_id=candidate_pack.candidate_pack_id,
        source_package_id=candidate_pack.source_package_id,
        source_package_version=candidate_pack.source_package_version,
        next_package_name=next_package_name,
        next_package_version=next_package_version,
        draft_status=draft_status,
        applied_candidate_ids=[
            candidate.iteration_candidate_id for candidate in candidate_pack.iteration_candidates
        ],
        warnings=[
            "Manifest is draft metadata only.",
            "Practice runtime loading requires a later lawyer-approved load review path.",
        ],
        **v731j_safety_flags(),
    )
