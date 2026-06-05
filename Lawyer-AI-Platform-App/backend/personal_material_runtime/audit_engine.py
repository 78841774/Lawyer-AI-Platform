from uuid import uuid4

from personal_material_runtime.schemas import PersonalMaterialAuditEvent, PersonalMaterialAuditTimeline
from personal_material_runtime.storage import AUDIT_DIR, read_payloads, write_payload


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
