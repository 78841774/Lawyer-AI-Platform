from personal_skill_studio.training_artifacts.schemas import (
    CaseCauseClassification,
    TrainingIntakeSourceTrace,
    TrainingSampleSegment,
)


SEGMENT_DEFINITIONS = [
    ("fact_summary", "case_fact_extraction_skill"),
    ("evidence_mapping", "case_fact_extraction_skill"),
    ("timeline", "case_fact_extraction_skill"),
    ("disputed_facts", "case_fact_extraction_skill"),
    ("missing_facts", "case_fact_extraction_skill"),
    ("legal_issues", "case_legal_analysis_skill"),
    ("claim_basis", "case_legal_analysis_skill"),
    ("defense_path", "case_legal_analysis_skill"),
    ("burden_of_proof", "case_legal_analysis_skill"),
    ("risk_assessment", "case_legal_analysis_skill"),
    ("next_actions", "case_legal_analysis_skill"),
]


def build_segments(classification: CaseCauseClassification, source_traces: list[TrainingIntakeSourceTrace]) -> list[TrainingSampleSegment]:
    source_trace_ids = [trace.source_trace_id for trace in source_traces]
    return [
        TrainingSampleSegment(
            segment_id=f"{classification.intake_id}_segment_{segment_type}",
            intake_id=classification.intake_id,
            segment_type=segment_type,
            case_cause_path=classification.case_cause_path,
            target_skill_id=target_skill_id,
            source_trace_ids=source_trace_ids,
            segment_metadata={
                "metadata_only": True,
                "raw_content_included": False,
                "redaction_completed": True,
                "legal_relevance_preserved": True,
                "case_cause_name": classification.case_cause_name,
            },
        )
        for segment_type, target_skill_id in SEGMENT_DEFINITIONS
    ]
