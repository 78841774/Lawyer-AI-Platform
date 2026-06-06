from datetime import UTC, datetime

from personal_skill_studio.training_artifacts.case_analysis_output_safety_engine import v733_safety_flags
from personal_skill_studio.training_artifacts.schemas import CaseAnalysisRuntimeOutput


FACT_OUTPUT_DEFINITIONS = [
    ("case_fact_summary", "案件事实摘要", "提炼经脱敏抽象后的案件事实结构，供律师复核。", "low"),
    ("key_fact_list", "关键事实清单", "列出影响争点、证据与责任判断的关键事实项，供律师校对。", "low"),
]


def build_fact_outputs(runtime_load_id: str, usage_event_id: str | None, experience_ids: list[str]) -> list[CaseAnalysisRuntimeOutput]:
    now = datetime.now(UTC).isoformat()
    outputs = []
    for index, (output_type, title, summary, risk_level) in enumerate(FACT_OUTPUT_DEFINITIONS, start=1):
        output_id = f"case_analysis_fact_{output_type}_v733"
        outputs.append(
            CaseAnalysisRuntimeOutput(
                output_id=output_id,
                group_id="fact_extraction",
                output_type=output_type,
                output_title=title,
                output_order=index,
                output_summary_redacted=summary,
                output_detail_redacted=f"{title}为 Skill Output Schema 定义的事实类辅助产出，仅包含脱敏抽象摘要，不形成最终事实认定。",
                risk_level=risk_level,
                source_experience_ids=experience_ids[:3],
                source_runtime_load_id=runtime_load_id,
                source_usage_event_id=usage_event_id,
                source_trace_id=f"{output_id}_source_trace",
                audit_id=f"{output_id}_audit",
                allowed_actions=["view_detail", "submit_feedback", "create_risk_event", "view_audit", "view_source_trace", "mark_reviewed"],
                created_at=now,
                updated_at=now,
                **v733_safety_flags(),
            )
        )
    return outputs
