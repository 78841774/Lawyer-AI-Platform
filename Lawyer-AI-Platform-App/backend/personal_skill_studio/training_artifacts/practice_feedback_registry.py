from collections import Counter

from personal_skill_studio.training_artifacts.practice_feedback_safety_engine import v731h_safety_flags
from personal_skill_studio.training_artifacts.schemas import (
    PracticeFeedbackRiskEvent,
    PracticeFeedbackRiskEventList,
    PracticeFeedbackSummary,
    PracticeLawyerFeedback,
    PracticeLawyerFeedbackList,
    PracticeOutputObservation,
    PracticeOutputObservationList,
    V731hPracticeFeedbackStatus,
)
from personal_skill_studio.training_artifacts.storage import (
    PRACTICE_FEEDBACK_RISK_EVENTS_DIR,
    PRACTICE_LAWYER_FEEDBACK_DIR,
    PRACTICE_OUTPUT_OBSERVATIONS_DIR,
    read_payload,
    read_payloads,
    write_payload,
)


def write_observation(observation: PracticeOutputObservation) -> None:
    write_payload(PRACTICE_OUTPUT_OBSERVATIONS_DIR, observation.observation_id, observation.model_dump())


def write_feedback(feedback: PracticeLawyerFeedback) -> None:
    write_payload(PRACTICE_LAWYER_FEEDBACK_DIR, feedback.feedback_id, feedback.model_dump())


def write_feedback_risk_event(risk_event: PracticeFeedbackRiskEvent) -> None:
    write_payload(PRACTICE_FEEDBACK_RISK_EVENTS_DIR, risk_event.risk_event_id, risk_event.model_dump())


def get_observation_record(observation_id: str) -> PracticeOutputObservation | None:
    payload = read_payload(PRACTICE_OUTPUT_OBSERVATIONS_DIR, observation_id)
    return PracticeOutputObservation(**payload) if payload else None


def get_feedback_record(feedback_id: str) -> PracticeLawyerFeedback | None:
    payload = read_payload(PRACTICE_LAWYER_FEEDBACK_DIR, feedback_id)
    return PracticeLawyerFeedback(**payload) if payload else None


def get_risk_event_record(risk_event_id: str) -> PracticeFeedbackRiskEvent | None:
    payload = read_payload(PRACTICE_FEEDBACK_RISK_EVENTS_DIR, risk_event_id)
    return PracticeFeedbackRiskEvent(**payload) if payload else None


def get_observation(observation_id: str) -> dict | None:
    record = get_observation_record(observation_id)
    return record.model_dump() if record else None


def get_feedback(feedback_id: str) -> dict | None:
    record = get_feedback_record(feedback_id)
    return record.model_dump() if record else None


def get_risk_event(risk_event_id: str) -> dict | None:
    record = get_risk_event_record(risk_event_id)
    return record.model_dump() if record else None


def list_observation_records() -> list[PracticeOutputObservation]:
    records = [
        PracticeOutputObservation(**payload)
        for payload in read_payloads(PRACTICE_OUTPUT_OBSERVATIONS_DIR)
        if payload.get("observation_id")
    ]
    return sorted(records, key=lambda item: item.generated_at, reverse=True)


def list_feedback_records() -> list[PracticeLawyerFeedback]:
    records = [
        PracticeLawyerFeedback(**payload)
        for payload in read_payloads(PRACTICE_LAWYER_FEEDBACK_DIR)
        if payload.get("feedback_id")
    ]
    return sorted(records, key=lambda item: item.created_at, reverse=True)


def list_feedback_risk_event_records() -> list[PracticeFeedbackRiskEvent]:
    records = [
        PracticeFeedbackRiskEvent(**payload)
        for payload in read_payloads(PRACTICE_FEEDBACK_RISK_EVENTS_DIR)
        if payload.get("risk_event_id")
    ]
    return sorted(records, key=lambda item: item.created_at, reverse=True)


def list_observations() -> dict:
    observations = list_observation_records()
    return PracticeOutputObservationList(
        observations=observations,
        observation_count=len(observations),
        warnings=["Output observations are redacted metadata only; no raw output is stored."],
        **v731h_safety_flags(),
    ).model_dump()


def list_feedback() -> dict:
    feedback_items = list_feedback_records()
    return PracticeLawyerFeedbackList(
        feedback_items=feedback_items,
        feedback_count=len(feedback_items),
        submitted_count=sum(1 for item in feedback_items if item.feedback_status == "submitted"),
        triaged_count=sum(1 for item in feedback_items if item.feedback_status == "triaged"),
        accepted_as_candidate_count=sum(1 for item in feedback_items if item.feedback_status == "accepted_as_candidate"),
        warnings=["Lawyer feedback is metadata-only and does not mutate runtime packages."],
        **v731h_safety_flags(),
    ).model_dump()


def list_feedback_risk_events() -> dict:
    risk_events = list_feedback_risk_event_records()
    return PracticeFeedbackRiskEventList(
        risk_events=risk_events,
        risk_event_count=len(risk_events),
        high_severity_count=sum(1 for item in risk_events if item.severity in {"high", "critical"}),
        immediate_action_required_count=sum(1 for item in risk_events if item.immediate_action_required),
        warnings=["Risk events recommend review only; disable and rollback remain manual v7.31g controls."],
        **v731h_safety_flags(),
    ).model_dump()


def build_feedback_summary() -> dict:
    observations = list_observation_records()
    feedback_items = list_feedback_records()
    risk_events = list_feedback_risk_event_records()
    feedback_type_counts = Counter(item.feedback_type for item in feedback_items)
    risk_type_counts = Counter(item.risk_type for item in risk_events)
    return PracticeFeedbackSummary(
        observation_count=len(observations),
        feedback_count=len(feedback_items),
        risk_event_count=len(risk_events),
        triaged_feedback_count=sum(1 for item in feedback_items if item.feedback_status == "triaged"),
        iteration_candidate_recommended_count=sum(
            1 for item in feedback_items if item.classification.create_iteration_candidate_recommended
        ),
        auto_disable_recommended_count=sum(1 for item in feedback_items if item.classification.auto_disable_recommended),
        rollback_recommended_count=sum(1 for item in feedback_items if item.classification.rollback_recommended),
        immediate_action_required_count=sum(1 for item in risk_events if item.immediate_action_required),
        package_ids=sorted({item.package_id for item in [*observations, *feedback_items, *risk_events]}),
        runtime_load_ids=sorted({item.runtime_load_id for item in [*observations, *feedback_items, *risk_events]}),
        feedback_type_counts=dict(feedback_type_counts),
        risk_type_counts=dict(risk_type_counts),
        warnings=[
            "Feedback summary is candidate input for v7.31i only.",
            "It does not disable, rollback, replace, train, publish, or externally deliver any package.",
        ],
        **v731h_safety_flags(),
    ).model_dump()


def build_v731h_status() -> dict:
    observations = list_observation_records()
    feedback_items = list_feedback_records()
    risk_events = list_feedback_risk_event_records()
    return V731hPracticeFeedbackStatus(
        observation_count=len(observations),
        feedback_count=len(feedback_items),
        risk_event_count=len(risk_events),
        triaged_feedback_count=sum(1 for item in feedback_items if item.feedback_status == "triaged"),
        warnings=[
            "v7.31h observes output metadata and collects lawyer feedback only.",
            "Feedback does not automatically mutate loaded packages, update Skills, trigger training, disable, or rollback.",
        ],
        **v731h_safety_flags(),
    ).model_dump()
