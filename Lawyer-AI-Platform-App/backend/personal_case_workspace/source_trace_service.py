from personal_case_workspace.schemas import CaseWorkspaceSourceTrace, CaseWorkspaceSourceTraceList
from personal_case_workspace.storage import MATERIALS


def build_source_traces(material_id: str | None = None) -> CaseWorkspaceSourceTraceList:
    traces: list[CaseWorkspaceSourceTrace] = []
    for material in MATERIALS:
        if material_id is not None and material.material_id != material_id:
            continue
        for source_trace_id in material.source_trace_ids:
            traces.append(
                CaseWorkspaceSourceTrace(
                    source_trace_id=source_trace_id,
                    linked_object_type="case_workspace_material",
                    linked_object_id=material.material_id,
                    source_label=f"{material.material_title} 来源追踪 metadata",
                    confirmed=source_trace_id.endswith("001"),
                    warnings=["来源追踪只返回 metadata，不返回原始材料片段。"],
                )
            )
    return CaseWorkspaceSourceTraceList(
        source_traces=traces,
        source_trace_count=len(traces),
        confirmed_count=sum(1 for trace in traces if trace.confirmed),
        warnings=["source_trace_required=true；律师复核后才能用于后续草稿。"],
    )
