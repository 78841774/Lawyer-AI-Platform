from personal_skill_studio.schemas import SkillStudioSourceTrace, SkillStudioSourceTraceList
from personal_skill_studio.storage import SOURCE_TRACES_DIR, read_payload, read_payloads, write_payload


def create_source_trace(
    *,
    source_trace_id: str,
    source_type: str,
    source_label: str,
    linked_object_type: str,
    linked_object_id: str,
    created_at: str,
    case_id: str | None = None,
    experience_package_id: str | None = None,
    skill_candidate_id: str | None = None,
) -> SkillStudioSourceTrace:
    trace = SkillStudioSourceTrace(
        source_trace_id=source_trace_id,
        source_type=source_type,
        source_label=source_label,
        linked_object_type=linked_object_type,
        linked_object_id=linked_object_id,
        case_id=case_id,
        experience_package_id=experience_package_id,
        skill_candidate_id=skill_candidate_id,
        created_at=created_at,
    )
    write_payload(SOURCE_TRACES_DIR, source_trace_id, trace.model_dump())
    return trace


def get_source_trace(source_trace_id: str) -> SkillStudioSourceTrace | None:
    payload = read_payload(SOURCE_TRACES_DIR, source_trace_id)
    return SkillStudioSourceTrace(**payload) if payload else None


def list_source_traces() -> list[SkillStudioSourceTrace]:
    return [SkillStudioSourceTrace(**payload) for payload in read_payloads(SOURCE_TRACES_DIR)]


def build_source_trace_list() -> dict:
    traces = sorted(list_source_traces(), key=lambda trace: trace.created_at, reverse=True)
    return SkillStudioSourceTraceList(
        source_traces=traces,
        source_trace_count=len(traces),
        warnings=["Source Trace 仅记录草案来源 metadata，不包含案件原文。"],
    ).model_dump()
