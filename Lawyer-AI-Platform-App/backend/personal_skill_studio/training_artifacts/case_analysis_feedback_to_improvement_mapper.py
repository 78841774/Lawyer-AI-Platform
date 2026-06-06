from personal_skill_studio.training_artifacts.schemas import CaseAnalysisImprovementCandidate


SEVERITY_ORDER = {"low": 1, "medium": 2, "high": 3, "critical": 4}

FEEDBACK_RULES: dict[str, tuple[str, str, str, str]] = {
    "inaccurate": ("revise_experience_card", "revise", "experience_card", "medium"),
    "over_generalized": ("narrow_usage_boundary", "narrow", "usage_boundary", "medium"),
    "too_narrow": ("expand_usage_boundary", "expand", "usage_boundary", "low"),
    "missing_risk_warning": ("add_risk_warning", "warn", "risk_warning", "medium"),
    "wrong_usage_boundary": ("narrow_usage_boundary", "narrow", "usage_boundary", "high"),
    "unsafe_output": ("mark_output_as_high_risk", "warn", "case_analysis_output", "high"),
    "hallucinated_law": ("mark_output_as_high_risk", "warn", "case_analysis_output", "critical"),
    "unclear_reasoning": ("revise_legal_analysis_prompt_hint", "revise", "case_analysis_output", "medium"),
    "needs_editorial_revision": ("revise_experience_card", "revise", "experience_card", "low"),
    "should_create_next_version": ("suggest_next_package_version", "next_version_recommendation", "experience_package", "medium"),
    "schema_output_feedback": ("revise_experience_card", "revise", "experience_card", "low"),
    "improvement_suggestion": ("revise_experience_card", "revise", "experience_card", "low"),
}

RISK_RULES: dict[str, tuple[str, str, str, str]] = {
    "hallucinated_law": ("mark_output_as_high_risk", "warn", "case_analysis_output", "critical"),
    "sensitive_content_risk": ("suggest_package_disable", "disable_recommendation", "runtime_load", "high"),
    "usage_boundary_violation": ("narrow_usage_boundary", "narrow", "usage_boundary", "high"),
    "output_quality_issue": ("revise_experience_card", "revise", "experience_card", "medium"),
}

TARGET_BY_CANDIDATE_TYPE: dict[str, str] = {
    "revise_experience_card": "experience_card",
    "add_experience_card": "experience_card",
    "delete_experience_card": "experience_card",
    "narrow_usage_boundary": "usage_boundary",
    "expand_usage_boundary": "usage_boundary",
    "add_risk_warning": "risk_warning",
    "revise_risk_warning": "risk_warning",
    "revise_output_schema_metadata": "skill_output_schema_metadata",
    "revise_output_order": "case_analysis_output",
    "revise_output_title": "case_analysis_output",
    "revise_legal_analysis_prompt_hint": "case_analysis_output",
    "revise_fact_extraction_prompt_hint": "case_analysis_output",
    "mark_output_as_low_value": "case_analysis_output",
    "mark_output_as_high_risk": "case_analysis_output",
    "suggest_package_disable": "runtime_load",
    "suggest_package_rollback": "runtime_load",
    "suggest_next_package_version": "experience_package",
    "suggest_training_dataset_update": "training_dataset_future_input",
}


def classify_feedback_type(feedback_type: str, output_group: str) -> tuple[str, str, str, str]:
    rule = FEEDBACK_RULES.get(feedback_type, FEEDBACK_RULES["improvement_suggestion"])
    if feedback_type in {"inaccurate", "unclear_reasoning"} and output_group == "legal_analysis":
        return ("revise_legal_analysis_prompt_hint", "revise", "case_analysis_output", rule[3])
    if feedback_type == "inaccurate" and output_group == "fact_extraction":
        return ("revise_fact_extraction_prompt_hint", "revise", "case_analysis_output", rule[3])
    return rule


def classify_risk_type(risk_event: dict) -> str:
    if risk_event.get("risk_type"):
        return str(risk_event["risk_type"])
    summary = str(risk_event.get("risk_summary", "")).lower()
    level = str(risk_event.get("risk_level", "")).lower()
    if "hallucinated" in summary or "虚构" in summary or "法条" in summary:
        return "hallucinated_law"
    if "sensitive" in summary or "隐私" in summary or "敏感" in summary:
        return "sensitive_content_risk"
    if "boundary" in summary or "边界" in summary:
        return "usage_boundary_violation"
    if level in {"high", "critical"}:
        return "usage_boundary_violation"
    return "output_quality_issue"


def choose_mapping(
    output_group: str,
    feedback_records: list[dict],
    risk_records: list[dict],
) -> tuple[str, str, str, str, list[str]]:
    candidates: list[tuple[str, str, str, str, str]] = []
    for feedback in feedback_records:
        feedback_type = str(feedback.get("feedback_type", "improvement_suggestion"))
        candidate_type, change_type, target_type, default_severity = classify_feedback_type(feedback_type, output_group)
        severity = _max_severity(default_severity, str(feedback.get("severity", default_severity)))
        candidates.append((candidate_type, change_type, target_type, severity, feedback_type))
    for risk in risk_records:
        risk_type = classify_risk_type(risk)
        candidate_type, change_type, target_type, default_severity = RISK_RULES.get(risk_type, RISK_RULES["output_quality_issue"])
        severity = _max_severity(default_severity, str(risk.get("risk_level", default_severity)))
        candidates.append((candidate_type, change_type, target_type, severity, risk_type))
    if not candidates:
        return ("revise_experience_card", "revise", "experience_card", "low", ["no_feedback_or_risk"])
    candidates.sort(key=lambda item: SEVERITY_ORDER.get(item[3], 2), reverse=True)
    selected = candidates[0]
    reasons = [item[4] for item in candidates]
    return selected[0], selected[1], TARGET_BY_CANDIDATE_TYPE.get(selected[0], selected[2]), selected[3], reasons


def build_candidate_copy(candidate: CaseAnalysisImprovementCandidate, **updates) -> CaseAnalysisImprovementCandidate:
    return candidate.model_copy(update=updates)


def _max_severity(first: str, second: str) -> str:
    first = first if first in SEVERITY_ORDER else "medium"
    second = second if second in SEVERITY_ORDER else "medium"
    return first if SEVERITY_ORDER[first] >= SEVERITY_ORDER[second] else second
