from personal_skill_studio.training_artifacts.practice_feedback_safety_engine import v731h_safety_flags
from personal_skill_studio.training_artifacts.schemas import PracticeFeedbackClassification


HIGH_RISK_FEEDBACK_TYPES = {
    "unsafe_output",
    "hallucinated_law",
    "wrong_usage_boundary",
    "should_disable_package",
    "should_rollback_package",
}

ITERATION_FEEDBACK_TYPES = {
    "inaccurate",
    "over_generalized",
    "too_narrow",
    "missing_risk_warning",
    "wrong_usage_boundary",
    "unsafe_output",
    "hallucinated_law",
    "unclear_reasoning",
    "needs_editorial_revision",
    "should_create_next_version",
    "should_add_experience_card",
    "should_revise_experience_card",
    "should_delete_experience_card",
    "should_narrow_usage_boundary",
    "should_add_risk_warning",
}


def classify_feedback(feedback_type: str, severity: str) -> PracticeFeedbackClassification:
    normalized_type = feedback_type.strip() or "useful"
    normalized_severity = _normalize_severity(severity)
    return PracticeFeedbackClassification(
        feedback_category=normalized_type,
        severity=_classification_severity(normalized_type, normalized_severity),
        suggested_next_action=_suggested_action(normalized_type),
        auto_disable_recommended=normalized_type == "should_disable_package",
        rollback_recommended=normalized_type == "should_rollback_package",
        create_iteration_candidate_recommended=normalized_type in ITERATION_FEEDBACK_TYPES,
        warnings=[
            "Classification is rule-based metadata only.",
            "Disable, rollback, iteration, and package mutation are not automatically executed.",
        ],
        **v731h_safety_flags(),
    )


def _classification_severity(feedback_type: str, severity: str) -> str:
    if feedback_type in HIGH_RISK_FEEDBACK_TYPES and severity == "low":
        return "medium"
    return severity


def _normalize_severity(severity: str) -> str:
    return severity if severity in {"low", "medium", "high", "critical"} else "medium"


def _suggested_action(feedback_type: str) -> str:
    if feedback_type == "useful":
        return "keep_as_reference"
    if feedback_type == "should_disable_package":
        return "manual_disable_review_via_v731g_runtime_controls"
    if feedback_type == "should_rollback_package":
        return "manual_rollback_review_via_v731g_runtime_controls"
    if feedback_type in ITERATION_FEEDBACK_TYPES:
        return "prepare_for_v731i_iteration_candidate"
    return "triage_feedback_metadata"
