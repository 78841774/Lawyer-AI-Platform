from datetime import UTC, datetime

from personal_skill_studio.training_artifacts.experience_lifecycle_safety_engine import v732_safety_flags
from personal_skill_studio.training_artifacts.schemas import ExperienceLifecycleStageEvent


STAGE_ORDER = [
    "raw_work_product_controlled_processing",
    "ocr_document_parse",
    "legal_retrieval",
    "experience_candidate_generation",
    "experience_redaction_abstraction",
    "skill_experience_pool",
    "skill_draft_build",
    "skill_package_versioning",
    "system_validation_gate",
    "internal_training_task_build",
    "experience_package_build",
    "practice_load_review",
    "lawyer_experience_editing",
    "lawyer_approved_package",
    "practice_runtime_loading",
    "runtime_policy_evaluation",
    "runtime_usage_monitoring",
    "output_observation",
    "lawyer_feedback",
    "risk_event",
    "feedback_candidate_pack",
    "next_experience_package_draft",
    "pending_next_practice_load_review",
]


def build_stage_event(
    lifecycle_id: str,
    stage_name: str,
    stage_status: str,
    linked_object_type: str,
    linked_object_id: str | None,
    previous_stage_event_id: str | None,
    allowed_actions: list[str],
    source_trace_id: str | None = None,
    blocked_reason: str | None = None,
) -> ExperienceLifecycleStageEvent:
    return ExperienceLifecycleStageEvent(
        stage_event_id=f"{lifecycle_id}_{stage_name}",
        lifecycle_id=lifecycle_id,
        stage_name=stage_name,
        stage_status=stage_status,
        linked_object_type=linked_object_type,
        linked_object_id=linked_object_id,
        previous_stage_event_id=previous_stage_event_id,
        next_stage_candidates=_next_stage_candidates(stage_name),
        allowed_actions=allowed_actions,
        blocked_reason=blocked_reason,
        safety_flags=["metadata_only", "source_trace_required", "audit_required"],
        audit_id=f"{lifecycle_id}_{stage_name}_audit",
        source_trace_id=source_trace_id or f"{lifecycle_id}_{stage_name}_source_trace",
        created_at=datetime.now(UTC).isoformat(),
        **v732_safety_flags(),
    )


def _next_stage_candidates(stage_name: str) -> list[str]:
    if stage_name not in STAGE_ORDER:
        return []
    index = STAGE_ORDER.index(stage_name)
    return STAGE_ORDER[index + 1:index + 2]
