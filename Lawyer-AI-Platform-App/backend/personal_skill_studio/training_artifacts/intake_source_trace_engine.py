from personal_skill_studio.training_artifacts.schemas import TrainingIntakeSourceTrace


def build_source_traces(intake_id: str) -> list[TrainingIntakeSourceTrace]:
    return [
        TrainingIntakeSourceTrace(
            source_trace_id=f"{intake_id}_source_case_metadata",
            intake_id=intake_id,
            source_type="closed_case_training_material_metadata",
            source_label="authorized_closed_case_metadata",
            retained_metadata_fields=[
                "case_cause_path",
                "subject_type",
                "jurisdiction_context",
                "timeline_markers",
                "evidence_type",
            ],
        ),
        TrainingIntakeSourceTrace(
            source_trace_id=f"{intake_id}_source_redaction_report",
            intake_id=intake_id,
            source_type="redaction_report_metadata",
            source_label="redaction_quality_metadata",
            retained_metadata_fields=[
                "personal_identifiers_removed",
                "legal_relevance_preserved",
                "jurisdiction_context_preserved",
                "age_capacity_context_preserved",
            ],
        ),
    ]
