from datetime import datetime, timezone
from uuid import uuid4

from fastapi import HTTPException

from personal_case_analysis.audit_engine import record_audit_event
from personal_case_analysis.schemas import (
    CaseAnalysisReviewActionResult,
    CaseAnalysisReviewItem,
    CaseAnalysisReviewQueue,
    ReviewActionRequest,
)
from personal_case_analysis.storage import REVIEW_QUEUE_DIR, read_payload, read_payloads, write_payload


ALLOWED_ACTIONS = {"approve_draft_metadata", "request_revision", "mark_low_confidence", "mark_not_ready", "reject"}


def create_review_item(
    *,
    linked_object_type: str,
    linked_object_id: str,
    case_id: str,
    review_focus: list[str],
    risk_flags: list[str],
    created_at: str,
) -> CaseAnalysisReviewItem:
    review_item_id = f"case_analysis_review_{uuid4().hex[:12]}"
    item = CaseAnalysisReviewItem(
        review_item_id=review_item_id,
        linked_object_type=linked_object_type,
        linked_object_id=linked_object_id,
        case_id=case_id,
        review_focus=review_focus,
        risk_flags=risk_flags,
        created_at=created_at,
        warnings=["Review item 仅用于律师复核 draft metadata，不产生训练数据。"],
    )
    write_payload(REVIEW_QUEUE_DIR, review_item_id, item.model_dump())
    return item


def get_review_item(review_item_id: str) -> CaseAnalysisReviewItem | None:
    payload = read_payload(REVIEW_QUEUE_DIR, review_item_id)
    return CaseAnalysisReviewItem(**payload) if payload else None


def list_review_items() -> list[CaseAnalysisReviewItem]:
    return [CaseAnalysisReviewItem(**payload) for payload in read_payloads(REVIEW_QUEUE_DIR)]


def build_review_queue() -> dict:
    items = sorted(list_review_items(), key=lambda item: item.created_at, reverse=True)
    return CaseAnalysisReviewQueue(
        review_items=items,
        item_count=len(items),
        pending_count=sum(1 for item in items if item.review_status == "pending_lawyer_review"),
        warnings=["律师复核队列仅管理未结案件分析 draft metadata。"],
    ).model_dump()


def submit_review_action(review_item_id: str, request: ReviewActionRequest) -> dict:
    item = get_review_item(review_item_id)
    if item is None:
        raise HTTPException(status_code=404, detail="review_item_id 不存在")
    if request.action not in ALLOWED_ACTIONS:
        raise HTTPException(status_code=400, detail="review action 不支持")
    missing = [
        field
        for field in [
            "explicit_lawyer_confirmation",
            "explicit_no_training_data_confirmation",
            "explicit_no_final_opinion_confirmation",
        ]
        if not getattr(request, field)
    ]
    if missing:
        raise HTTPException(status_code=400, detail={"message": "review confirmation 不完整", "missing": missing})
    now = datetime.now(timezone.utc).isoformat()
    item.review_status = request.action
    item.updated_at = now
    write_payload(REVIEW_QUEUE_DIR, review_item_id, item.model_dump())
    record_audit_event(
        action=f"review_action_{request.action}",
        actor=request.reviewer_id,
        object_type="review_item",
        object_id=review_item_id,
        timestamp=now,
    )
    return CaseAnalysisReviewActionResult(
        review_item_id=review_item_id,
        action=request.action,
        review_status=item.review_status,
        warnings=["复核动作仅更新 review metadata，不生成最终法律意见或训练数据。"],
    ).model_dump()
