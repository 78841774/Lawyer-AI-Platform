from personal_trial_readiness.schemas import TrialAuditEvent, TrialAuditTimeline
from personal_trial_readiness.trial_session_engine import now_iso


def build_audit_timeline() -> dict:
    events = [
        TrialAuditEvent(
            event_id="trial_audit_001",
            action="trial_readiness_status_viewed",
            object_type="trial_readiness_runtime",
            object_id="personal_trial_readiness_runtime",
            created_at=now_iso(),
        ),
        TrialAuditEvent(
            event_id="trial_audit_002",
            action="safety_confirmation_metadata_ready",
            object_type="safety_confirmation",
            object_id="trial_mock_001",
            created_at=now_iso(),
        ),
    ]
    return TrialAuditTimeline(events=events, event_count=len(events)).model_dump()

