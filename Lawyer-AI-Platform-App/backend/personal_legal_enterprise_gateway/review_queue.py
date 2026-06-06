from personal_legal_enterprise_gateway.audit_engine import now_iso, record_audit_event
from personal_legal_enterprise_gateway.schemas import ReviewActionRequest, ReviewActionResult, ReviewItem, ReviewQueue
from personal_legal_enterprise_gateway.storage import REVIEW_DIR, read_payload, read_payloads, write_payload


def create_review_item(run_id: str, provider_id: str, review_type: str) -> str:
    review_item_id = f"review_{run_id}"
    item = ReviewItem(
        review_item_id=review_item_id,
        run_id=run_id,
        provider_id=provider_id,
        review_type=review_type,
        created_at=now_iso(),
    )
    write_payload(REVIEW_DIR, review_item_id, item.model_dump())
    return review_item_id


def build_review_queue() -> dict:
    items = [ReviewItem(**payload) for payload in read_payloads(REVIEW_DIR)]
    return ReviewQueue(
        items=items,
        item_count=len(items),
        pending_review_count=sum(1 for item in items if item.review_status == "pending_review"),
    ).model_dump()


def submit_review_action(review_item_id: str, request: ReviewActionRequest) -> dict:
    payload = read_payload(REVIEW_DIR, review_item_id)
    if payload is None:
        return ReviewActionResult(review_item_id=review_item_id, action=request.action, status="blocked", blocked_reasons=["review_item_id not found"]).model_dump()
    blocked = []
    if not request.owner_confirmation:
        blocked.append("owner_confirmation_missing")
    if not request.lawyer_review_acknowledged:
        blocked.append("lawyer_review_acknowledged_missing")
    if not request.source_trace_acknowledged:
        blocked.append("source_trace_acknowledged_missing")
    record_audit_event(payload["provider_id"], f"review_{request.action}", payload["run_id"])
    return ReviewActionResult(
        review_item_id=review_item_id,
        action=request.action,
        status="blocked" if blocked else "action_recorded_metadata_only",
        blocked_reasons=blocked,
    ).model_dump()

