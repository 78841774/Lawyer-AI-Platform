from datetime import UTC, datetime

from personal_skill_studio.training_artifacts.case_analysis_improvement_safety_engine import v734_safety_flags
from personal_skill_studio.training_artifacts.case_analysis_runtime_output_registry import list_workbench_views
from personal_skill_studio.training_artifacts.schemas import (
    CaseAnalysisOutputToExperienceTrace,
    CaseAnalysisOutputToExperienceTraceList,
)


def build_output_to_experience_traces() -> list[CaseAnalysisOutputToExperienceTrace]:
    traces: list[CaseAnalysisOutputToExperienceTrace] = []
    for view in _views():
        for group in view.get("output_groups", []):
            for output in group.get("outputs", []):
                traces.append(_build_trace(view, group, output))
    return traces


def list_output_to_experience_traces() -> dict:
    traces = build_output_to_experience_traces()
    return CaseAnalysisOutputToExperienceTraceList(
        output_traces=traces,
        trace_count=len(traces),
        warnings=["Output trace records are metadata-only and do not expose source materials."],
        **v734_safety_flags(),
    ).model_dump()


def get_output_to_experience_trace(trace_id: str) -> dict | None:
    for trace in build_output_to_experience_traces():
        if trace.trace_id == trace_id:
            return trace.model_dump()
    return None


def get_output_to_experience_trace_by_output(output_id: str) -> CaseAnalysisOutputToExperienceTrace | None:
    for trace in build_output_to_experience_traces():
        if trace.output_id == output_id:
            return trace
    return None


def _build_trace(view: dict, group: dict, output: dict) -> CaseAnalysisOutputToExperienceTrace:
    now = datetime.now(UTC).isoformat()
    experience_card_ids = list(output.get("source_experience_ids") or [])
    missing: list[str] = []
    if not experience_card_ids:
        missing.append("Experience card linkage is not available; trace remains partial.")
    if not output.get("source_trace_id"):
        missing.append("Source trace reference is not available.")
    if not output.get("audit_id"):
        missing.append("Audit reference is not available.")
    if not output.get("source_trace_id") or not output.get("audit_id"):
        trace_status = "blocked"
    elif not experience_card_ids:
        trace_status = "partial"
    else:
        trace_status = "complete"
    return CaseAnalysisOutputToExperienceTrace(
        trace_id=f"{output.get('output_id')}_experience_trace_v734",
        output_id=output.get("output_id", "unknown_output"),
        output_group=group.get("group_type") or group.get("group_id", "unknown_group"),
        output_type=output.get("output_type", "unknown_output_type"),
        runtime_load_id=output.get("source_runtime_load_id") or view.get("runtime_load_id", "runtime_load_pending"),
        package_id=view.get("package_id", "package_pending"),
        package_version=view.get("package_version", "version_pending"),
        experience_package_id=view.get("package_id", "package_pending"),
        experience_card_ids=experience_card_ids,
        skill_schema_id=f"{view.get('skill_id', 'case_analysis_skill')}_output_schema_v733",
        skill_schema_version=view.get("skill_version", "v7.33"),
        usage_event_id=output.get("source_usage_event_id"),
        audit_id=output.get("audit_id") or f"{output.get('output_id')}_audit_missing",
        source_trace_id=output.get("source_trace_id") or f"{output.get('output_id')}_trace_missing",
        trace_status=trace_status,
        missing_trace_warnings=missing,
        created_at=now,
        warnings=["Trace links case-analysis output metadata to experience metadata only."],
        **v734_safety_flags(),
    )


def _views() -> list[dict]:
    payload = list_workbench_views()
    return payload.get("views", []) or []
