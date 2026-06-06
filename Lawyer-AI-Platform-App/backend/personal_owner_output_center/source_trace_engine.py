from personal_owner_output_center.output_registry import get_registry_output, list_registry_outputs
from personal_owner_output_center.schemas import OwnerOutputSourceTrace, OwnerOutputSourceTraceList


def _traces_for_output(output_id: str) -> list[OwnerOutputSourceTrace]:
    output = get_registry_output(output_id)
    if output is None:
        return []
    count = max(1, min(output.source_trace_count, 4))
    return [
        OwnerOutputSourceTrace(
            source_trace_id=f"owner_output_trace_{output_id}_{index}",
            output_id=output_id,
            source_type="metadata_source_trace",
            source_label=f"{output.output_title} 来源追踪 metadata {index}",
            source_module=output.source_module,
            linked_source_id=output.source_id,
            warnings=["Source trace is metadata only and excludes raw content."],
        )
        for index in range(1, count + 1)
    ]


def build_source_trace_list(output_id: str | None = None) -> OwnerOutputSourceTraceList:
    traces = _traces_for_output(output_id) if output_id else [
        trace for output in list_registry_outputs() for trace in _traces_for_output(output.output_id)[:1]
    ]
    return OwnerOutputSourceTraceList(
        output_id=output_id,
        source_traces=traces,
        source_trace_count=len(traces),
        warnings=["Source trace list is metadata-only and safe for diagnostics."],
    )
