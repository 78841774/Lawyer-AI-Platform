from datetime import UTC, datetime

from personal_skill_studio.training_artifacts.case_analysis_improvement_safety_engine import v734_safety_flags
from personal_skill_studio.training_artifacts.schemas import CaseAnalysisImprovementAudit, CaseAnalysisImprovementCandidate


def build_candidate_audit(candidate: CaseAnalysisImprovementCandidate) -> CaseAnalysisImprovementAudit:
    now = datetime.now(UTC).isoformat()
    events = [
        {
            "audit_event_id": f"{candidate.candidate_id}_mapped",
            "action": "mapped_from_case_analysis_output_feedback",
            "actor": "case_analysis_improvement_registry",
            "timestamp": candidate.created_at,
            "summary": "Candidate metadata was mapped from output feedback, risk event, audit, and trace references.",
        },
        {
            "audit_event_id": f"{candidate.candidate_id}_status",
            "action": candidate.candidate_status,
            "actor": "owner_controlled_metadata_layer",
            "timestamp": now,
            "summary": "Status metadata does not apply package, schema, runtime, or training changes.",
        },
    ]
    return CaseAnalysisImprovementAudit(
        candidate_id=candidate.candidate_id,
        audit_id=candidate.audit_id,
        events=events,
        event_count=len(events),
        warnings=["Audit contains metadata events only."],
        **v734_safety_flags(),
    )
