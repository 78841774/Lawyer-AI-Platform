from datetime import UTC, datetime

from personal_skill_studio.training_artifacts.practice_feedback_audit_engine import build_feedback_audit_event
from personal_skill_studio.training_artifacts.practice_feedback_classifier import classify_feedback
from personal_skill_studio.training_artifacts.practice_feedback_registry import (
    get_feedback,
    get_feedback_record,
    get_observation_record,
    list_feedback,
    write_feedback,
)
from personal_skill_studio.training_artifacts.practice_feedback_safety_engine import (
    feedback_metadata_safe,
    v731h_safety_flags,
)
from personal_skill_studio.training_artifacts.practice_feedback_source_trace_engine import build_feedback_source_trace
from personal_skill_studio.training_artifacts.schemas import (
    PracticeFeedbackTriageRequest,
    PracticeLawyerFeedback,
    PracticeLawyerFeedbackRequest,
)


def create_lawyer_feedback(request: PracticeLawyerFeedbackRequest) -> dict | None:
    observation = get_observation_record(request.observation_id)
    if observation is None or not feedback_metadata_safe(request.model_dump()):
        return None
    feedback_id = f"practice_feedback_{datetime.now(UTC).strftime('%Y%m%d%H%M%S%f')}"
    classification = classify_feedback(request.feedback_type, request.severity)
    source_trace = build_feedback_source_trace(
        object_id=feedback_id,
        source_trace_type="practice_lawyer_feedback",
        usage_event_id=observation.usage_event_id,
        runtime_load_id=observation.runtime_load_id,
        package_id=observation.package_id,
    )
    audit_event = build_feedback_audit_event(
        object_id=feedback_id,
        object_type="practice_lawyer_feedback",
        action="lawyer_feedback_submitted",
        actor_id=request.created_by,
        actor_note="lawyer feedback metadata submitted",
    )
    feedback = PracticeLawyerFeedback(
        feedback_id=feedback_id,
        observation_id=observation.observation_id,
        usage_event_id=observation.usage_event_id,
        runtime_load_id=observation.runtime_load_id,
        package_id=observation.package_id,
        package_version=observation.package_version,
        feedback_type=request.feedback_type,
        feedback_summary=request.feedback_summary,
        suggested_change=request.suggested_change,
        severity=classification.severity,
        applies_to_experience_card_id=request.applies_to_experience_card_id,
        applies_to_usage_boundary=request.applies_to_usage_boundary,
        created_by=request.created_by,
        created_at=datetime.now(UTC).isoformat(),
        audit_id=f"{feedback_id}_audit",
        source_trace_id=source_trace.source_trace_id,
        classification=classification,
        audit_events=[audit_event],
        source_trace=source_trace,
        warnings=[
            "Lawyer feedback is metadata-only.",
            "Feedback does not automatically disable, rollback, mutate, train, or publish packages.",
        ],
        **v731h_safety_flags(),
    )
    write_feedback(feedback)
    return feedback.model_dump()


def list_lawyer_feedback() -> dict:
    return list_feedback()


def get_lawyer_feedback(feedback_id: str) -> dict | None:
    return get_feedback(feedback_id)


def triage_lawyer_feedback(feedback_id: str, request: PracticeFeedbackTriageRequest) -> dict | None:
    feedback = get_feedback_record(feedback_id)
    if feedback is None or not feedback_metadata_safe(request.model_dump()):
        return None
    updated = feedback.model_copy(deep=True)
    updated.feedback_status = request.feedback_status
    updated.classification = classify_feedback(updated.feedback_type, updated.severity)
    updated.audit_events.append(
        build_feedback_audit_event(
            object_id=feedback_id,
            object_type="practice_lawyer_feedback",
            action=f"lawyer_feedback_{request.feedback_status}",
            actor_id=request.triaged_by,
            actor_note=request.triage_note,
        )
    )
    updated.warnings = [
        "Triage is metadata-only.",
        "Triage recommendations do not automatically mutate loaded packages or execute disable/rollback.",
    ]
    write_feedback(updated)
    return updated.model_dump()
