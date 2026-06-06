from datetime import UTC, datetime
from uuid import uuid4

from personal_skill_studio.training_artifacts.internal_training_task_builder import v731e_safety_flags
from personal_skill_studio.training_artifacts.schemas import (
    ExperiencePackage,
    ExperiencePackageBuildRequest,
    TrainingPackageAuditEvent,
    TrainingPackageSourceTraceBundle,
    TrainingTask,
)
from personal_skill_studio.training_artifacts.storage import INTERNAL_TRAINING_TASKS_DIR, read_payload, read_payloads


def build_experience_package(request: ExperiencePackageBuildRequest) -> ExperiencePackage | None:
    task = _resolve_training_task(request.source_training_task_id, request.source_skill_package_id)
    if task is None or task.training_task_status != "training_completed":
        return None

    now = datetime.now(UTC).isoformat()
    package_id = f"training_package_v731e_{uuid4().hex[:10]}"
    source_trace_bundle = TrainingPackageSourceTraceBundle(
        source_trace_bundle_id=f"{package_id}_source_trace_bundle",
        artifact_id=package_id,
        source_skill_package_id=task.source_skill_package_id,
        source_training_task_id=task.training_task_id,
        source_trace_ids=sorted({trace_id for sample in task.samples for trace_id in sample.source_trace_ids}),
        source_experience_ids=task.source_experience_ids,
        source_draft_id=task.source_draft_id,
        trace_count=len({trace_id for sample in task.samples for trace_id in sample.source_trace_ids}),
        warnings=["Source trace bundle contains metadata identifiers only."],
        **v731e_safety_flags(),
    )
    audit_events = [
        _build_audit_event(package_id, "experience_package_built"),
        _build_audit_event(package_id, "pending_practice_load_review"),
    ]
    return ExperiencePackage(
        package_id=package_id,
        package_name=request.package_name,
        package_version=request.package_version,
        source_training_task_id=task.training_task_id,
        source_skill_package_id=task.source_skill_package_id,
        source_draft_id=task.source_draft_id,
        source_experience_ids=task.source_experience_ids,
        source_trace_bundle_id=source_trace_bundle.source_trace_bundle_id,
        audit_bundle_id=f"{package_id}_audit_bundle",
        sample_count=len(task.samples),
        samples=task.samples,
        source_trace_bundle=source_trace_bundle,
        audit_events=audit_events,
        created_at=now,
        updated_at=now,
        warnings=[
            "Experience package is structured internal training metadata only.",
            "Practice runtime loading requires v7.31f review before use.",
        ],
        **v731e_safety_flags(),
    )


def _resolve_training_task(training_task_id: str | None, source_skill_package_id: str | None) -> TrainingTask | None:
    if training_task_id:
        payload = read_payload(INTERNAL_TRAINING_TASKS_DIR, training_task_id)
        return TrainingTask(**payload) if payload else None
    tasks = [TrainingTask(**payload) for payload in reversed(read_payloads(INTERNAL_TRAINING_TASKS_DIR))]
    if source_skill_package_id:
        return next((task for task in tasks if task.source_skill_package_id == source_skill_package_id), None)
    return next((task for task in tasks if task.training_task_status == "training_completed"), None)


def _build_audit_event(artifact_id: str, action: str) -> TrainingPackageAuditEvent:
    return TrainingPackageAuditEvent(
        event_id=f"{artifact_id}_audit_{action}_{datetime.now(UTC).strftime('%Y%m%d%H%M%S%f')}",
        artifact_id=artifact_id,
        action=action,
        timestamp=datetime.now(UTC).isoformat(),
    )
