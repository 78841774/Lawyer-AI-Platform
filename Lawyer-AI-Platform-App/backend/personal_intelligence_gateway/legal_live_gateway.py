from datetime import datetime, timezone
from uuid import uuid4

from personal_intelligence_gateway.audit_engine import record_live_audit_event
from personal_intelligence_gateway.live_guard import live_mode_enabled_for, validate_live_gate
from personal_intelligence_gateway.provider_config import get_live_provider_config
from personal_intelligence_gateway.query_boundary import validate_enterprise_query_boundary, validate_legal_query_boundary
from personal_intelligence_gateway.response_sanitizer import sanitize_live_run
from personal_intelligence_gateway.schemas import (
    PersonalIntelligenceLiveReviewActionRequest,
    PersonalIntelligenceLiveReviewActionResult,
    PersonalIntelligenceLiveReviewItem,
    PersonalIntelligenceLiveReviewQueue,
    PersonalIntelligenceLiveRunList,
    PersonalIntelligenceLiveRunRecord,
    PersonalIntelligenceLiveRunRequest,
)
from personal_intelligence_gateway.source_trace_engine import create_live_source_traces
from personal_intelligence_gateway.storage import (
    LIVE_ENTERPRISE_RUNS_DIR,
    LIVE_LEGAL_RUNS_DIR,
    LIVE_REVIEW_QUEUE_DIR,
    read_payload,
    read_payloads,
    write_payload,
)
from personal_intelligence_gateway.usage_meter import build_live_metadata_preview


LIVE_REVIEW_ACTIONS = {
    "approve_metadata_only": "metadata_approved",
    "request_manual_review": "manual_review_requested",
    "reject": "rejected",
    "mark_low_confidence": "low_confidence",
    "mark_irrelevant": "irrelevant",
    "request_source_verification": "source_verification_requested",
    "block_raw_content": "raw_content_blocked",
    "block_ai_prompt_injection": "ai_prompt_injection_blocked",
}


def execute_legal_live_run(request: PersonalIntelligenceLiveRunRequest, *, dry_run: bool) -> dict:
    return _execute_live_run(request.model_copy(update={"dry_run": dry_run}), run_type="legal")


def execute_enterprise_live_run(request: PersonalIntelligenceLiveRunRequest, *, dry_run: bool) -> dict:
    return _execute_live_run(request.model_copy(update={"dry_run": dry_run}), run_type="enterprise")


def list_legal_live_runs() -> dict:
    return _build_run_list(LIVE_LEGAL_RUNS_DIR)


def list_enterprise_live_runs() -> dict:
    return _build_run_list(LIVE_ENTERPRISE_RUNS_DIR)


def get_legal_live_run(run_id: str) -> PersonalIntelligenceLiveRunRecord | None:
    payload = read_payload(LIVE_LEGAL_RUNS_DIR, run_id)
    return PersonalIntelligenceLiveRunRecord(**payload) if payload else None


def get_enterprise_live_run(run_id: str) -> PersonalIntelligenceLiveRunRecord | None:
    payload = read_payload(LIVE_ENTERPRISE_RUNS_DIR, run_id)
    return PersonalIntelligenceLiveRunRecord(**payload) if payload else None


def build_live_review_queue() -> dict:
    items = [PersonalIntelligenceLiveReviewItem(**payload) for payload in read_payloads(LIVE_REVIEW_QUEUE_DIR)]
    items = sorted(items, key=lambda item: item.updated_at, reverse=True)
    return PersonalIntelligenceLiveReviewQueue(
        items=items,
        item_count=len(items),
        pending_review_count=sum(1 for item in items if item.review_status == "pending_review"),
        warnings=[
            "Live review queue is metadata-only.",
            "approve_metadata_only is not final citation and does not allow raw content into AI prompts.",
        ],
    ).model_dump()


def submit_live_review_action(review_item_id: str, request: PersonalIntelligenceLiveReviewActionRequest) -> dict:
    item_payload = read_payload(LIVE_REVIEW_QUEUE_DIR, review_item_id)
    if item_payload is None:
        return PersonalIntelligenceLiveReviewActionResult(
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
        return PersonalIntelligenceLiveReviewActionResult(
            review_item_id=review_item_id,
            action=request.action,
            status="blocked",
            blocked_reasons=blocked,
            warnings=["Review action blocked. Unsafe or incomplete confirmation metadata was not applied."],
        ).model_dump()

    item = PersonalIntelligenceLiveReviewItem(**item_payload)
    now = datetime.now(timezone.utc).isoformat()
    next_status = LIVE_REVIEW_ACTIONS[request.action]
    updated = item.model_copy(update={"review_status": next_status, "updated_at": now})
    write_payload(LIVE_REVIEW_QUEUE_DIR, review_item_id, updated.model_dump())
    record_live_audit_event(
        provider_id=item.provider_id,
        action=f"review_{request.action}",
        actor_id=request.actor_id,
        query_type=item.query_type,
        review_item_id=review_item_id,
        created_at=now,
    )
    return PersonalIntelligenceLiveReviewActionResult(
        review_item_id=review_item_id,
        action=request.action,
        status="review_action_recorded",
        review_status=next_status,
        warnings=[
            "Review action recorded as metadata only.",
            "No raw result, AI prompt injection, final citation, legal opinion, report, or external delivery was triggered.",
        ],
    ).model_dump()


def _execute_live_run(request: PersonalIntelligenceLiveRunRequest, *, run_type: str) -> dict:
    now = datetime.now(timezone.utc).isoformat()
    run_id = f"personal_intelligence_live_{run_type}_{uuid4().hex[:12]}"
    boundary = validate_legal_query_boundary(request) if run_type == "legal" else validate_enterprise_query_boundary(request)
    gate = validate_live_gate(request, run_type=run_type)
    blocked_reasons = [*boundary, *gate]
    provider = get_live_provider_config(request.provider_id)
    provider_type = provider.provider_type if provider else ("enterprise_info" if run_type == "enterprise" else "legal_search")
    metadata = build_live_metadata_preview(request, run_type=run_type, query_id=run_id)

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

    traces = create_live_source_traces(
        run_id=run_id,
        run_type=run_type,
        provider_id=request.provider_id,
        provider_type=provider_type,
        query_type=request.query_type,
        created_at=now,
        count=metadata.citation_candidate_count or metadata.enterprise_candidate_count or 1,
    )
    metadata.source_trace_ids = [trace.source_trace_id for trace in traces]
    record = PersonalIntelligenceLiveRunRecord(
        run_id=run_id,
        run_type=run_type,
        provider_id=request.provider_id,
        provider_type=provider_type,
        query_type=request.query_type,
        status=status,
        dry_run=request.dry_run,
        would_call_provider=would_call_provider,
        live_mode_enabled=live_mode_enabled_for(run_type),
        live_call_requested=not request.dry_run,
        live_call_executed=False,
        blocked_reason=blocked_reason,
        blocked_reasons=blocked_reasons,
        provider_adapter_unavailable=adapter_unavailable,
        metadata_preview=metadata,
        source_trace_created=True,
        created_at=now,
        warnings=[
            "v7.14 returns legal / enterprise metadata candidates only.",
            "Raw provider result content is not returned or injected into AI prompts.",
            "Citation candidates are not final citations.",
        ],
    )
    record = sanitize_live_run(record)
    directory = LIVE_LEGAL_RUNS_DIR if run_type == "legal" else LIVE_ENTERPRISE_RUNS_DIR
    write_payload(directory, run_id, record.model_dump())
    _create_review_item(record, now)
    record_live_audit_event(
        provider_id=request.provider_id,
        action=f"{run_type}_{'dry_run' if request.dry_run else 'live_attempt'}",
        actor_id=request.actor_id,
        query_type=request.query_type,
        run_id=run_id,
        live_call_requested=not request.dry_run,
        live_call_executed=False,
        blocked_reason=blocked_reason,
        source_trace_created=True,
        created_at=now,
    )
    return record.model_dump()


def _create_review_item(record: PersonalIntelligenceLiveRunRecord, created_at: str) -> None:
    review_item_id = f"personal_intelligence_live_review_{record.run_id}"
    item = PersonalIntelligenceLiveReviewItem(
        review_item_id=review_item_id,
        run_id=record.run_id,
        run_type=record.run_type,
        provider_id=record.provider_id,
        provider_type=record.provider_type,
        query_type=record.query_type,
        confidence_summary=record.metadata_preview.confidence_summary,
        citation_candidate=record.run_type == "legal",
        enterprise_candidate=record.run_type == "enterprise",
        created_at=created_at,
        updated_at=created_at,
        warnings=["Metadata-only review item. Raw provider content and final citation remain blocked."],
    )
    write_payload(LIVE_REVIEW_QUEUE_DIR, review_item_id, item.model_dump())


def _build_run_list(directory) -> dict:
    runs = [PersonalIntelligenceLiveRunRecord(**payload) for payload in read_payloads(directory)]
    runs = sorted(runs, key=lambda run: run.created_at, reverse=True)
    return PersonalIntelligenceLiveRunList(
        runs=runs,
        run_count=len(runs),
        warnings=["Live run list contains metadata only. No raw legal result, raw enterprise result, local path, API key, or final citation is returned."],
    ).model_dump()


def _validate_review_action(request: PersonalIntelligenceLiveReviewActionRequest) -> list[str]:
    blocked: list[str] = []
    if not request.explicit_review_confirmation:
        blocked.append("explicit_review_confirmation is required")
    if not request.raw_content_handling_acknowledged:
        blocked.append("raw_content_handling_acknowledged is required")
    if not request.no_ai_prompt_injection_acknowledged:
        blocked.append("no_ai_prompt_injection_acknowledged is required")
    if not request.no_final_citation_acknowledged:
        blocked.append("no_final_citation_acknowledged is required")
    return blocked
