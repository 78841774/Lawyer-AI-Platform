from personal_skill_studio.training_artifacts.case_analysis_output_safety_engine import v733_safety_flags
from personal_skill_studio.training_artifacts.schemas import CaseAnalysisOutputSourceTrace, CaseAnalysisRuntimeOutput


def build_output_source_trace(output: CaseAnalysisRuntimeOutput) -> CaseAnalysisOutputSourceTrace:
    return CaseAnalysisOutputSourceTrace(
        output_id=output.output_id,
        source_trace_id=output.source_trace_id,
        source_experience_ids=output.source_experience_ids,
        source_runtime_load_id=output.source_runtime_load_id,
        source_usage_event_id=output.source_usage_event_id,
        trace_summary=[
            "Output definition comes from Case Analysis Skill Output Schema.",
            "Runtime load and experience package linkage are metadata-only.",
            "Trace view does not expose case source content.",
        ],
        warnings=["Source trace view contains identifiers and summaries only."],
        **v733_safety_flags(),
    )
