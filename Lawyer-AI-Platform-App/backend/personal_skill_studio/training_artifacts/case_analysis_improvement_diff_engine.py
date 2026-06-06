from datetime import UTC, datetime

from personal_skill_studio.training_artifacts.case_analysis_improvement_safety_engine import v734_safety_flags
from personal_skill_studio.training_artifacts.schemas import CaseAnalysisImprovementCandidate, CaseAnalysisImprovementDiff


def build_improvement_diff(candidates: list[CaseAnalysisImprovementCandidate]) -> CaseAnalysisImprovementDiff:
    now = datetime.now(UTC).isoformat()
    active = [candidate for candidate in candidates if candidate.candidate_status != "archived"]
    package_id = active[0].source_package_id if active else "package_pending"
    package_version = active[0].source_package_version if active else "version_pending"
    ready_count = sum(1 for candidate in active if candidate.readiness_status == "ready_for_training_dataset_build")
    return CaseAnalysisImprovementDiff(
        diff_id=f"case_analysis_improvement_diff_{now.replace(':', '').replace('.', '')}",
        candidate_ids=[candidate.candidate_id for candidate in active],
        source_package_id=package_id,
        source_package_version=package_version,
        target_next_package_version_hint=f"{package_version}.next-v734",
        added_cards_count=_count(active, {"add_experience_card"}),
        revised_cards_count=_count(active, {"revise_experience_card", "revise_legal_analysis_prompt_hint", "revise_fact_extraction_prompt_hint"}),
        deleted_cards_count=_count(active, {"delete_experience_card"}),
        boundary_changes_count=_count(active, {"narrow_usage_boundary", "expand_usage_boundary"}),
        risk_warning_changes_count=_count(active, {"add_risk_warning", "revise_risk_warning", "mark_output_as_high_risk"}),
        schema_metadata_changes_count=_count(active, {"revise_output_schema_metadata", "revise_output_order", "revise_output_title"}),
        training_update_recommendations_count=_count(active, {"suggest_training_dataset_update", "suggest_next_package_version"}),
        disable_recommendations_count=_count(active, {"suggest_package_disable"}),
        rollback_recommendations_count=_count(active, {"suggest_package_rollback"}),
        diff_summary=f"{len(active)} improvement candidates summarized for later human review; no package or schema change was applied.",
        risk_summary=_risk_summary(active),
        readiness_status="ready_for_training_dataset_build" if active and ready_count == len(active) else "ready_for_candidate_pack",
        audit_id=f"case_analysis_improvement_diff_audit_{now.replace(':', '').replace('.', '')}",
        source_trace_id=f"case_analysis_improvement_diff_source_trace_{now.replace(':', '').replace('.', '')}",
        created_at=now,
        warnings=["Diff is a summary only and is not applied to packages, runtime loads, schemas, or training artifacts."],
        **v734_safety_flags(),
    )


def _count(candidates: list[CaseAnalysisImprovementCandidate], candidate_types: set[str]) -> int:
    return sum(1 for candidate in candidates if candidate.candidate_type in candidate_types)


def _risk_summary(candidates: list[CaseAnalysisImprovementCandidate]) -> str:
    high = sum(1 for candidate in candidates if candidate.candidate_severity in {"high", "critical"})
    disable = sum(1 for candidate in candidates if candidate.candidate_type == "suggest_package_disable")
    rollback = sum(1 for candidate in candidates if candidate.candidate_type == "suggest_package_rollback")
    return f"{high} high-or-critical candidates, {disable} disable recommendations, {rollback} rollback recommendations; all remain advisory metadata."
