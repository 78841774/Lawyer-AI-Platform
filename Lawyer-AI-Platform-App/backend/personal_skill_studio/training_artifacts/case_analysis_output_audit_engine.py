from datetime import UTC, datetime

from personal_skill_studio.training_artifacts.case_analysis_output_safety_engine import v733_safety_flags
from personal_skill_studio.training_artifacts.schemas import CaseAnalysisOutputAudit


def build_output_audit(output_id: str, action: str = "schema_defined_output_visible") -> CaseAnalysisOutputAudit:
    now = datetime.now(UTC).isoformat()
    return CaseAnalysisOutputAudit(
        output_id=output_id,
        audit_id=f"{output_id}_audit",
        events=[
            {
                "audit_event_id": f"{output_id}_{action}",
                "action": action,
                "actor": "case_analysis_workbench_runtime",
                "timestamp": now,
                "summary": "Schema-defined metadata output was exposed for owner lawyer review.",
            }
        ],
        event_count=1,
        warnings=["Audit view contains metadata events only."],
        **v733_safety_flags(),
    )
