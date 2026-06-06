from personal_skill_studio.training_artifacts.iteration_candidate_safety_engine import v731i_safety_flags
from personal_skill_studio.training_artifacts.schemas import ExperienceIterationCandidate, ExperienceIterationDiff


def build_iteration_diff(candidate_pack_id: str, candidates: list[ExperienceIterationCandidate]) -> ExperienceIterationDiff:
    return ExperienceIterationDiff(
        candidate_pack_id=candidate_pack_id,
        added_cards=_filter(candidates, "add_experience_card"),
        revised_cards=_filter(candidates, "revise_experience_card"),
        removed_cards=_filter(candidates, "delete_experience_card"),
        narrowed_boundaries=_filter(candidates, "narrow_usage_boundary"),
        expanded_boundaries=_filter(candidates, "expand_usage_boundary"),
        added_risk_warnings=_filter(candidates, "add_risk_warning"),
        rollback_recommendations=_filter(candidates, "mark_package_for_rollback"),
        disable_recommendations=_filter(candidates, "mark_package_for_disable"),
        next_version_recommendation=any(candidate.change_type == "create_next_version" for candidate in candidates),
        proposed_changes_count=len(candidates),
        warnings=[
            "Diff is candidate metadata only.",
            "It does not modify loaded packages, runtime policy, Skills, or training artifacts.",
        ],
        **v731i_safety_flags(),
    )


def _filter(candidates: list[ExperienceIterationCandidate], change_type: str) -> list[ExperienceIterationCandidate]:
    return [candidate for candidate in candidates if candidate.change_type == change_type]
