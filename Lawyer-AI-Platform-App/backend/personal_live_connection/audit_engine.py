from datetime import datetime, timezone
from uuid import uuid4

from personal_live_connection.provider_registry import list_providers
from personal_live_connection.schemas import LiveConnectionAuditEvent, LiveConnectionAuditTimeline
from personal_live_connection.storage import AUDIT_DIR, read_payloads, write_payload


def now_iso() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def record_audit_event(provider_id: str, action: str, run_id: str | None = None) -> None:
    event_id = f"personal_live_audit_{uuid4().hex[:12]}"
    event = LiveConnectionAuditEvent(
        event_id=event_id,
        provider_id=provider_id,
        action=action,
        run_id=run_id,
        created_at=now_iso(),
        warnings=["Audit event records metadata only; no secret, raw content, local path, or provider response is logged."],
    )
    write_payload(AUDIT_DIR, event_id, event.model_dump())


def build_audit_timeline() -> dict:
    events = [LiveConnectionAuditEvent(**payload) for payload in read_payloads(AUDIT_DIR)]
    if not events:
        events = [
            LiveConnectionAuditEvent(
                event_id=f"personal_live_audit_seed_{index + 1:03d}",
                provider_id=provider.provider_id,
                action="provider_live_connection_metadata_checked",
                created_at=now_iso(),
            )
            for index, provider in enumerate(list_providers()[:4])
        ]
    events = sorted(events, key=lambda event: event.created_at, reverse=True)
    return LiveConnectionAuditTimeline(
        events=events,
        event_count=len(events),
        warnings=["Audit timeline is metadata-only and redacted."],
    ).model_dump()

