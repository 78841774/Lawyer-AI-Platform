from datetime import UTC, datetime

from personal_skill_studio.training_artifacts.case_analysis_output_safety_engine import v733_safety_flags
from personal_skill_studio.training_artifacts.schemas import (
    CaseAnalysisOutputFeedback,
    CaseAnalysisOutputFeedbackRequest,
)


def build_output_feedback(output_id: str, request: CaseAnalysisOutputFeedbackRequest) -> CaseAnalysisOutputFeedback | None:
    if not request.explicit_metadata_only_confirmation or not request.explicit_no_training_confirmation:
        return None
    now = datetime.now(UTC).isoformat()
    return CaseAnalysisOutputFeedback(
        feedback_id=f"{output_id}_feedback_{now.replace(':', '').replace('.', '')}",
        output_id=output_id,
        reviewer_id=request.reviewer_id,
        feedback_type=request.feedback_type,
        feedback_summary=request.feedback_summary,
        severity=request.severity,
        source_trace_id=f"{output_id}_feedback_source_trace",
        audit_id=f"{output_id}_feedback_audit",
        created_at=now,
        warnings=["Feedback is metadata-only and does not update packages or trigger training."],
        **v733_safety_flags(),
    )
