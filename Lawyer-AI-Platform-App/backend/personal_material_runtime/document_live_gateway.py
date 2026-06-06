from datetime import datetime, timezone
from uuid import uuid4

from personal_material_runtime.audit_engine import record_live_audit_event
from personal_material_runtime.document_boundary import validate_document_boundary, validate_ocr_boundary
from personal_material_runtime.live_guard import live_mode_enabled_for, validate_live_gate
from personal_material_runtime.ocr_response_sanitizer import sanitize_live_run
from personal_material_runtime.page_usage_meter import build_document_metadata_preview, build_ocr_metadata_preview
from personal_material_runtime.schemas import (
    PersonalMaterialLiveReviewActionRequest,
    PersonalMaterialLiveReviewActionResult,
    PersonalMaterialLiveReviewItem,
    PersonalMaterialLiveReviewQueue,
    PersonalMaterialLiveRunList,
    PersonalMaterialLiveRunRecord,
    PersonalMaterialLiveRunRequest,
)
from personal_material_runtime.source_trace_engine import create_live_source_trace
from personal_material_runtime.storage import (
    LIVE_DOCUMENT_RUNS_DIR,
    LIVE_OCR_RUNS_DIR,
    LIVE_REVIEW_QUEUE_DIR,
    read_payload,
    read_payloads,
    write_payload,
)


LIVE_REVIEW_ACTIONS = {
    "approve_metadata_only": "metadata_approved",
    "request_manual_review": "manual_review_requested",
    "reject": "rejected",
    "mark_low_confidence": "low_confidence",
    "allow_redacted_preview": "redacted_preview_allowed",
    "block_raw_content": "raw_content_blocked",
}


def execute_document_live_run(request: PersonalMaterialLiveRunRequest, *, dry_run: bool) -> dict:
    return _execute_live_run(request.model_copy(update={"dry_run": dry_run}), run_type="document")


def execute_ocr_live_run(request: PersonalMaterialLiveRunRequest, *, dry_run: bool) -> dict:
    return _execute_live_run(request.model_copy(update={"dry_run": dry_run}), run_type="ocr")


def list_document_live_runs() -> dict:
    return _build_run_list(LIVE_DOCUMENT_RUNS_DIR)


def list_ocr_live_runs() -> dict:
    return _build_run_list(LIVE_OCR_RUNS_DIR)


def get_document_live_run(run_id: str) -> PersonalMaterialLiveRunRecord | None:
    payload = read_payload(LIVE_DOCUMENT_RUNS_DIR, run_id)
    return PersonalMaterialLiveRunRecord(**payload) if payload else None


def get_ocr_live_run(run_id: str) -> PersonalMaterialLiveRunRecord | None:
    payload = read_payload(LIVE_OCR_RUNS_DIR, run_id)
    return PersonalMaterialLiveRunRecord(**payload) if payload else None


def build_live_review_queue() -> dict:
    items = [PersonalMaterialLiveReviewItem(**payload) for payload in read_payloads(LIVE_REVIEW_QUEUE_DIR)]
    items = sorted(items, key=lambda item: item.updated_at, reverse=True)
    return PersonalMaterialLiveReviewQueue(
        items=items,
        item_count=len(items),
        pending_review_count=sum(1 for item in items if item.review_status == "pending_review"),
        warnings=[
            "Live review queue is metadata-only.",
            "approve_metadata_only does not allow raw OCR text or raw document content into AI prompts.",
        ],
    ).model_dump()


def submit_live_review_action(review_item_id: str, request: PersonalMaterialLiveReviewActionRequest) -> dict:
    item_payload = read_payload(LIVE_REVIEW_QUEUE_DIR, review_item_id)
    if item_payload is None:
        return PersonalMaterialLiveReviewActionResult(
            review_item_id=review_item_id,
            action=request.action,
            status="blocked",
            blocked_reasons=["review_item_id is not registered"],
            warnings=["Review action blocked. No metadata was changed."],
        ).model_dump()
    blocked = _validate_review_action(request)
    if request.action not in LIVE_REVIEW_ACTIONS:
        blocked.append("action is not supported")
    if blocked:
        return PersonalMaterialLiveReviewActionResult(
            review_item_id=review_item_id,
            action=request.action,
            status="blocked",
            blocked_reasons=blocked,
            warnings=["Review action blocked. Unsafe or incomplete confirmation metadata was not applied."],
        ).model_dump()

    item = PersonalMaterialLiveReviewItem(**item_payload)
    now = datetime.now(timezone.utc).isoformat()
    next_status = LIVE_REVIEW_ACTIONS[request.action]
    updated = item.model_copy(
        update={
            "review_status": next_status,
            "redacted_preview_allowed": request.action == "allow_redacted_preview",
            "raw_content_blocked": True,
            "updated_at": now,
            "warnings": [
                "Review metadata updated.",
                "Raw full content remains blocked and is not injected into AI prompts.",
            ],
        }
    )
    write_payload(LIVE_REVIEW_QUEUE_DIR, review_item_id, updated.model_dump())
    record_live_audit_event(
        provider_id=item.provider_id,
        action=f"review_{request.action}",
        actor_id=request.actor_id,
        review_item_id=review_item_id,
        created_at=now,
        blocked_reason=None,
    )
    return PersonalMaterialLiveReviewActionResult(
        review_item_id=review_item_id,
        action=request.action,
        status="review_action_recorded",
        review_status=next_status,
        warnings=[
            "Review action recorded as metadata only.",
            "No raw OCR text, document content, AI prompt injection, fact extraction, legal analysis, final report, or external delivery was triggered.",
        ],
    ).model_dump()


def _execute_live_run(request: PersonalMaterialLiveRunRequest, *, run_type: str) -> dict:
    now = datetime.now(timezone.utc).isoformat()
    run_id = f"personal_material_live_{run_type}_{uuid4().hex[:12]}"
    boundary = validate_ocr_boundary(request) if run_type == "ocr" else validate_document_boundary(request)
    gate = validate_live_gate(request, run_type=run_type)
    blocked_reasons = [*boundary, *gate]
    metadata = build_ocr_metadata_preview(request) if run_type == "ocr" else build_document_metadata_preview(request)
    if request.dry_run and not blocked_reasons:
        status = "dry_run_completed"
        blocked_reason = None
        would_call_provider = False
        adapter_unavailable = False
    elif blocked_reasons:
        status = "live_call_blocked"
        blocked_reason = "; ".join(blocked_reasons)
        would_call_provider = False
        adapter_unavailable = False
    else:
        status = "provider_adapter_unavailable"
        blocked_reason = "adapter_unavailable"
        blocked_reasons = ["adapter_unavailable"]
        would_call_provider = True
        adapter_unavailable = True

    record = PersonalMaterialLiveRunRecord(
        run_id=run_id,
        run_type=run_type,
        provider_id=request.provider_id,
        case_id=request.case_id,
        material_id=request.material_id,
        file_name="redacted_file_name",
        file_type=request.file_type.strip().lower().lstrip(".") or "pdf",
        status=status,
        dry_run=request.dry_run,
        would_call_provider=would_call_provider,
        live_mode_enabled=live_mode_enabled_for(run_type),
        live_call_requested=not request.dry_run,
        live_call_executed=False,
        blocked_reason=blocked_reason,
        blocked_reasons=blocked_reasons,
        provider_adapter_unavailable=adapter_unavailable,
        file_metadata_only=True,
        document_metadata=metadata if run_type == "document" else build_document_metadata_preview(request),
        ocr_metadata=metadata if run_type == "ocr" else build_ocr_metadata_preview(request),
        source_trace_created=True,
        created_at=now,
        warnings=[
            "v7.13 returns OCR / document metadata only.",
            "Raw OCR text and raw document content are not returned or injected into AI prompts.",
        ],
    )
    record = sanitize_live_run(record)
    directory = LIVE_OCR_RUNS_DIR if run_type == "ocr" else LIVE_DOCUMENT_RUNS_DIR
    write_payload(directory, run_id, record.model_dump())
    _create_review_item(record, now)
    create_live_source_trace(
        run_id=run_id,
        run_type=run_type,
        provider_id=request.provider_id,
        case_id=request.case_id,
        material_id=request.material_id,
        created_at=now,
        page_count=metadata.page_count_estimate,
    )
    record_live_audit_event(
        provider_id=request.provider_id,
        action=f"{run_type}_{'dry_run' if request.dry_run else 'live_attempt'}",
        actor_id=request.actor_id,
        run_id=run_id,
        live_call_requested=not request.dry_run,
        live_call_executed=False,
        blocked_reason=blocked_reason,
        source_trace_created=True,
        page_count=metadata.page_count_estimate,
        created_at=now,
    )
    return record.model_dump()


def _create_review_item(record: PersonalMaterialLiveRunRecord, created_at: str) -> None:
    review_item_id = f"personal_material_live_review_{record.run_id}"
    item = PersonalMaterialLiveReviewItem(
        review_item_id=review_item_id,
        run_id=record.run_id,
        run_type=record.run_type,
        provider_id=record.provider_id,
        case_id=record.case_id,
        material_id=record.material_id,
        confidence_summary=(
            record.ocr_metadata.confidence_summary if record.run_type == "ocr" else record.document_metadata.confidence_summary
        ),
        created_at=created_at,
        updated_at=created_at,
        warnings=["Metadata-only review item. Raw content remains blocked by default."],
    )
    write_payload(LIVE_REVIEW_QUEUE_DIR, review_item_id, item.model_dump())


def _build_run_list(directory) -> dict:
    runs = [PersonalMaterialLiveRunRecord(**payload) for payload in read_payloads(directory)]
    runs = sorted(runs, key=lambda run: run.created_at, reverse=True)
    return PersonalMaterialLiveRunList(
        runs=runs,
        run_count=len(runs),
        warnings=["Live run list contains metadata only. No raw OCR text, document content, local path, or provider secret is returned."],
    ).model_dump()


def _validate_review_action(request: PersonalMaterialLiveReviewActionRequest) -> list[str]:
    blocked: list[str] = []
    if not request.explicit_review_confirmation:
        blocked.append("explicit_review_confirmation is required")
    if not request.raw_content_handling_acknowledged:
        blocked.append("raw_content_handling_acknowledged is required")
    if not request.no_ai_prompt_injection_acknowledged:
        blocked.append("no_ai_prompt_injection_acknowledged is required")
    return blocked
