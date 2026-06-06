from personal_skill_studio.training_artifacts.iteration_candidate_safety_engine import v731i_safety_flags
from personal_skill_studio.training_artifacts.schemas import ExperienceIterationCandidate, PracticeFeedbackRiskEvent, PracticeLawyerFeedback


FEEDBACK_CHANGE_TYPE_MAP = {
    "missing_risk_warning": "add_risk_warning",
    "wrong_usage_boundary": "narrow_usage_boundary",
    "over_generalized": "narrow_usage_boundary",
    "too_narrow": "expand_usage_boundary",
    "unsafe_output": "revise_experience_card",
    "hallucinated_law": "revise_experience_card",
    "inaccurate": "revise_experience_card",
    "unclear_reasoning": "revise_experience_card",
    "needs_editorial_revision": "revise_experience_card",
    "should_add_experience_card": "add_experience_card",
    "should_revise_experience_card": "revise_experience_card",
    "should_delete_experience_card": "delete_experience_card",
    "should_narrow_usage_boundary": "narrow_usage_boundary",
    "should_add_risk_warning": "add_risk_warning",
    "should_disable_package": "mark_package_for_disable",
    "should_rollback_package": "mark_package_for_rollback",
    "should_create_next_version": "create_next_version",
}

RISK_CHANGE_TYPE_MAP = {
    "hallucinated_law": "revise_experience_card",
    "incorrect_case_cause": "narrow_usage_boundary",
    "sensitive_content_risk": "add_risk_warning",
    "over_confident_guidance": "add_risk_warning",
    "missing_disclaimer": "add_risk_warning",
    "usage_boundary_violation": "narrow_usage_boundary",
    "package_policy_mismatch": "narrow_usage_boundary",
    "output_quality_issue": "revise_experience_card",
    "unsafe_practice_suggestion": "mark_package_for_disable",
    "wrong_evidence_assumption": "revise_experience_card",
    "wrong_lawyer_strategy_hint": "revise_experience_card",
}


def map_feedback_to_candidate(
    feedback: PracticeLawyerFeedback,
    candidate_pack_id: str,
    sequence: int,
) -> ExperienceIterationCandidate:
    change_type = FEEDBACK_CHANGE_TYPE_MAP.get(feedback.feedback_type, "revise_experience_card")
    return ExperienceIterationCandidate(
        iteration_candidate_id=f"{candidate_pack_id}_feedback_candidate_{sequence}",
        candidate_pack_id=candidate_pack_id,
        change_type=change_type,
        target_experience_card_id=feedback.applies_to_experience_card_id,
        current_text_summary="Current experience card metadata is preserved; v7.31i does not copy full package text.",
        proposed_change_summary=feedback.suggested_change,
        proposed_lawyer_review_text=_lawyer_review_text(change_type),
        reason_from_feedback=feedback.feedback_summary,
        risk_basis="Feedback classification: " + feedback.classification.feedback_category,
        source_feedback_ids=[feedback.feedback_id],
        source_risk_event_ids=[],
        severity=feedback.severity,
        suggested_action=feedback.classification.suggested_next_action,
        status="candidate",
        warnings=[
            "Feedback candidate is preparation metadata only.",
            "It does not mutate the loaded package or lawyer-approved package.",
        ],
        **v731i_safety_flags(),
    )


def map_risk_event_to_candidate(
    risk_event: PracticeFeedbackRiskEvent,
    candidate_pack_id: str,
    sequence: int,
) -> ExperienceIterationCandidate:
    change_type = RISK_CHANGE_TYPE_MAP.get(risk_event.risk_type, "add_risk_warning")
    return ExperienceIterationCandidate(
        iteration_candidate_id=f"{candidate_pack_id}_risk_candidate_{sequence}",
        candidate_pack_id=candidate_pack_id,
        change_type=change_type,
        target_experience_card_id=None,
        current_text_summary="Current package metadata is preserved; v7.31i does not copy full package text.",
        proposed_change_summary=risk_event.suggested_action,
        proposed_lawyer_review_text=_lawyer_review_text(change_type),
        reason_from_feedback="Risk event metadata: " + risk_event.risk_summary,
        risk_basis=risk_event.risk_type,
        source_feedback_ids=[],
        source_risk_event_ids=[risk_event.risk_event_id],
        severity=risk_event.severity,
        suggested_action="prepare_for_next_experience_build",
        status="candidate",
        warnings=[
            "Risk candidate is recommendation metadata only.",
            "Disable and rollback suggestions are not executed automatically.",
        ],
        **v731i_safety_flags(),
    )


def _lawyer_review_text(change_type: str) -> str:
    review_notes = {
        "add_experience_card": "律师需复核是否新增经验卡片，并确认适用与不适用场景。",
        "revise_experience_card": "律师需复核经验卡片修改摘要，确认不会形成最终法律意见。",
        "delete_experience_card": "律师需复核是否删除或停用相关经验卡片。",
        "narrow_usage_boundary": "律师需复核是否缩小使用边界并补充限制说明。",
        "expand_usage_boundary": "律师需复核是否扩大使用边界，且不得越过安全范围。",
        "add_risk_warning": "律师需复核新增风险提示内容和展示位置。",
        "mark_package_for_rollback": "律师需通过 v7.31g 控制流程另行评估回滚建议。",
        "mark_package_for_disable": "律师需通过 v7.31g 控制流程另行评估禁用建议。",
        "create_next_version": "律师需确认是否进入下一版经验包草案构建。",
    }
    return review_notes.get(change_type, "律师需复核该候选变更。")
