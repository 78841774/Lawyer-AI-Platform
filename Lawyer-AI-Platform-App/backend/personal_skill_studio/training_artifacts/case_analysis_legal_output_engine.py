from datetime import UTC, datetime

from personal_skill_studio.training_artifacts.case_analysis_output_safety_engine import v733_safety_flags
from personal_skill_studio.training_artifacts.schemas import CaseAnalysisRuntimeOutput


LEGAL_OUTPUT_DEFINITIONS = [
    ("claim_basis_analysis", "请求基础分析", "梳理可能请求基础及其成立条件。", "medium"),
    ("legal_relationship_analysis", "法律关系分析", "识别合同、侵权或其他法律关系结构。", "low"),
    ("issue_identification", "争点识别", "归纳需律师重点确认的事实与法律争点。", "medium"),
    ("evidence_chain_analysis", "证据链分析", "提示证据链完整性与待补强方向。", "medium"),
    ("burden_of_proof_analysis", "举证责任分析", "提示主要争点对应的举证责任配置。", "medium"),
    ("statute_application_analysis", "规范适用分析", "列出需律师核验的规范适用路径。", "medium"),
    ("case_law_reference_analysis", "类案参考分析", "提示可检索类案方向，不作为最终引用。", "low"),
    ("risk_point_analysis", "风险点分析", "标记可能影响案件走向的风险点。", "high"),
    ("opponent_argument_prediction", "相对方观点预判", "整理相对方可能抗辩方向。", "medium"),
    ("litigation_strategy_analysis", "诉讼策略分析", "提供程序与实体策略辅助提示。", "medium"),
    ("damages_or_amount_analysis", "金额与损失分析", "提示金额构成、计算口径与证明风险。", "medium"),
    ("limitation_period_analysis", "时效期间分析", "提示时效、期间与程序节点核验方向。", "high"),
    ("procedural_risk_analysis", "程序风险分析", "提示管辖、保全、送达等程序风险。", "medium"),
    ("settlement_strategy_analysis", "和解策略分析", "提供和解空间与风险提示辅助。", "low"),
    ("drafting_points_analysis", "文书要点分析", "整理后续文书起草应关注的要点。", "low"),
    ("next_action_recommendation", "下一步行动建议", "列出需律师决定的下一步动作清单。", "medium"),
]


def build_legal_outputs(runtime_load_id: str, usage_event_id: str | None, experience_ids: list[str]) -> list[CaseAnalysisRuntimeOutput]:
    now = datetime.now(UTC).isoformat()
    outputs = []
    for index, (output_type, title, summary, risk_level) in enumerate(LEGAL_OUTPUT_DEFINITIONS, start=1):
        output_id = f"case_analysis_legal_{output_type}_v733"
        outputs.append(
            CaseAnalysisRuntimeOutput(
                output_id=output_id,
                group_id="legal_analysis",
                output_type=output_type,
                output_title=title,
                output_order=index,
                output_summary_redacted=summary,
                output_detail_redacted=f"{title}为 Skill Output Schema 定义的法律分析辅助产出，仅作律师复核线索，不生成最终法律意见。",
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
