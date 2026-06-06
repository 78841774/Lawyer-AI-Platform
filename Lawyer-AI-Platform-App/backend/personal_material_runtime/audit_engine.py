from uuid import uuid4

from personal_material_runtime.schemas import PersonalMaterialAuditEvent, PersonalMaterialAuditTimeline, PersonalMaterialLiveAuditEvent, PersonalMaterialLiveAuditTimeline
from personal_material_runtime.storage import AUDIT_DIR, LIVE_AUDIT_DIR, read_payloads, write_payload


def record_audit_event(
    *,
    event_type: str,
    case_id: str,
    material_id: str,
    provider_id: str,
    job_id: str,
    created_at: str,
    manual_approval_confirmed: bool = True,
) -> None:
    event_id = f"personal_material_audit_{uuid4().hex[:12]}"
    event = PersonalMaterialAuditEvent(
        event_id=event_id,
        event_type=event_type,
        case_id=case_id,
        material_id=material_id,
        provider_id=provider_id,
        job_id=job_id,
        manual_approval_confirmed=manual_approval_confirmed,
        created_at=created_at,
    )
    write_payload(AUDIT_DIR, event_id, event.model_dump())


def build_audit_timeline() -> dict:
    events = [PersonalMaterialAuditEvent(**payload) for payload in read_payloads(AUDIT_DIR)]
    events = sorted(events, key=lambda event: event.created_at, reverse=True)
    return PersonalMaterialAuditTimeline(
        events=events,
        event_count=len(events),
        warnings=["Audit records contain metadata only. No source document text, local path, or provider secret is returned."],
    ).model_dump()


def record_live_audit_event(
    *,
    provider_id: str,
    action: str,
    actor_id: str,
    created_at: str,
    run_id: str | None = None,
    review_item_id: str | None = None,
    live_call_requested: bool = False,
    live_call_executed: bool = False,
    blocked_reason: str | None = None,
    source_trace_created: bool = False,
    page_count: int = 0,
) -> None:
    event_id = f"personal_material_live_audit_{uuid4().hex[:12]}"
    event = PersonalMaterialLiveAuditEvent(
        event_id=event_id,
        provider_id=provider_id,
        action=action,
        actor_id="redacted_actor" if actor_id else "system",
        run_id=run_id,
        review_item_id=review_item_id,
        live_call_requested=live_call_requested,
        live_call_executed=live_call_executed,
        blocked_reason=blocked_reason,
        source_trace_created=source_trace_created,
        page_count=page_count,
        created_at=created_at,
    )
    write_payload(LIVE_AUDIT_DIR, event_id, event.model_dump())


def build_live_audit_timeline() -> dict:
    events = [PersonalMaterialLiveAuditEvent(**payload) for payload in read_payloads(LIVE_AUDIT_DIR)]
    events = sorted(events, key=lambda event: event.created_at, reverse=True)
    return PersonalMaterialLiveAuditTimeline(
        events=events,
        event_count=len(events),
        warnings=["Live audit records contain metadata only. No OCR text, document text, local path, or provider secret is returned."],
    ).model_dump()
