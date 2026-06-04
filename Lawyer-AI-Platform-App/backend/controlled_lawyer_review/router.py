from typing import Any

from fastapi import APIRouter

from controlled_lawyer_review.audit import list_controlled_lawyer_review_audit_logs
from controlled_lawyer_review.review_engine import (
    approve_controlled_lawyer_review,
    get_controlled_lawyer_review,
    get_controlled_lawyer_review_status,
    reject_controlled_lawyer_review,
    request_revision_controlled_lawyer_review,
    submit_controlled_lawyer_review,
)
from controlled_lawyer_review.schemas import ControlledLawyerReviewActionRequest, ControlledLawyerReviewSubmitRequest

router = APIRouter(prefix="/controlled-review", tags=["controlled-review"])


@router.get("/status")
def controlled_lawyer_review_status() -> dict[str, Any]:
    return get_controlled_lawyer_review_status()


@router.post("/submit")
def controlled_lawyer_review_submit(request: ControlledLawyerReviewSubmitRequest) -> dict[str, Any]:
    return submit_controlled_lawyer_review(request)


@router.get("/audit-logs")
def controlled_lawyer_review_audit_logs() -> dict[str, Any]:
    return {"audit_logs": list_controlled_lawyer_review_audit_logs()}


@router.get("/{review_id}")
def controlled_lawyer_review_record(review_id: str) -> dict[str, Any]:
    return get_controlled_lawyer_review(review_id)


@router.post("/{review_id}/approve")
def controlled_lawyer_review_approve(review_id: str, request: ControlledLawyerReviewActionRequest) -> dict[str, Any]:
    return approve_controlled_lawyer_review(review_id, request)


@router.post("/{review_id}/reject")
def controlled_lawyer_review_reject(review_id: str, request: ControlledLawyerReviewActionRequest) -> dict[str, Any]:
    return reject_controlled_lawyer_review(review_id, request)


@router.post("/{review_id}/request-revision")
def controlled_lawyer_review_request_revision(review_id: str, request: ControlledLawyerReviewActionRequest) -> dict[str, Any]:
    return request_revision_controlled_lawyer_review(review_id, request)

