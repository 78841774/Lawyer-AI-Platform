from datetime import datetime, timezone
from uuid import uuid4

from fastapi import HTTPException

from personal_production_pilot.audit_engine import record_audit_event
from personal_production_pilot.schemas import PilotReviewActionRequest, PilotReviewActionResult, PilotReviewItem, PilotReviewQueue
from personal_production_pilot.storage import REVIEW_QUEUE_DIR, read_payload, read_payloads, write_payload


ALLOWED_ACTIONS = {"approve_owner_download_metadata", "request_revision", "mark_low_confidence", "mark_not_ready", "reject"}


def create_review_item(*, linked_object_type: str, linked_object_id: str, created_at: str) -> PilotReviewItem:
    review_item_id = f"pilot_review_{uuid4().hex[:12]}"
    item = PilotReviewItem(
        review_item_id=review_item_id,
        linked_object_type=linked_object_type,
        linked_object_id=linked_object_id,
        review_focus=["owner-only download boundary", "draft label", "source trace", "no external delivery"],
        created_at=created_at,
        warnings=["Review item only updates pilot metadata; it does not send, share, final-label, or publish output."],
    )
    write_payload(REVIEW_QUEUE_DIR, review_item_id, item.model_dump())
    return item


def _get_review_item(review_item_id: str) -> PilotReviewItem | None:
    payload = read_payload(REVIEW_QUEUE_DIR, review_item_id)
    return PilotReviewItem(**payload) if payload else None


def build_review_queue() -> dict:
    items = [PilotReviewItem(**payload) for payload in read_payloads(REVIEW_QUEUE_DIR)]
    items = sorted(items, key=lambda item: item.created_at, reverse=True)
    return PilotReviewQueue(
        review_items=items,
        item_count=len(items),
        pending_count=sum(1 for item in items if item.review_status == "pending_lawyer_review"),
        warnings=["Pilot review queue is metadata-only and owner-download focused."],
    ).model_dump()


def submit_review_action(review_item_id: str, request: PilotReviewActionRequest) -> dict:
    item = _get_review_item(review_item_id)
    if item is None:
        raise HTTPException(status_code=404, detail="review_item_id 不存在")
    if request.action not in ALLOWED_ACTIONS:
        raise HTTPException(status_code=400, detail="review action 不支持")
    missing = [
        field
        for field in [
            "explicit_lawyer_confirmation",
            "explicit_no_external_delivery_confirmation",
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
    record_audit_event(action=f"pilot_review_action_{request.action}", actor=request.reviewer_id, object_type="review_item", object_id=review_item_id, timestamp=now)
    return PilotReviewActionResult(
        review_item_id=review_item_id,
        action=request.action,
        review_status=item.review_status,
        warnings=["Review action recorded; no email, public link, final opinion, final report, or external delivery is triggered."],
    ).model_dump()
