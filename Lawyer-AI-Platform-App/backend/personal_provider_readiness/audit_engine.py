from datetime import datetime, timezone

from personal_provider_readiness.provider_registry import list_provider_metadata
from personal_provider_readiness.schemas import ProviderAuditEvent, ProviderAuditTimeline


def now_iso() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def build_audit_timeline() -> dict:
    events = [
        ProviderAuditEvent(
            event_id=f"provider_audit_{index + 1:03d}",
            provider_id=provider.provider_id,
            action="provider_readiness_metadata_checked",
            created_at=now_iso(),
            warnings=["Audit event records metadata lookup only; no secret value or provider response is logged."],
        )
        for index, provider in enumerate(list_provider_metadata()[:5])
    ]
    return ProviderAuditTimeline(events=events, event_count=len(events)).model_dump()

