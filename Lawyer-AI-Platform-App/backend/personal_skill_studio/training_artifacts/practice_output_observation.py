from datetime import UTC, datetime

from personal_skill_studio.training_artifacts.practice_feedback_audit_engine import build_feedback_audit_event
from personal_skill_studio.training_artifacts.practice_feedback_registry import (
    build_v731h_status,
    get_observation,
    list_observations,
    write_observation,
)
from personal_skill_studio.training_artifacts.practice_feedback_safety_engine import (
    feedback_metadata_safe,
    v731h_safety_flags,
)
from personal_skill_studio.training_artifacts.practice_feedback_source_trace_engine import build_feedback_source_trace
from personal_skill_studio.training_artifacts.practice_runtime_registry import list_usage_events
from personal_skill_studio.training_artifacts.schemas import (
    PracticeOutputObservation,
    PracticeOutputObservationRequest,
    PracticeRuntimeUsageEvent,
)


def create_output_observation(request: PracticeOutputObservationRequest) -> dict | None:
    usage_event = _get_usage_event(request.usage_event_id)
    if usage_event is None or not feedback_metadata_safe(request.model_dump()):
        return None
    observation_id = f"practice_observation_{datetime.now(UTC).strftime('%Y%m%d%H%M%S%f')}"
    source_trace = build_feedback_source_trace(
        object_id=observation_id,
        source_trace_type="practice_output_observation",
        usage_event_id=usage_event.usage_event_id,
        runtime_load_id=usage_event.runtime_load_id,
        package_id=usage_event.package_id,
    )
    audit_event = build_feedback_audit_event(
        object_id=observation_id,
        object_type="practice_output_observation",
        action="output_observation_recorded",
        actor_id=request.observed_by,
        actor_note="redacted output observation metadata recorded",
    )
    observation = PracticeOutputObservation(
        observation_id=observation_id,
        usage_event_id=usage_event.usage_event_id,
        runtime_load_id=usage_event.runtime_load_id,
        package_id=usage_event.package_id,
        package_version=usage_event.package_version,
        case_cause=usage_event.case_cause,
        task_type=usage_event.task_type,
        runtime_mode=usage_event.runtime_mode,
        output_category=request.output_category,
        output_summary_redacted=request.output_summary_redacted,
        observed_issue_summary=request.observed_issue_summary,
        safety_flags=request.safety_flags,
        generated_at=datetime.now(UTC).isoformat(),
        observed_by=request.observed_by,
        audit_id=f"{observation_id}_audit",
        source_trace_id=source_trace.source_trace_id,
        audit_events=[audit_event],
        source_trace=source_trace,
        warnings=[
            "Observation stores redacted metadata only.",
            "Observation does not mutate loaded packages or trigger provider calls.",
        ],
        **v731h_safety_flags(),
    )
    write_observation(observation)
    return observation.model_dump()


def list_output_observations() -> dict:
    return list_observations()


def get_output_observation(observation_id: str) -> dict | None:
    return get_observation(observation_id)


def build_output_observation_status() -> dict:
    return build_v731h_status()


def _get_usage_event(usage_event_id: str) -> PracticeRuntimeUsageEvent | None:
    for event in list_usage_events():
        if event.usage_event_id == usage_event_id:
            return event
    return None
