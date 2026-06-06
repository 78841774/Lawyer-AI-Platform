from personal_skill_studio.schemas import SkillFinalSourceTraceList
from personal_skill_studio.source_trace_engine import list_source_traces
from personal_skill_studio.skill_final_draft_engine import get_skill_final_draft


def build_skill_final_source_traces(skill_id: str) -> SkillFinalSourceTraceList | None:
    draft = get_skill_final_draft(skill_id)
    if draft is None:
        return None
    traces = [
        trace
        for trace in list_source_traces()
        if trace.skill_candidate_id in {skill_id, draft.source_skill_id} or trace.linked_object_id in {skill_id, draft.source_skill_id}
    ]
    return SkillFinalSourceTraceList(
        skill_id=skill_id,
        source_traces=traces,
        source_trace_count=len(traces),
        baseline_discovered=draft.baseline_discovered,
        baseline_complete=draft.baseline_complete,
        warnings=["Source traces are metadata-only; raw content is excluded."],
    )
