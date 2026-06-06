from uuid import uuid4

from personal_trial_readiness.schemas import QualityReview
from personal_trial_readiness.storage import read_json, write_json


def build_quality_review(trial_id: str) -> QualityReview:
    data = read_json("quality", trial_id)
    if data:
        return QualityReview(**data)
    return QualityReview(
        review_id=f"quality_{trial_id}",
        trial_id=trial_id,
        stage_scores={
            "case_intake": 84,
            "material_workspace": 83,
            "fact_preview": 82,
            "legal_analysis_draft": 80,
            "skill_final_drafts": 79,
            "owner_output_center": 84,
        },
        optimization_suggestions=[
            "优先优化低风险试运行中的问题记录与按钮提示。",
            "继续把评分描述为参考，不表达法律正确性保证。",
        ],
        warnings=["评分只作为优化参考，不构成最终法律意见。"],
    )


def create_mock_quality_review(trial_id: str) -> dict:
    review = build_quality_review(trial_id)
    review.review_id = f"quality_{uuid4().hex[:10]}"
    write_json("quality", trial_id, review.model_dump())
    return review.model_dump()

