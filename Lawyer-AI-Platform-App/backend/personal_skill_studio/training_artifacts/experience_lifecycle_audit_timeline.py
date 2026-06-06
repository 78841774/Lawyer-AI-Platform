from datetime import UTC, datetime

from personal_skill_studio.training_artifacts.experience_lifecycle_safety_engine import v732_safety_flags
from personal_skill_studio.training_artifacts.schemas import ExperienceLifecycleAuditEventView, ExperienceLifecycleAuditTimeline, ExperienceLifecycleRecord


def build_audit_timeline(record: ExperienceLifecycleRecord) -> ExperienceLifecycleAuditTimeline:
    events = [
        ExperienceLifecycleAuditEventView(
            audit_event_id=event.audit_id,
            lifecycle_id=record.lifecycle_id,
            event_type=_event_type(event.stage_name),
            stage_name=event.stage_name,
            linked_object_type=event.linked_object_type,
            linked_object_id=event.linked_object_id,
            actor="system_metadata_aggregator",
            timestamp=event.created_at,
            summary=f"{event.stage_name} status: {event.stage_status}",
            safety_flags=event.safety_flags,
            source_trace_id=event.source_trace_id,
            **v732_safety_flags(),
        )
        for event in record.stage_events
    ]
    latest = max((event.timestamp for event in events), default=datetime.now(UTC).isoformat())
    return ExperienceLifecycleAuditTimeline(
        audit_timeline_id=record.audit_timeline_id,
        lifecycle_id=record.lifecycle_id,
        events=events,
        events_count=len(events),
        latest_event_at=latest,
        risk_events_count=len(record.risk_event_ids),
        blocked_events_count=sum(1 for event in record.stage_events if event.stage_status == "blocked"),
        manual_load_review_events_count=sum(1 for event in record.stage_events if "load_review" in event.stage_name),
        runtime_events_count=sum(1 for event in record.stage_events if event.stage_name.startswith("runtime") or "runtime" in event.stage_name),
        feedback_events_count=len(record.feedback_ids),
        warnings=["Timeline summarizes metadata events only."],
        **v732_safety_flags(),
    )


def _event_type(stage_name: str) -> str:
    return {
        "practice_load_review": "practice_load_review_started",
        "lawyer_approved_package": "practice_load_approved",
        "practice_runtime_loading": "runtime_package_loaded",
        "output_observation": "output_observed",
        "lawyer_feedback": "lawyer_feedback_submitted",
        "risk_event": "risk_event_created",
        "feedback_candidate_pack": "candidate_pack_built",
        "next_experience_package_draft": "next_package_rebuilt",
    }.get(stage_name, f"{stage_name}_metadata")
