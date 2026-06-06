from personal_production_pilot.schemas import PilotSourceTrace, PilotSourceTraceList
from personal_production_pilot.storage import SOURCE_TRACES_DIR, read_payloads, write_payload


def create_source_trace(
    *,
    source_trace_id: str,
    source_type: str,
    source_label: str,
    linked_object_type: str,
    linked_object_id: str,
    created_at: str,
    run_id: str | None = None,
) -> PilotSourceTrace:
    trace = PilotSourceTrace(
        source_trace_id=source_trace_id,
        source_type=source_type,
        source_label=source_label,
        linked_object_type=linked_object_type,
        linked_object_id=linked_object_id,
        run_id=run_id,
        created_at=created_at,
    )
    write_payload(SOURCE_TRACES_DIR, source_trace_id, trace.model_dump())
    return trace


def list_source_traces() -> list[PilotSourceTrace]:
    return [PilotSourceTrace(**payload) for payload in read_payloads(SOURCE_TRACES_DIR)]


def build_source_trace_list() -> dict:
    traces = sorted(list_source_traces(), key=lambda trace: trace.created_at, reverse=True)
    return PilotSourceTraceList(
        source_traces=traces,
        source_trace_count=len(traces),
        warnings=["Source trace contains metadata only; no raw content is returned in diagnostics or regression output."],
    ).model_dump()
