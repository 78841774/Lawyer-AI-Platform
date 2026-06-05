from datetime import datetime, timezone

from personal_intelligence_gateway.schemas import PersonalIntelligenceSourceTrace, PersonalIntelligenceSourceTraceList
from personal_intelligence_gateway.storage import CONFIRMATION_QUEUE_DIR, SOURCE_TRACES_DIR, read_payload, read_payloads, write_payload


def create_source_traces(
    *,
    provider_id: str,
    query_id: str,
    source_definitions: list[dict[str, str]],
    created_at: str,
) -> list[PersonalIntelligenceSourceTrace]:
    traces: list[PersonalIntelligenceSourceTrace] = []
    for index, definition in enumerate(source_definitions, start=1):
        source_trace_id = f"personal_intelligence_source_trace_{query_id}_{index}"
        trace = PersonalIntelligenceSourceTrace(
            source_trace_id=source_trace_id,
            source_type=definition["source_type"],
            provider_id=provider_id,
            external_source_label=definition["external_source_label"],
            source_category=definition["source_category"],
            query_id=query_id,
            created_at=created_at,
        )
        write_payload(SOURCE_TRACES_DIR, source_trace_id, trace.model_dump())
        write_payload(CONFIRMATION_QUEUE_DIR, source_trace_id, trace.model_dump())
        traces.append(trace)
    return traces


def get_source_trace(source_trace_id: str) -> PersonalIntelligenceSourceTrace | None:
    payload = read_payload(SOURCE_TRACES_DIR, source_trace_id)
    return PersonalIntelligenceSourceTrace(**payload) if payload else None


def save_source_trace(trace: PersonalIntelligenceSourceTrace) -> None:
    payload = trace.model_dump()
    write_payload(SOURCE_TRACES_DIR, trace.source_trace_id, payload)
    write_payload(CONFIRMATION_QUEUE_DIR, trace.source_trace_id, payload)


def list_source_traces() -> list[PersonalIntelligenceSourceTrace]:
    return [PersonalIntelligenceSourceTrace(**payload) for payload in read_payloads(SOURCE_TRACES_DIR)]


def build_source_trace_list() -> dict:
    traces = sorted(list_source_traces(), key=lambda trace: trace.created_at, reverse=True)
    return PersonalIntelligenceSourceTraceList(
        source_traces=traces,
        source_trace_count=len(traces),
        pending_confirmation_count=sum(1 for trace in traces if not trace.lawyer_confirmed),
        warnings=["Source Trace 仅为模拟 metadata，不包含外部原文或本地路径。"],
    ).model_dump()


def update_trace_confirmation(source_trace_id: str, citation_status: str, lawyer_confirmed: bool) -> PersonalIntelligenceSourceTrace | None:
    trace = get_source_trace(source_trace_id)
    if trace is None:
        return None
    updated = trace.model_copy(
        update={
            "citation_status": citation_status,
            "lawyer_confirmed": lawyer_confirmed,
            "updated_at": datetime.now(timezone.utc).isoformat(),
        }
    )
    save_source_trace(updated)
    return updated
