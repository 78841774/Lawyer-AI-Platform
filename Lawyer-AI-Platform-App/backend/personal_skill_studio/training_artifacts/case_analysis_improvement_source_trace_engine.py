from personal_skill_studio.training_artifacts.case_analysis_improvement_safety_engine import v734_safety_flags
from personal_skill_studio.training_artifacts.schemas import CaseAnalysisImprovementCandidate, CaseAnalysisImprovementSourceTrace


def build_candidate_source_trace(candidate: CaseAnalysisImprovementCandidate) -> CaseAnalysisImprovementSourceTrace:
    return CaseAnalysisImprovementSourceTrace(
        candidate_id=candidate.candidate_id,
        source_trace_id=candidate.source_trace_id,
        source_output_id=candidate.source_output_id,
        source_feedback_ids=candidate.source_feedback_ids,
        source_risk_event_ids=candidate.source_risk_event_ids,
        source_audit_ids=candidate.source_audit_ids,
        source_trace_ids=candidate.source_trace_ids,
        trace_summary=[
            "Candidate links to v7.33 schema output metadata.",
            "Feedback and risk event references are retained for later human review.",
            "Experience package references are identifiers only and are not modified by this layer.",
        ],
        warnings=["Source trace contains metadata references only."],
        **v734_safety_flags(),
    )
