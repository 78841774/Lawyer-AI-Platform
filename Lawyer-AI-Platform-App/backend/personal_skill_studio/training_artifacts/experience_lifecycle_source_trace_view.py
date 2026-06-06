from datetime import UTC, datetime

from personal_skill_studio.training_artifacts.experience_lifecycle_safety_engine import v732_safety_flags
from personal_skill_studio.training_artifacts.schemas import ExperienceLifecycleRecord, ExperienceLifecycleSourceTraceView


def build_source_trace_view(record: ExperienceLifecycleRecord) -> ExperienceLifecycleSourceTraceView:
    missing = []
    for event in record.stage_events:
        if not event.source_trace_id:
            missing.append(f"missing trace for {event.stage_name}")
    return ExperienceLifecycleSourceTraceView(
        source_trace_view_id=f"{record.lifecycle_id}_source_trace_view",
        lifecycle_id=record.lifecycle_id,
        root_source_trace_id=record.source_trace_root_id,
        material_trace_summary=record.source_candidate_ids[:8],
        ocr_trace_summary=[event.linked_object_id for event in record.stage_events if event.stage_name == "ocr_document_parse" and event.linked_object_id],
        legal_retrieval_trace_summary=[event.linked_object_id for event in record.stage_events if event.stage_name == "legal_retrieval" and event.linked_object_id],
        experience_candidate_trace_summary=record.source_candidate_ids[:8],
        skill_draft_trace_summary=record.skill_draft_ids[:8],
        skill_package_trace_summary=record.skill_package_ids[:8],
        training_package_trace_summary=record.experience_package_ids[:8],
        practice_load_trace_summary=record.practice_load_review_ids[:8],
        runtime_usage_trace_summary=record.usage_event_ids[:8],
        feedback_trace_summary=record.feedback_ids[:8],
        next_package_trace_summary=record.next_package_ids[:8],
        missing_trace_warnings=missing,
        created_at=datetime.now(UTC).isoformat(),
        **v732_safety_flags(),
    )
