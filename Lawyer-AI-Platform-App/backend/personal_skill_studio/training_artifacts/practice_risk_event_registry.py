from datetime import UTC, datetime

from personal_skill_studio.training_artifacts.practice_feedback_audit_engine import build_feedback_audit_event
from personal_skill_studio.training_artifacts.practice_feedback_registry import (
    get_observation_record,
    get_risk_event,
    list_feedback_risk_events,
    write_feedback_risk_event,
)
from personal_skill_studio.training_artifacts.practice_feedback_safety_engine import (
    feedback_metadata_safe,
    v731h_safety_flags,
)
from personal_skill_studio.training_artifacts.practice_feedback_source_trace_engine import build_feedback_source_trace
from personal_skill_studio.training_artifacts.schemas import PracticeFeedbackRiskEvent, PracticeRiskEventRequest


def create_practice_risk_event(request: PracticeRiskEventRequest) -> dict | None:
    observation = get_observation_record(request.observation_id)
    if observation is None or not feedback_metadata_safe(request.model_dump()):
        return None
    risk_event_id = f"practice_feedback_risk_{datetime.now(UTC).strftime('%Y%m%d%H%M%S%f')}"
    source_trace = build_feedback_source_trace(
        object_id=risk_event_id,
        source_trace_type="practice_feedback_risk_event",
        usage_event_id=observation.usage_event_id,
        runtime_load_id=observation.runtime_load_id,
        package_id=observation.package_id,
    )
    audit_event = build_feedback_audit_event(
        object_id=risk_event_id,
        object_type="practice_feedback_risk_event",
        action="risk_event_recorded",
        actor_id=request.created_by,
        actor_note="practice feedback risk metadata recorded",
    )
    risk_event = PracticeFeedbackRiskEvent(
        risk_event_id=risk_event_id,
        observation_id=observation.observation_id,
        usage_event_id=observation.usage_event_id,
        runtime_load_id=observation.runtime_load_id,
        package_id=observation.package_id,
        package_version=observation.package_version,
        severity=request.severity,
        risk_type=request.risk_type,
        risk_summary=request.risk_summary,
        immediate_action_required=request.immediate_action_required,
        suggested_action=request.suggested_action,
        created_at=datetime.now(UTC).isoformat(),
        audit_id=f"{risk_event_id}_audit",
        source_trace_id=source_trace.source_trace_id,
        audit_events=[audit_event],
        source_trace=source_trace,
        warnings=[
            "Risk event is metadata-only.",
            "Risk event does not automatically disable, rollback, replace, train, publish, or deliver packages.",
        ],
        **v731h_safety_flags(),
    )
    write_feedback_risk_event(risk_event)
    return risk_event.model_dump()


def list_practice_risk_events() -> dict:
    return list_feedback_risk_events()


def get_practice_risk_event(risk_event_id: str) -> dict | None:
    return get_risk_event(risk_event_id)
