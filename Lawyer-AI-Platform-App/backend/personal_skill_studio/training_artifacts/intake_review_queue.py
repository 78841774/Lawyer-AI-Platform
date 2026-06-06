from personal_skill_studio.training_artifacts.schemas import (
    TrainingIntakeReviewActionRequest,
    TrainingIntakeReviewItem,
)


def build_review_queue(intake_id: str) -> list[TrainingIntakeReviewItem]:
    return [
        TrainingIntakeReviewItem(
            review_item_id=f"{intake_id}_review_authorization",
            intake_id=intake_id,
            review_type="authorization_and_case_closed_confirmation",
            action_allowed=["approve_metadata_only", "request_revision", "reject"],
        ),
        TrainingIntakeReviewItem(
            review_item_id=f"{intake_id}_review_redaction",
            intake_id=intake_id,
            review_type="redaction_quality_review",
            action_allowed=["approve_metadata_only", "request_revision", "reject"],
        ),
        TrainingIntakeReviewItem(
            review_item_id=f"{intake_id}_review_case_cause",
            intake_id=intake_id,
            review_type="case_cause_classification_review",
            action_allowed=["approve_metadata_only", "request_revision", "reject"],
        ),
    ]


def apply_review_action(item: TrainingIntakeReviewItem, request: TrainingIntakeReviewActionRequest) -> TrainingIntakeReviewItem:
    status = "approved_metadata_only" if request.action == "approve_metadata_only" else request.action
    return item.model_copy(update={
        "review_status": status,
        "reviewed_by": request.reviewer_id,
        "reviewer_note": request.reviewer_note,
    })
