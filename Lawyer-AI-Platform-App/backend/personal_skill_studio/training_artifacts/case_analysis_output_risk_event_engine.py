from datetime import UTC, datetime

from personal_skill_studio.training_artifacts.case_analysis_output_safety_engine import v733_safety_flags
from personal_skill_studio.training_artifacts.schemas import (
    CaseAnalysisOutputRiskEvent,
    CaseAnalysisOutputRiskEventRequest,
)


def build_output_risk_event(output_id: str, request: CaseAnalysisOutputRiskEventRequest) -> CaseAnalysisOutputRiskEvent | None:
    if not request.explicit_metadata_only_confirmation or not request.explicit_no_external_delivery_confirmation:
        return None
    now = datetime.now(UTC).isoformat()
    return CaseAnalysisOutputRiskEvent(
        risk_event_id=f"{output_id}_risk_{now.replace(':', '').replace('.', '')}",
        output_id=output_id,
        reporter_id=request.reporter_id,
        risk_level=request.risk_level,
        risk_summary=request.risk_summary,
        mitigation_note=request.mitigation_note,
        source_trace_id=f"{output_id}_risk_source_trace",
        audit_id=f"{output_id}_risk_audit",
        created_at=now,
        warnings=["Risk event is metadata-only and does not block or deliver work externally."],
        **v733_safety_flags(),
    )
