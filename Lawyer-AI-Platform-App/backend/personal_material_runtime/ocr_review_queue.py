import re
from datetime import datetime, timezone

from personal_material_runtime.audit_engine import record_audit_event
from personal_material_runtime.ocr_runtime import get_ocr_job, save_ocr_job
from personal_material_runtime.schemas import (
    PersonalOCRReviewActionRequest,
    PersonalOCRReviewActionResult,
    PersonalOCRReviewItem,
    PersonalOCRReviewQueue,
)
from personal_material_runtime.storage import REVIEW_QUEUE_DIR, read_payload, read_payloads, write_payload


ALLOWED_ACTIONS = {
    "approve_preview_for_analysis": "approved_for_analysis",
    "request_manual_correction": "needs_manual_correction",
    "reject_ocr_preview": "rejected",
    "mark_low_confidence": "needs_manual_correction",
}
SAFE_REVIEWER_ID_PATTERN = re.compile(r"^[A-Za-z0-9_-]{1,64}$")


def build_review_queue() -> dict:
    items = [PersonalOCRReviewItem(**payload) for payload in read_payloads(REVIEW_QUEUE_DIR)]
    items = sorted(items, key=lambda item: item.updated_at, reverse=True)
    return PersonalOCRReviewQueue(
        items=items,
        item_count=len(items),
        pending_review_count=sum(1 for item in items if item.review_status == "pending_review"),
        warnings=["Review queue contains metadata only. It does not pass OCR preview content into AI prompts."],
    ).model_dump()


def submit_review_action(ocr_job_id: str, request: PersonalOCRReviewActionRequest) -> dict:
    blocked_reasons = validate_review_action_request(request)
    item = get_review_item(ocr_job_id)
    if item is None:
        blocked_reasons.append("ocr_job_id is not registered")
    if request.action not in ALLOWED_ACTIONS:
        return PersonalOCRReviewActionResult(
            ocr_job_id=ocr_job_id,
            action=request.action if _safe_short_value(request.action) else "redacted_action",
            status="invalid_action",
            blocked_reasons=["action is not supported"],
            warnings=["Review action was rejected. No review metadata was changed."],
        ).model_dump()
    if blocked_reasons:
        return PersonalOCRReviewActionResult(
            ocr_job_id=ocr_job_id,
            action=request.action if _safe_short_value(request.action) else "redacted_action",
            status="blocked",
            blocked_reasons=blocked_reasons,
            warnings=["Review action was blocked. Unsafe values are not echoed."],
        ).model_dump()

    assert item is not None
    now = datetime.now(timezone.utc).isoformat()
    next_status = ALLOWED_ACTIONS[request.action]
    eligible = request.action == "approve_preview_for_analysis"
    updated_item = item.model_copy(
        update={
            "review_status": next_status,
            "eligible_for_ai_prompt_after_review": eligible,
            "updated_at": now,
        }
    )
    write_payload(REVIEW_QUEUE_DIR, ocr_job_id, updated_item.model_dump())
    job = get_ocr_job(ocr_job_id)
    if job is not None:
        job.ocr_preview.eligible_for_ai_prompt_after_review = eligible
        updated_job = job.model_copy(update={"review_status": next_status, "eligible_for_ai_prompt_after_review": eligible})
        save_ocr_job(updated_job)
        record_audit_event(
            event_type=f"ocr_review_{request.action}",
            case_id=job.case_id,
            material_id=job.material_id,
            provider_id=job.ocr_provider_id,
            job_id=ocr_job_id,
            created_at=now,
            manual_approval_confirmed=request.manual_review_confirmed,
        )

    return PersonalOCRReviewActionResult(
        ocr_job_id=ocr_job_id,
        action=request.action,
        reviewer_id="redacted_reviewer",
        status="review_action_recorded",
        review_status=next_status,
        manual_review_confirmed=True,
        eligible_for_ai_prompt_after_review=eligible,
        warnings=["Review metadata updated. OCR output is not sent to AI prompts automatically."],
    ).model_dump()


def get_review_item(ocr_job_id: str) -> PersonalOCRReviewItem | None:
    payload = read_payload(REVIEW_QUEUE_DIR, ocr_job_id)
    return PersonalOCRReviewItem(**payload) if payload else None


def validate_review_action_request(request: PersonalOCRReviewActionRequest) -> list[str]:
    blocked: list[str] = []
    if not SAFE_REVIEWER_ID_PATTERN.match(request.reviewer_id):
        blocked.append("reviewer_id is unsafe")
    if not request.manual_review_confirmed:
        blocked.append("manual_review_confirmed is required")
    if not request.no_raw_ocr_exposure_confirmation:
        blocked.append("no_raw_ocr_exposure_confirmation is required")
    if not request.lawyer_review_required_confirmation:
        blocked.append("lawyer_review_required_confirmation is required")
    return blocked


def _safe_short_value(value: str) -> bool:
    return bool(re.match(r"^[A-Za-z0-9_-]{1,64}$", value))
