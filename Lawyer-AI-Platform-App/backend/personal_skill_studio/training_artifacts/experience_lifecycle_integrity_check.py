from datetime import UTC, datetime

from personal_skill_studio.training_artifacts.experience_lifecycle_safety_engine import (
    lifecycle_metadata_safe,
    v732_safety_flags,
)
from personal_skill_studio.training_artifacts.schemas import ExperienceLifecycleIntegrityCheck, ExperienceLifecycleRecord


def build_integrity_check(record: ExperienceLifecycleRecord) -> ExperienceLifecycleIntegrityCheck:
    passed: list[str] = []
    failed: list[str] = []

    _check(bool(record.practice_load_review_ids) or not record.runtime_load_ids, "loaded package has load review lineage", passed, failed)
    _check(bool(record.latest_lawyer_approved_package_id) or not record.runtime_load_ids, "loaded package is lawyer-approved", passed, failed)
    _check(all(event.audit_id for event in record.stage_events), "critical stages have audit ids", passed, failed)
    _check(all(event.source_trace_id for event in record.stage_events), "critical stages have source trace ids", passed, failed)
    _check(record.feedback_does_not_mutate_loaded_package, "feedback does not mutate loaded package", passed, failed)
    _check(record.next_package_requires_load_review, "next package requires load review", passed, failed)
    _check(lifecycle_metadata_safe(record.model_dump()), "lifecycle response metadata-safe scan", passed, failed)

    status = "passed" if not failed else "failed"
    return ExperienceLifecycleIntegrityCheck(
        integrity_check_id=f"{record.lifecycle_id}_integrity_check",
        lifecycle_id=record.lifecycle_id,
        status=status,
        passed_checks=passed,
        failed_checks=failed,
        warnings=["Integrity check inspects lifecycle metadata links only."],
        blocked_reason="; ".join(failed) if failed else None,
        recommended_actions=[] if not failed else ["recompute lifecycle after completing missing review, audit, or trace metadata"],
        created_at=datetime.now(UTC).isoformat(),
        **v732_safety_flags(),
    )


def _check(condition: bool, label: str, passed: list[str], failed: list[str]) -> None:
    if condition:
        passed.append(label)
    else:
        failed.append(label)
