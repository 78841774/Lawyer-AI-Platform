from uuid import uuid4

from personal_case_analysis.safety_engine import default_safety_flags
from personal_case_analysis.schemas import CaseAnalysisAuditEvent, CaseAnalysisAuditTimeline
from personal_case_analysis.storage import AUDIT_DIR, read_payloads, write_payload


def record_audit_event(*, action: str, actor: str, object_type: str, object_id: str, timestamp: str) -> None:
    audit_id = f"personal_case_analysis_audit_{uuid4().hex[:12]}"
    event = CaseAnalysisAuditEvent(
        audit_id=audit_id,
        action=action,
        actor="system" if actor == "system" else "redacted_reviewer",
        object_type=object_type,
        object_id=object_id,
        timestamp=timestamp,
        safety_flags=default_safety_flags(),
    )
    write_payload(AUDIT_DIR, audit_id, event.model_dump())


def build_audit_timeline() -> dict:
    events = [CaseAnalysisAuditEvent(**payload) for payload in read_payloads(AUDIT_DIR)]
    events = sorted(events, key=lambda event: event.timestamp, reverse=True)
    return CaseAnalysisAuditTimeline(
        events=events,
        event_count=len(events),
        warnings=["审计记录仅包含 v7.16 runtime metadata，不包含 API key、raw content 或本地路径。"],
    ).model_dump()
