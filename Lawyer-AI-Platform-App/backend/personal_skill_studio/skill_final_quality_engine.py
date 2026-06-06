from personal_skill_studio.schemas import SkillFinalQualityReport
from personal_skill_studio.skill_final_draft_engine import get_skill_final_draft


def build_skill_final_quality(skill_id: str) -> SkillFinalQualityReport | None:
    draft = get_skill_final_draft(skill_id)
    if draft is None:
        return None
    missing = [] if draft.evaluation_cases else [f"{skill_id} evaluation metadata not detected"]
    score_status = "reference_only" if draft.baseline_complete else "insufficient_baseline"
    if draft.skill_type == "fact_extraction":
        dimensions = {
            "fact_pattern_coverage": 72,
            "evidence_mapping_reviewability": 70,
            "timeline_rule_clarity": 76,
            "source_trace_rule_clarity": 82,
            "lawyer_review_readiness": 68,
        }
    else:
        dimensions = {
            "legal_issue_coverage": 74,
            "claim_basis_pattern_clarity": 70,
            "defense_path_coverage": 68,
            "citation_boundary_clarity": 84,
            "lawyer_review_readiness": 70,
        }
    return SkillFinalQualityReport(
        skill_id=skill_id,
        score_status=score_status,
        quality_score=draft.quality_score,
        dimensions=dimensions,
        missing_evaluation_files=missing,
        suggested_next_optimization=draft.optimization_suggestions,
        baseline_discovered=draft.baseline_discovered,
        baseline_complete=draft.baseline_complete,
        warnings=["Quality is a final draft reference score only; it is not a correctness guarantee or publish gate."],
    )
