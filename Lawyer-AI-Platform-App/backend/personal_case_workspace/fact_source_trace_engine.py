from personal_case_workspace.fact_preview_engine import get_fact_preview
from personal_case_workspace.schemas import CaseWorkspaceSourceTrace, CaseWorkspaceSourceTraceList


def build_fact_source_traces(fact_preview_id: str) -> CaseWorkspaceSourceTraceList | None:
    preview = get_fact_preview(fact_preview_id)
    if preview is None:
        return None
    traces = [
        CaseWorkspaceSourceTrace(
            source_trace_id=source_trace_id,
            linked_object_type="fact_preview",
            linked_object_id=fact_preview_id,
            source_label="事实预览来源追踪 metadata",
            trace_status="fact_preview_trace_metadata",
            confirmed=source_trace_id.endswith("001"),
            warnings=["事实来源只返回 metadata，不返回材料正文或 OCR 原文。"],
        )
        for source_trace_id in preview.source_trace_ids
    ]
    return CaseWorkspaceSourceTraceList(
        source_traces=traces,
        source_trace_count=len(traces),
        confirmed_count=sum(1 for trace in traces if trace.confirmed),
        warnings=["事实预览进入法律分析输入前需要来源追踪确认。"],
    )
