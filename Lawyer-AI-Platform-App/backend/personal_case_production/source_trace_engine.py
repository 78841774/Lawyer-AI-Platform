from personal_case_production.schemas import CaseProductionSourceTrace, CaseProductionSourceTraceList
from personal_case_production.storage import SOURCE_TRACES_DIR, read_payload, read_payloads, write_payload


def create_source_trace(
    *,
    source_trace_id: str,
    source_type: str,
    source_label: str,
    linked_object_type: str,
    linked_object_id: str,
    created_at: str,
    production_case_id: str | None = None,
    workflow_run_id: str | None = None,
    stage_run_id: str | None = None,
) -> CaseProductionSourceTrace:
    trace = CaseProductionSourceTrace(
        source_trace_id=source_trace_id,
        source_type=source_type,
        source_label=source_label,
        linked_object_type=linked_object_type,
        linked_object_id=linked_object_id,
        production_case_id=production_case_id,
        workflow_run_id=workflow_run_id,
        stage_run_id=stage_run_id,
        created_at=created_at,
    )
    write_payload(SOURCE_TRACES_DIR, source_trace_id, trace.model_dump())
    return trace


def get_source_trace(source_trace_id: str) -> CaseProductionSourceTrace | None:
    payload = read_payload(SOURCE_TRACES_DIR, source_trace_id)
    return CaseProductionSourceTrace(**payload) if payload else None


def list_source_traces() -> list[CaseProductionSourceTrace]:
    return [CaseProductionSourceTrace(**payload) for payload in read_payloads(SOURCE_TRACES_DIR)]


def build_source_trace_list() -> dict:
    traces = sorted(list_source_traces(), key=lambda trace: trace.created_at, reverse=True)
    return CaseProductionSourceTraceList(source_traces=traces, source_trace_count=len(traces), warnings=["Source Trace 仅记录生产流程 metadata。"]).model_dump()
