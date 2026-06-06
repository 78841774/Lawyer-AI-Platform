from personal_skill_studio.training_artifacts.practice_feedback_safety_engine import v731h_safety_flags
from personal_skill_studio.training_artifacts.practice_runtime_registry import get_runtime_load
from personal_skill_studio.training_artifacts.schemas import PracticeFeedbackSourceTrace


def build_feedback_source_trace(
    object_id: str,
    source_trace_type: str,
    usage_event_id: str,
    runtime_load_id: str,
    package_id: str,
) -> PracticeFeedbackSourceTrace:
    runtime_load = get_runtime_load(runtime_load_id) or {}
    return PracticeFeedbackSourceTrace(
        source_trace_id=f"{object_id}_source_trace",
        source_trace_type=source_trace_type,
        object_id=object_id,
        usage_event_id=usage_event_id,
        runtime_load_id=runtime_load_id,
        package_id=package_id,
        source_usage_event_id=usage_event_id,
        source_runtime_load_id=runtime_load_id,
        inherited_runtime_source_trace_id=runtime_load.get("source_trace_bundle_id"),
        warnings=["Feedback source trace links metadata identifiers only; no source content is copied."],
        **v731h_safety_flags(),
    )
