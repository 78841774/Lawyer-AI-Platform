from personal_legal_enterprise_gateway.audit_engine import now_iso
from personal_legal_enterprise_gateway.schemas import SourceTraceList, SourceTraceRecord
from personal_legal_enterprise_gateway.storage import SOURCE_TRACE_DIR, read_payloads, write_payload


def create_source_trace(run_id: str, provider_id: str, source_type: str) -> str:
    source_trace_id = f"source_trace_{run_id}"
    trace = SourceTraceRecord(
        source_trace_id=source_trace_id,
        run_id=run_id,
        provider_id=provider_id,
        source_type=source_type,
        created_at=now_iso(),
    )
    write_payload(SOURCE_TRACE_DIR, source_trace_id, trace.model_dump())
    return source_trace_id


def build_source_traces() -> dict:
    traces = [SourceTraceRecord(**payload) for payload in read_payloads(SOURCE_TRACE_DIR)]
    return SourceTraceList(source_traces=traces, source_trace_count=len(traces)).model_dump()

