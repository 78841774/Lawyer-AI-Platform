from personal_skill_studio.training_artifacts.next_package_safety_engine import v731j_safety_flags
from personal_skill_studio.training_artifacts.schemas import NextPackageLawyerReviewView, PracticeFeedbackCandidatePack


def regenerate_lawyer_review_view(
    next_package_id: str,
    candidate_pack: PracticeFeedbackCandidatePack,
    applied_changes: dict[str, list[dict[str, str | list[str] | bool]]],
) -> NextPackageLawyerReviewView:
    return NextPackageLawyerReviewView(
        lawyer_review_view_id=f"{next_package_id}_lawyer_review_view",
        next_package_id=next_package_id,
        candidate_pack_id=candidate_pack.candidate_pack_id,
        change_summary=(
            f"下一版草案基于 {len(candidate_pack.iteration_candidates)} 个候选变更生成，"
            "仅供后续 Practice Load Review Gate 复核。"
        ),
        added_experience_cards=applied_changes["added_experience_cards"],
        revised_experience_cards=applied_changes["revised_experience_cards"],
        removed_experience_cards=applied_changes["removed_experience_cards"],
        usage_boundary_changes=applied_changes["usage_boundary_changes"],
        risk_warning_changes=applied_changes["risk_warning_changes"],
        feedback_summary=[
            f"feedback:{feedback_id}" for feedback_id in candidate_pack.feedback_ids
        ],
        risk_event_summary=[
            f"risk_event:{risk_event_id}" for risk_event_id in candidate_pack.risk_event_ids
        ],
        warnings=[
            "Lawyer review view is metadata-only.",
            "It is not a final legal opinion, final report, or runtime-loaded package.",
        ],
        **v731j_safety_flags(),
    )
