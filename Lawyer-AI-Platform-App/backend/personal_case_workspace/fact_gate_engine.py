from personal_case_workspace.fact_preview_engine import get_fact_preview
from personal_case_workspace.schemas import FactGateReport, LegalAnalysisInputConfirmRequest, LegalAnalysisInputReadiness, LegalAnalysisInputReadinessList


def build_fact_gate(fact_preview_id: str) -> FactGateReport | None:
    if get_fact_preview(fact_preview_id) is None:
        return None
    return FactGateReport(
        gate_id=f"fact_gate_{fact_preview_id}",
        fact_preview_id=fact_preview_id,
        gate_status="yellow",
        gate_score=80,
        optimization_required=True,
        optimization_suggestions=[
            "建议用户本人确认争议事实。",
            "建议补充缺失事实 metadata。",
            "建议确认 Source Trace 后再进入法律分析草稿。",
        ],
        warnings=["门控仅作为质量参考，不阻断下一步。"],
    )


def build_legal_analysis_input_readiness(fact_preview_id: str, owner_confirmed: bool = False) -> LegalAnalysisInputReadiness | None:
    preview = get_fact_preview(fact_preview_id)
    if preview is None:
        return None
    source_trace_ready = len(preview.source_trace_ids) > 0
    ready = owner_confirmed and source_trace_ready
    return LegalAnalysisInputReadiness(
        readiness_id=f"fact_input_readiness_{fact_preview_id}",
        fact_preview_id=fact_preview_id,
        legal_analysis_input_ready=ready,
        owner_confirmed=owner_confirmed,
        source_trace_ready=source_trace_ready,
        missing_fact_flags=["付款节点 metadata 待确认", "通知义务 metadata 待确认"] if not owner_confirmed else [],
        low_confidence_flags=["时间线置信度需人工确认"] if not owner_confirmed else [],
        warnings=[
            "ready 只是状态，不自动触发法律分析。",
            "后续 runtime 或用户动作决定是否进入法律分析草稿。",
        ],
    )


def list_legal_analysis_input_readiness() -> LegalAnalysisInputReadinessList:
    items = []
    for preview_id in ["fact_preview_mock_001"]:
        item = build_legal_analysis_input_readiness(preview_id, owner_confirmed=False)
        if item is not None:
            items.append(item)
    return LegalAnalysisInputReadinessList(
        readiness_items=items,
        readiness_count=len(items),
        warnings=["事实输入 ready 不会自动触发法律分析。"],
    )


def confirm_for_legal_analysis(fact_preview_id: str, request: LegalAnalysisInputConfirmRequest) -> LegalAnalysisInputReadiness | None:
    confirmed = (
        request.explicit_owner_confirmation
        and request.explicit_source_trace_confirmation
        and request.explicit_no_auto_legal_analysis_confirmation
        and request.explicit_no_training_data_confirmation
    )
    return build_legal_analysis_input_readiness(fact_preview_id, owner_confirmed=confirmed)
