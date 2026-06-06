from personal_skill_studio.training_artifacts.iteration_candidate_safety_engine import v731i_safety_flags
from personal_skill_studio.training_artifacts.practice_runtime_registry import get_runtime_load
from personal_skill_studio.training_artifacts.schemas import IterationCandidateSourceTrace


def build_iteration_candidate_source_trace(
    object_id: str,
    source_trace_type: str,
    source_package_id: str,
    source_package_version: str,
    source_runtime_load_id: str,
    source_feedback_ids: list[str],
    source_risk_event_ids: list[str],
    source_observation_ids: list[str],
) -> IterationCandidateSourceTrace:
    runtime_load = get_runtime_load(source_runtime_load_id) or {}
    return IterationCandidateSourceTrace(
        source_trace_id=f"{object_id}_source_trace",
        source_trace_type=source_trace_type,
        object_id=object_id,
        source_package_id=source_package_id,
        source_package_version=source_package_version,
        source_runtime_load_id=source_runtime_load_id,
        source_feedback_ids=source_feedback_ids,
        source_risk_event_ids=source_risk_event_ids,
        source_observation_ids=source_observation_ids,
        inherited_runtime_source_trace_id=runtime_load.get("source_trace_bundle_id"),
        warnings=["Iteration source trace links metadata identifiers only; no source content is copied."],
        **v731i_safety_flags(),
    )
