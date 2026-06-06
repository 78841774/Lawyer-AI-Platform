from datetime import UTC, datetime

from personal_skill_studio.training_artifacts.case_analysis_output_safety_engine import v733_safety_flags
from personal_skill_studio.training_artifacts.case_analysis_risk_output_engine import count_risk_outputs
from personal_skill_studio.training_artifacts.schemas import (
    CaseAnalysisSummaryMetrics,
    CaseAnalysisWorkbenchView,
    CaseAnalysisSkillOutputSchema,
)


def build_case_analysis_workbench_view(
    *,
    case_id: str,
    case_cause_name: str,
    runtime_load_status: str,
    skill_output_schema: CaseAnalysisSkillOutputSchema,
) -> CaseAnalysisWorkbenchView:
    now = datetime.now(UTC).isoformat()
    outputs = [output for group in skill_output_schema.output_groups for output in group.outputs]
    risk_counts = count_risk_outputs(outputs)
    metrics = CaseAnalysisSummaryMetrics(
        total_outputs=len(outputs),
        fact_output_count=sum(1 for output in outputs if output.group_id == "fact_extraction"),
        legal_analysis_output_count=sum(1 for output in outputs if output.group_id == "legal_analysis"),
        risk_flagged_count=risk_counts["risk_flagged_count"],
        high_risk_count=risk_counts["high_risk_count"],
        feedback_count=sum(output.feedback_count for output in outputs),
        reviewed_count=sum(1 for output in outputs if output.output_status == "reviewed"),
        **v733_safety_flags(),
    )
    return CaseAnalysisWorkbenchView(
        view_id=f"case_analysis_workbench_{skill_output_schema.runtime_load_id}",
        case_id=case_id,
        case_cause_name=case_cause_name,
        package_id=skill_output_schema.package_id,
        package_version=skill_output_schema.package_version,
        runtime_load_id=skill_output_schema.runtime_load_id,
        runtime_load_status=runtime_load_status,
        skill_id=skill_output_schema.skill_id,
        skill_name=skill_output_schema.skill_name,
        skill_version=skill_output_schema.skill_version,
        output_groups=skill_output_schema.output_groups,
        summary_metrics=metrics,
        safety_summary={
            "schema_driven_output_only": True,
            "frontend_output_definition_forbidden": True,
            "metadata_only": True,
            "lawyer_review_required": True,
            "does_not_replace_lawyer_judgment": True,
            "provider_call_executed": False,
            "training_triggered": False,
            "final_legal_opinion_generated": False,
            "final_report_generated": False,
        },
        audit_id=f"case_analysis_workbench_{skill_output_schema.runtime_load_id}_audit",
        source_trace_id=f"case_analysis_workbench_{skill_output_schema.runtime_load_id}_source_trace",
        created_at=now,
        updated_at=now,
        warnings=[
            "Workbench view renders backend Skill Output Schema only.",
            "Outputs are auxiliary review metadata and do not replace lawyer judgment.",
        ],
        **v733_safety_flags(),
    )
