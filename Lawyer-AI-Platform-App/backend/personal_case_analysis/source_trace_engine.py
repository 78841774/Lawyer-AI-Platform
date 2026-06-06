from personal_case_analysis.schemas import CaseAnalysisSourceTrace, CaseAnalysisSourceTraceList
from personal_case_analysis.storage import SOURCE_TRACES_DIR, read_payload, read_payloads, write_payload


def create_source_trace(
    *,
    source_trace_id: str,
    source_type: str,
    source_label: str,
    linked_object_type: str,
    linked_object_id: str,
    created_at: str,
    case_id: str | None = None,
    run_id: str | None = None,
) -> CaseAnalysisSourceTrace:
    trace = CaseAnalysisSourceTrace(
        source_trace_id=source_trace_id,
        source_type=source_type,
        source_label=source_label,
        linked_object_type=linked_object_type,
        linked_object_id=linked_object_id,
        case_id=case_id,
        run_id=run_id,
        created_at=created_at,
    )
    write_payload(SOURCE_TRACES_DIR, source_trace_id, trace.model_dump())
    return trace


def get_source_trace(source_trace_id: str) -> CaseAnalysisSourceTrace | None:
    payload = read_payload(SOURCE_TRACES_DIR, source_trace_id)
    return CaseAnalysisSourceTrace(**payload) if payload else None


def list_source_traces() -> list[CaseAnalysisSourceTrace]:
    return [CaseAnalysisSourceTrace(**payload) for payload in read_payloads(SOURCE_TRACES_DIR)]


def build_source_trace_list() -> dict:
    traces = sorted(list_source_traces(), key=lambda trace: trace.created_at, reverse=True)
    return CaseAnalysisSourceTraceList(
        source_traces=traces,
        source_trace_count=len(traces),
        warnings=["来源追踪仅记录 v7.16 实战分析 metadata，不包含原文、OCR 原文或本地路径。"],
    ).model_dump()
