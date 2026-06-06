from datetime import datetime, timezone

from personal_intelligence_gateway.schemas import (
    PersonalIntelligenceLiveSourceTrace,
    PersonalIntelligenceLiveSourceTraceList,
    PersonalIntelligenceSourceTrace,
    PersonalIntelligenceSourceTraceList,
)
from personal_intelligence_gateway.storage import CONFIRMATION_QUEUE_DIR, LIVE_SOURCE_TRACES_DIR, SOURCE_TRACES_DIR, read_payload, read_payloads, write_payload


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


def create_live_source_traces(
    *,
    run_id: str,
    run_type: str,
    provider_id: str,
    provider_type: str,
    query_type: str,
    created_at: str,
    count: int,
) -> list[PersonalIntelligenceLiveSourceTrace]:
    traces: list[PersonalIntelligenceLiveSourceTrace] = []
    for index in range(1, count + 1):
        source_trace_id = f"personal_intelligence_live_source_trace_{run_id}_{index}"
        trace = PersonalIntelligenceLiveSourceTrace(
            source_trace_id=source_trace_id,
            provider_id=provider_id,
            provider_type=provider_type,
            query_id=run_id,
            query_type=query_type,
            source_title=f"{run_type} candidate metadata {index}",
            source_type="citation_candidate" if run_type == "legal" else "enterprise_candidate",
            source_reference=f"metadata_reference_{index}",
            citation_candidate=run_type == "legal",
            enterprise_candidate=run_type == "enterprise",
            created_at=created_at,
        )
        write_payload(LIVE_SOURCE_TRACES_DIR, source_trace_id, trace.model_dump())
        traces.append(trace)
    return traces


def get_live_source_trace(source_trace_id: str) -> PersonalIntelligenceLiveSourceTrace | None:
    payload = read_payload(LIVE_SOURCE_TRACES_DIR, source_trace_id)
    return PersonalIntelligenceLiveSourceTrace(**payload) if payload else None


def build_live_source_trace_list() -> dict:
    traces = [PersonalIntelligenceLiveSourceTrace(**payload) for payload in read_payloads(LIVE_SOURCE_TRACES_DIR)]
    traces = sorted(traces, key=lambda trace: trace.created_at, reverse=True)
    return PersonalIntelligenceLiveSourceTraceList(
        source_traces=traces,
        source_trace_count=len(traces),
        warnings=["Live source traces are candidate metadata only. No provider raw content, local path, or final citation is returned."],
    ).model_dump()
