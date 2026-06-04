from typing import Any

from fastapi import APIRouter

from personal_alpha_lawyer_final_review.review_engine import (
    get_personal_alpha_lawyer_final_review_action,
    get_personal_alpha_lawyer_final_review_packet_detail,
    get_personal_alpha_lawyer_final_review_status,
    get_personal_alpha_lawyer_final_review_summary,
    list_personal_alpha_lawyer_final_review_actions,
    submit_personal_alpha_lawyer_final_review_action,
)
from personal_alpha_lawyer_final_review.schemas import PersonalAlphaLawyerFinalReviewActionRequest

router = APIRouter(prefix="/personal-alpha-lawyer-final-review", tags=["personal-alpha-lawyer-final-review"])


@router.get("/status")
def personal_alpha_lawyer_final_review_status() -> dict[str, Any]:
    return get_personal_alpha_lawyer_final_review_status()


@router.get("/packets/{packet_id}")
def personal_alpha_lawyer_final_review_packet_detail(packet_id: str) -> dict[str, Any]:
    return get_personal_alpha_lawyer_final_review_packet_detail(packet_id)


@router.get("/packets/{packet_id}/summary")
def personal_alpha_lawyer_final_review_summary(packet_id: str) -> dict[str, Any]:
    return get_personal_alpha_lawyer_final_review_summary(packet_id)


@router.get("/packets/{packet_id}/actions")
def personal_alpha_lawyer_final_review_actions(packet_id: str) -> dict[str, Any]:
    return list_personal_alpha_lawyer_final_review_actions(packet_id)


@router.post("/packets/{packet_id}/actions")
def personal_alpha_lawyer_final_review_submit_action(packet_id: str, request: PersonalAlphaLawyerFinalReviewActionRequest) -> dict[str, Any]:
    return submit_personal_alpha_lawyer_final_review_action(packet_id, request)


@router.get("/actions/{action_id}")
def personal_alpha_lawyer_final_review_action_detail(action_id: str) -> dict[str, Any]:
    return get_personal_alpha_lawyer_final_review_action(action_id)
