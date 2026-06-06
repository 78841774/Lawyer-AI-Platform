from personal_material_runtime.schemas import (
    PersonalMaterialLiveSourceTrace,
    PersonalMaterialLiveSourceTraceList,
    PersonalMaterialSourceTrace,
    PersonalMaterialSourceTraceList,
)
from personal_material_runtime.storage import LIVE_SOURCE_TRACES_DIR, SOURCE_TRACES_DIR, read_payloads, write_payload


def create_source_traces(
    *,
    case_id: str,
    material_id: str,
    job_id: str,
    source_type: str,
    provider_id: str,
    created_at: str,
    block_count: int = 1,
) -> list[PersonalMaterialSourceTrace]:
    traces: list[PersonalMaterialSourceTrace] = []
    for index in range(block_count):
        source_trace_id = f"personal_material_source_trace_{job_id}_{index + 1}"
        trace = PersonalMaterialSourceTrace(
            source_trace_id=source_trace_id,
            case_id=case_id,
            material_id=material_id,
            job_id=job_id,
            source_type=source_type,
            provider_id=provider_id,
            page_number=1,
            block_id=f"mock_block_{index + 1}",
            bbox={"x": 0, "y": index * 24, "w": 100, "h": 20},
            confidence=0.91 if index == 0 else 0.88,
            created_at=created_at,
        )
        write_payload(SOURCE_TRACES_DIR, source_trace_id, trace.model_dump())
        traces.append(trace)
    return traces


def list_source_traces() -> list[PersonalMaterialSourceTrace]:
    return [PersonalMaterialSourceTrace(**payload) for payload in read_payloads(SOURCE_TRACES_DIR)]


def build_source_trace_list() -> dict:
    traces = sorted(list_source_traces(), key=lambda trace: trace.created_at, reverse=True)
    return PersonalMaterialSourceTraceList(
        source_traces=traces,
        source_trace_count=len(traces),
        warnings=["Source traces are mock metadata only and do not expose recognized source text or local file paths."],
    ).model_dump()


def create_live_source_trace(
    *,
    run_id: str,
    run_type: str,
    provider_id: str,
    case_id: str,
    material_id: str,
    created_at: str,
    page_count: int,
) -> PersonalMaterialLiveSourceTrace:
    source_trace_id = f"personal_material_live_source_trace_{run_id}"
    trace = PersonalMaterialLiveSourceTrace(
        source_trace_id=source_trace_id,
        run_id=run_id,
        run_type=run_type,
        provider_id=provider_id,
        case_id=case_id,
        material_id=material_id,
        source_type=f"{run_type}_metadata_preview",
        page_count=page_count,
        created_at=created_at,
    )
    write_payload(LIVE_SOURCE_TRACES_DIR, source_trace_id, trace.model_dump())
    return trace


def build_live_source_trace_list() -> dict:
    traces = [PersonalMaterialLiveSourceTrace(**payload) for payload in read_payloads(LIVE_SOURCE_TRACES_DIR)]
    traces = sorted(traces, key=lambda trace: trace.created_at, reverse=True)
    return PersonalMaterialLiveSourceTraceList(
        source_traces=traces,
        source_trace_count=len(traces),
        warnings=["Live source traces are metadata-only and never include OCR text or document content."],
    ).model_dump()
