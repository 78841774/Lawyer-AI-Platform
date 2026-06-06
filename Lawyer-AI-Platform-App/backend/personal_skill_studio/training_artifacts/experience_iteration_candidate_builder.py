from datetime import UTC, datetime

from personal_skill_studio.training_artifacts.experience_iteration_diff_engine import build_iteration_diff
from personal_skill_studio.training_artifacts.feedback_to_experience_mapper import (
    map_feedback_to_candidate,
    map_risk_event_to_candidate,
)
from personal_skill_studio.training_artifacts.iteration_candidate_audit_engine import build_iteration_candidate_audit_event
from personal_skill_studio.training_artifacts.iteration_candidate_safety_engine import (
    iteration_candidate_metadata_safe,
    v731i_safety_flags,
)
from personal_skill_studio.training_artifacts.iteration_candidate_source_trace_engine import build_iteration_candidate_source_trace
from personal_skill_studio.training_artifacts.next_package_proposal_registry import (
    build_next_package_name,
    build_next_package_version,
)
from personal_skill_studio.training_artifacts.practice_feedback_registry import (
    list_feedback_records,
    list_feedback_risk_event_records,
)
from personal_skill_studio.training_artifacts.practice_runtime_registry import get_runtime_load
from personal_skill_studio.training_artifacts.schemas import (
    ExperienceIterationCandidate,
    PracticeFeedbackCandidatePack,
    PracticeFeedbackCandidatePackBuildRequest,
)


ELIGIBLE_FEEDBACK_STATUSES = {"triaged", "accepted_as_candidate", "converted_to_iteration_candidate"}


def build_candidate_pack(request: PracticeFeedbackCandidatePackBuildRequest) -> PracticeFeedbackCandidatePack | None:
    if not iteration_candidate_metadata_safe(request.model_dump()):
        return None
    feedback_items = _eligible_feedback_items(request)
    if not feedback_items:
        return None
    source_package_id = request.source_package_id or feedback_items[0].package_id
    source_package_version = feedback_items[0].package_version
    source_runtime_load_id = request.source_runtime_load_id or feedback_items[0].runtime_load_id
    runtime_load = get_runtime_load(source_runtime_load_id) or {}
    candidate_pack_id = f"practice_feedback_candidate_pack_{datetime.now(UTC).strftime('%Y%m%d%H%M%S%f')}"
    related_risk_events = _related_risk_events(source_package_id, source_runtime_load_id)
    candidates = _build_iteration_candidates(candidate_pack_id, feedback_items, related_risk_events)
    diff = build_iteration_diff(candidate_pack_id, candidates)
    feedback_ids = [item.feedback_id for item in feedback_items]
    risk_event_ids = [item.risk_event_id for item in related_risk_events]
    observation_ids = sorted(
        {
            item.observation_id
            for item in [*feedback_items, *related_risk_events]
            if item.observation_id
        }
    )
    audit_event = build_iteration_candidate_audit_event(
        object_id=candidate_pack_id,
        object_type="practice_feedback_candidate_pack",
        action="candidate_pack_built",
        actor_id=request.build_requested_by,
        actor_note="built from triaged v7.31h feedback metadata only",
    )
    source_trace = build_iteration_candidate_source_trace(
        object_id=candidate_pack_id,
        source_trace_type="practice_feedback_candidate_pack",
        source_package_id=source_package_id,
        source_package_version=source_package_version,
        source_runtime_load_id=source_runtime_load_id,
        source_feedback_ids=feedback_ids,
        source_risk_event_ids=risk_event_ids,
        source_observation_ids=observation_ids,
    )
    return PracticeFeedbackCandidatePack(
        candidate_pack_id=candidate_pack_id,
        source_package_id=source_package_id,
        source_package_version=source_package_version,
        source_runtime_load_id=source_runtime_load_id,
        feedback_ids=feedback_ids,
        risk_event_ids=risk_event_ids,
        observation_ids=observation_ids,
        candidate_status="draft_candidate_pack" if candidates else "blocked",
        proposed_next_package_name=build_next_package_name(source_package_id, request.proposed_next_package_name),
        proposed_next_package_version=build_next_package_version(source_package_version, request.proposed_next_package_version),
        proposed_changes_count=len(candidates),
        created_at=datetime.now(UTC).isoformat(),
        audit_id=f"{candidate_pack_id}_audit",
        source_trace_id=source_trace.source_trace_id,
        iteration_candidates=candidates,
        diff=diff,
        audit_events=[audit_event],
        source_trace=source_trace,
        warnings=[
            "Candidate pack is metadata-only preparation for a later rebuild stage.",
            "It does not mutate loaded packages, lawyer-approved packages, runtime policy, Skills, or training artifacts.",
            "Next package draft rebuild remains deferred to v7.31j.",
        ],
        **v731i_safety_flags(),
    )


def _eligible_feedback_items(request: PracticeFeedbackCandidatePackBuildRequest):
    records = [
        item
        for item in list_feedback_records()
        if item.feedback_status in ELIGIBLE_FEEDBACK_STATUSES
        and item.classification.create_iteration_candidate_recommended
    ]
    if request.source_package_id:
        records = [item for item in records if item.package_id == request.source_package_id]
    if request.source_runtime_load_id:
        records = [item for item in records if item.runtime_load_id == request.source_runtime_load_id]
    return sorted(records, key=lambda item: item.created_at)


def _related_risk_events(source_package_id: str, source_runtime_load_id: str):
    return [
        event
        for event in list_feedback_risk_event_records()
        if event.package_id == source_package_id and event.runtime_load_id == source_runtime_load_id
    ]


def _build_iteration_candidates(candidate_pack_id: str, feedback_items, risk_events) -> list[ExperienceIterationCandidate]:
    candidates: list[ExperienceIterationCandidate] = []
    for index, feedback in enumerate(feedback_items, start=1):
        candidates.append(map_feedback_to_candidate(feedback, candidate_pack_id, index))
    start = len(candidates) + 1
    for index, risk_event in enumerate(risk_events, start=start):
        candidates.append(map_risk_event_to_candidate(risk_event, candidate_pack_id, index))
    return candidates
