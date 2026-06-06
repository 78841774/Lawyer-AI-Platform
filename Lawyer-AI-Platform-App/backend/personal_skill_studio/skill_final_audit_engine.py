from personal_skill_studio.audit_engine import build_audit_timeline
from personal_skill_studio.schemas import SkillFinalAuditTimeline, SkillStudioAuditEvent
from personal_skill_studio.skill_final_draft_engine import get_skill_final_draft


def build_skill_final_audit(skill_id: str) -> SkillFinalAuditTimeline | None:
    draft = get_skill_final_draft(skill_id)
    if draft is None:
        return None
    timeline = build_audit_timeline()
    events = [
        SkillStudioAuditEvent(**event)
        for event in timeline.get("events", [])
        if event.get("object_id") in {skill_id, draft.source_skill_id} or event.get("object_type") in {"skill_candidate", "evaluation", "skill_final_draft"}
    ]
    return SkillFinalAuditTimeline(
        skill_id=skill_id,
        events=events,
        event_count=len(events),
        baseline_discovered=draft.baseline_discovered,
        baseline_complete=draft.baseline_complete,
        warnings=["Audit timeline is metadata-only and excludes raw content, secrets, and local paths."],
    )
