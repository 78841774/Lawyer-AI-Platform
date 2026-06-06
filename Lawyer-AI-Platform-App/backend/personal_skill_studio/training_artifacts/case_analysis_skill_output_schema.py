from datetime import UTC, datetime

from personal_skill_studio.training_artifacts.case_analysis_fact_output_engine import build_fact_outputs
from personal_skill_studio.training_artifacts.case_analysis_legal_output_engine import build_legal_outputs
from personal_skill_studio.training_artifacts.case_analysis_output_safety_engine import v733_safety_flags
from personal_skill_studio.training_artifacts.schemas import CaseAnalysisOutputGroup, CaseAnalysisSkillOutputSchema


def build_case_analysis_skill_output_schema(
    *,
    package_id: str,
    package_version: str,
    runtime_load_id: str,
    usage_event_id: str | None,
    experience_ids: list[str],
) -> CaseAnalysisSkillOutputSchema:
    now = datetime.now(UTC).isoformat()
    fact_outputs = build_fact_outputs(runtime_load_id, usage_event_id, experience_ids)
    legal_outputs = build_legal_outputs(runtime_load_id, usage_event_id, experience_ids)
    groups = [
        CaseAnalysisOutputGroup(
            group_id="fact_extraction",
            group_title="事实提炼",
            group_type="fact_extraction",
            expected_count=2,
            actual_count=len(fact_outputs),
            display_order=1,
            description="由案件事实提炼 Skill Output Schema 定义的事实类辅助产出。",
            outputs=fact_outputs,
            **v733_safety_flags(),
        ),
        CaseAnalysisOutputGroup(
            group_id="legal_analysis",
            group_title="法律分析",
            group_type="legal_analysis",
            expected_count=len(legal_outputs),
            actual_count=len(legal_outputs),
            display_order=2,
            description="由案件法律分析 Skill Output Schema 定义的法律分析类辅助产出。",
            outputs=legal_outputs,
            **v733_safety_flags(),
        ),
    ]
    return CaseAnalysisSkillOutputSchema(
        skill_id="case_analysis_skill_bundle",
        skill_name="案件分析 Skill 组合",
        skill_version="v7.33",
        package_id=package_id,
        package_version=package_version,
        runtime_load_id=runtime_load_id,
        output_groups=groups,
        created_at=now,
        audit_id="case_analysis_skill_output_schema_v733_audit",
        source_trace_id="case_analysis_skill_output_schema_v733_source_trace",
        safety_flags=v733_safety_flags(),
        warnings=[
            "Output groups, titles, types, order, and counts are defined by backend Skill Output Schema.",
            "The schema does not produce final legal opinions or formal reports.",
        ],
        **v733_safety_flags(),
    )
