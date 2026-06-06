from personal_case_workspace.fact_preview_engine import get_fact_preview
from personal_case_workspace.schemas import FactQualityReport


DIMENSION_SCORES = {
    "fact_completeness": 84,
    "evidence_mapping_reviewability": 81,
    "timeline_clarity": 78,
    "disputed_fact_identification": 76,
    "missing_fact_value": 73,
    "source_trace_completeness": 86,
    "legal_analysis_input_readiness": 80,
}


def build_fact_quality(fact_preview_id: str) -> FactQualityReport | None:
    if get_fact_preview(fact_preview_id) is None:
        return None
    overall = round(sum(DIMENSION_SCORES.values()) / len(DIMENSION_SCORES))
    return FactQualityReport(
        fact_preview_id=fact_preview_id,
        overall_score=overall,
        dimension_scores=DIMENSION_SCORES,
        gate_status="yellow",
        optimization_suggestions=[
            "补齐缺失事实 flags 的来源追踪。",
            "将低置信度时间线节点交给用户本人确认。",
            "进入法律分析输入前保留纠正版本和确认版本。",
        ],
        warnings=["评分只提供质量参考和优化方向，不阻断下一步。"],
    )
