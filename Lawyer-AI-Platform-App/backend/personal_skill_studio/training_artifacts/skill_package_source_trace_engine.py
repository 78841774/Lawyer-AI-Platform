from personal_skill_studio.training_artifacts.schemas import CodexSkillDraft, SkillPackageSourceTraceBundle
from personal_skill_studio.training_artifacts.skill_package_safety_engine import v731d_safety_flags


def build_source_trace_bundle(package_id: str, draft: CodexSkillDraft) -> SkillPackageSourceTraceBundle:
    trace_ids = sorted(set(draft.source_trace_ids))
    return SkillPackageSourceTraceBundle(
        source_trace_bundle_id=f"{package_id}_source_trace_bundle",
        package_id=package_id,
        source_draft_id=draft.draft_id,
        source_trace_ids=trace_ids,
        experience_ids=draft.created_from_experience_ids,
        trace_count=len(trace_ids),
        warnings=["Source trace bundle contains identifiers and metadata only."],
        **v731d_safety_flags(),
    )
