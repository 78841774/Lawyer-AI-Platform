from datetime import UTC, datetime
from uuid import uuid4

from personal_skill_studio.training_artifacts.schemas import (
    SkillPackage,
    TrainingPackageAuditEvent,
    TrainingSample,
    TrainingTask,
    TrainingTaskBuildRequest,
)
from personal_skill_studio.training_artifacts.storage import SKILL_PACKAGES_DIR, read_payload, read_payloads


def v731e_safety_flags() -> dict[str, bool | str]:
    return {
        "owner_only": True,
        "local_private_processing_only": True,
        "system_validated_package_required": True,
        "approved_experience_only": True,
        "redacted_output_only": True,
        "abstracted_experience_only": True,
        "structured_training_metadata_only": True,
        "practice_load_review_required_later": True,
        "training_output_manual_review_status": "not_applicable",
        "practice_load_review_status": "pending_practice_load_review",
        "source_trace_required": True,
        "audit_required": True,
        "provider_call_executed": False,
        "key_value_read": False,
        "credential_value_returned": False,
        "provider_result_payload_returned": False,
        "source_content_returned": False,
        "source_material_returned": False,
        "non_validated_package_used": False,
        "unreviewed_experience_used": False,
        "unsafe_experience_used": False,
        "missing_source_trace_used": False,
        "real_codex_training_triggered": False,
        "formal_training_set_written": False,
        "skill_updated": False,
        "skill_published": False,
        "skill_publishable": False,
        "final_legal_opinion_generated": False,
        "final_report_generated": False,
        "public_link_created": False,
        "email_sent": False,
        "external_delivery_triggered": False,
    }


def build_internal_training_task(request: TrainingTaskBuildRequest) -> TrainingTask | None:
    package = _resolve_system_validated_package(request.source_skill_package_id)
    if package is None:
        return None

    now = datetime.now(UTC).isoformat()
    training_task_id = f"internal_training_task_v731e_{uuid4().hex[:10]}"
    samples = [
        _build_sample(training_task_id, package, experience_id, now)
        for experience_id in package.experience_ids
    ]
    audit_events = [
        _build_audit_event(training_task_id, "training_task_created"),
        _build_audit_event(training_task_id, "training_completed"),
    ]
    return TrainingTask(
        training_task_id=training_task_id,
        task_name=request.task_name,
        source_skill_package_id=package.package_id,
        source_draft_id=package.source_draft_id,
        source_manifest_id=package.manifest_id,
        source_trace_bundle_id=package.source_trace_bundle_id,
        source_audit_bundle_id=package.audit_bundle_id,
        source_experience_ids=package.experience_ids,
        sample_count=len(samples),
        samples=samples,
        audit_events=audit_events,
        created_at=now,
        updated_at=now,
        warnings=[
            "Internal training task is structured metadata only.",
            "Training output manual review is not applicable in v7.31e; practice load review is deferred to v7.31f.",
        ],
        **v731e_safety_flags(),
    )


def _build_sample(training_task_id: str, package: SkillPackage, experience_id: str, now: str) -> TrainingSample:
    sample_id = f"training_sample_v731e_{uuid4().hex[:10]}"
    return TrainingSample(
        sample_id=sample_id,
        source_skill_package_id=package.package_id,
        source_draft_id=package.source_draft_id,
        source_experience_id=experience_id,
        source_trace_ids=package.source_trace_bundle.source_trace_ids,
        prompt_template="根据脱敏经验 metadata 生成结构化办案经验要点。",
        input_metadata={
            "training_task_id": training_task_id,
            "source_skill_package_id": package.package_id,
            "source_draft_id": package.source_draft_id,
            "source_experience_id": experience_id,
            "package_version": package.package_version,
        },
        expected_output_metadata={
            "experience_summary": "abstracted_experience_metadata",
            "fact_pattern": "structured_fact_pattern_metadata",
            "issue_pattern": "structured_issue_pattern_metadata",
            "evidence_pattern": "structured_evidence_pattern_metadata",
            "risk_warning": "structured_risk_warning_metadata",
            "practice_load_review_status": "pending_practice_load_review",
        },
        input_output_pair_id=f"{sample_id}_pair",
        created_at=now,
        **v731e_safety_flags(),
    )


def _build_audit_event(artifact_id: str, action: str) -> TrainingPackageAuditEvent:
    return TrainingPackageAuditEvent(
        event_id=f"{artifact_id}_audit_{action}_{datetime.now(UTC).strftime('%Y%m%d%H%M%S%f')}",
        artifact_id=artifact_id,
        action=action,
        timestamp=datetime.now(UTC).isoformat(),
    )


def _resolve_system_validated_package(package_id: str | None) -> SkillPackage | None:
    if package_id:
        payload = read_payload(SKILL_PACKAGES_DIR, package_id)
        package = SkillPackage(**payload) if payload else None
        return package if package and _system_validated(package) else None
    packages = [SkillPackage(**payload) for payload in reversed(read_payloads(SKILL_PACKAGES_DIR))]
    return next((package for package in packages if _system_validated(package)), None)


def _system_validated(package: SkillPackage) -> bool:
    return (
        package.pre_publish_gate_status == "system_validated"
        and package.package_status == "ready_for_training_package_build"
        and bool(package.validation_result)
        and bool(package.validation_result.gate_passed)
        and bool(package.experience_ids)
    )
