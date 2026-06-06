from personal_skill_studio.training_artifacts.next_package_safety_engine import v731j_safety_flags
from personal_skill_studio.training_artifacts.schemas import NextPackageSourceTrace, PracticeFeedbackCandidatePack


def build_next_package_source_trace(next_package_id: str, candidate_pack: PracticeFeedbackCandidatePack) -> NextPackageSourceTrace:
    return NextPackageSourceTrace(
        source_trace_id=f"{next_package_id}_source_trace",
        next_package_id=next_package_id,
        source_package_id=candidate_pack.source_package_id,
        source_package_version=candidate_pack.source_package_version,
        candidate_pack_id=candidate_pack.candidate_pack_id,
        source_feedback_ids=candidate_pack.feedback_ids,
        source_risk_event_ids=candidate_pack.risk_event_ids,
        source_observation_ids=candidate_pack.observation_ids,
        source_iteration_candidate_ids=[
            candidate.iteration_candidate_id for candidate in candidate_pack.iteration_candidates
        ],
        inherited_candidate_pack_source_trace_id=candidate_pack.source_trace_id,
        warnings=["Next package source trace links candidate metadata only; no source content is copied."],
        **v731j_safety_flags(),
    )
