from personal_skill_studio.training_artifacts.schemas import ExperienceIterationCandidate, PracticeFeedbackCandidatePack


def apply_candidate_pack(candidate_pack: PracticeFeedbackCandidatePack) -> dict[str, list[dict[str, str | list[str] | bool]]]:
    candidates = candidate_pack.iteration_candidates
    return {
        "added_experience_cards": [_candidate_card(item, "added") for item in _filter(candidates, "add_experience_card")],
        "revised_experience_cards": [_candidate_card(item, "revised") for item in _filter(candidates, "revise_experience_card")],
        "removed_experience_cards": [_candidate_card(item, "removed") for item in _filter(candidates, "delete_experience_card")],
        "usage_boundary_changes": [
            _candidate_card(item, "usage_boundary_changed")
            for item in [
                *_filter(candidates, "narrow_usage_boundary"),
                *_filter(candidates, "expand_usage_boundary"),
            ]
        ],
        "risk_warning_changes": [_candidate_card(item, "risk_warning_added") for item in _filter(candidates, "add_risk_warning")],
        "rollback_recommendations": [_candidate_card(item, "manual_rollback_review") for item in _filter(candidates, "mark_package_for_rollback")],
        "disable_recommendations": [_candidate_card(item, "manual_disable_review") for item in _filter(candidates, "mark_package_for_disable")],
    }


def _candidate_card(candidate: ExperienceIterationCandidate, draft_change_status: str) -> dict[str, str | list[str] | bool]:
    return {
        "candidate_id": candidate.iteration_candidate_id,
        "target_experience_card_id": candidate.target_experience_card_id or "new_or_package_level_candidate",
        "draft_change_status": draft_change_status,
        "change_type": candidate.change_type,
        "draft_summary": candidate.proposed_change_summary,
        "lawyer_review_note": candidate.proposed_lawyer_review_text,
        "reason_summary": candidate.reason_from_feedback,
        "risk_basis": candidate.risk_basis,
        "severity": candidate.severity,
        "metadata_only": True,
        "requires_lawyer_review": True,
    }


def _filter(candidates: list[ExperienceIterationCandidate], change_type: str) -> list[ExperienceIterationCandidate]:
    return [candidate for candidate in candidates if candidate.change_type == change_type]
