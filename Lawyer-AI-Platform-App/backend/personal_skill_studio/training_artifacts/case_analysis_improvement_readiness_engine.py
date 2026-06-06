from datetime import UTC, datetime

from personal_skill_studio.training_artifacts.case_analysis_improvement_safety_engine import (
    case_analysis_improvement_metadata_safe,
    v734_safety_flags,
)
from personal_skill_studio.training_artifacts.schemas import (
    CaseAnalysisImprovementCandidate,
    CaseAnalysisImprovementReadinessReport,
)


def build_readiness_report(candidate: CaseAnalysisImprovementCandidate) -> CaseAnalysisImprovementReadinessReport:
    passed: list[str] = []
    failed: list[str] = []
    warnings: list[str] = []

    _require(bool(candidate.source_output_id), "source output linked", passed, failed)
    _require(bool(candidate.source_trace_id), "candidate source trace linked", passed, failed)
    _require(bool(candidate.audit_id), "candidate audit linked", passed, failed)
    _require(bool(candidate.source_feedback_ids or candidate.source_risk_event_ids), "feedback or risk source retained", passed, failed)
    _require(case_analysis_improvement_metadata_safe(candidate.model_dump()), "sensitive marker scan passed", passed, failed)
    _require(candidate.loaded_package_auto_mutated is False, "loaded package unchanged", passed, failed)
    _require(candidate.training_triggered is False, "training not triggered", passed, failed)
    _require(bool(candidate.training_relevance), "training relevance labelled", passed, failed)
    _require(bool(candidate.practice_relevance), "practice relevance labelled", passed, failed)

    if candidate.candidate_status == "archived":
        failed.append("candidate is archived")
    if candidate.trace_status if hasattr(candidate, "trace_status") else False:
        warnings.append("Trace status is carried in output trace records.")

    status = "ready_for_training_dataset_build" if not failed and candidate.readiness_status == "ready_for_training_dataset_build" else "ready_for_candidate_pack"
    if failed:
        status = "blocked" if any("sensitive" in item or "audit" in item or "source trace" in item for item in failed) else "not_ready"

    return CaseAnalysisImprovementReadinessReport(
        readiness_report_id=f"{candidate.candidate_id}_readiness_v734",
        candidate_id=candidate.candidate_id,
        status=status,
        passed_checks=passed,
        failed_checks=failed,
        warnings=warnings or ["Readiness is metadata-only and requires a later dataset gate before training use."],
        blocked_reason="; ".join(failed) if failed else None,
        recommended_next_action=_recommended_next_action(status),
        created_at=datetime.now(UTC).isoformat(),
        audit_id=f"{candidate.candidate_id}_readiness_audit",
        **v734_safety_flags(),
    )


def can_mark_ready(candidate: CaseAnalysisImprovementCandidate) -> bool:
    report = build_readiness_report(candidate)
    return report.status in {"ready_for_candidate_pack", "ready_for_training_dataset_build"} and not report.failed_checks


def _require(condition: bool, label: str, passed: list[str], failed: list[str]) -> None:
    if condition:
        passed.append(label)
    else:
        failed.append(label)


def _recommended_next_action(status: str) -> str:
    if status == "ready_for_training_dataset_build":
        return "Keep candidate for v7.35 dataset builder and training gate review."
    if status == "ready_for_candidate_pack":
        return "Review candidate metadata before marking it ready for v7.35."
    if status == "blocked":
        return "Resolve missing trace, audit, or safety metadata before any later use."
    return "Collect more lawyer feedback or risk metadata."
