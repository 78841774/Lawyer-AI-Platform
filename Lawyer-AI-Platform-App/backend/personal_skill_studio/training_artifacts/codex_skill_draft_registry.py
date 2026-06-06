from datetime import UTC, datetime

from personal_skill_studio.training_artifacts.codex_skill_draft_builder import build_draft
from personal_skill_studio.training_artifacts.schemas import (
    CodexSkillDraft,
    CodexSkillDraftAudit,
    CodexSkillDraftAuditEvent,
    CodexSkillDraftBuildRequest,
    CodexSkillDraftList,
    CodexSkillDraftReviewRequest,
)
from personal_skill_studio.training_artifacts.skill_experience_safety_engine import v731c_safety_flags
from personal_skill_studio.training_artifacts.storage import CODEX_SKILL_DRAFTS_DIR, read_payload, read_payloads, write_payload


def create_draft(request: CodexSkillDraftBuildRequest) -> dict:
    response = build_draft(request)
    draft = response["draft"]
    write_payload(CODEX_SKILL_DRAFTS_DIR, draft["draft_id"], draft)
    return response


def list_drafts() -> dict:
    drafts = _all_drafts()
    return CodexSkillDraftList(
        drafts=drafts,
        draft_count=len(drafts),
        warnings=["Skill drafts require manual confirmation and are not publishable in v7.31c."],
        **v731c_safety_flags(),
    ).model_dump()


def get_draft(draft_id: str) -> dict | None:
    draft = _read_draft(draft_id)
    return draft.model_dump() if draft else None


def review_draft(draft_id: str, request: CodexSkillDraftReviewRequest) -> dict | None:
    draft = _read_draft(draft_id)
    if draft is None:
        return None
    now = datetime.now(UTC).isoformat()
    status_by_action = {
        "approve_draft_structure": "structure_approved_requires_pre_publish_gate",
        "request_changes": "changes_requested",
        "reject_draft": "rejected",
    }
    draft.confirmation_status = status_by_action.get(request.action, "changes_requested")
    draft.draft_status = draft.confirmation_status
    draft.publish_status = "not_publishable"
    draft.training_status = "not_training_ready"
    draft.updated_at = now
    draft.audit_events.append(
        CodexSkillDraftAuditEvent(
            event_id=f"{draft_id}_audit_review_{request.action}",
            draft_id=draft_id,
            action=f"codex_skill_draft_review_{request.action}",
            timestamp=now,
        )
    )
    write_payload(CODEX_SKILL_DRAFTS_DIR, draft.draft_id, draft.model_dump())
    return {
        "draft": draft.model_dump(),
        "review": {
            "draft_id": draft_id,
            "action": request.action,
            "confirmation_status": draft.confirmation_status,
            "reviewer_id": request.reviewer_id,
            "reviewer_note": request.reviewer_note,
            "skill_published": False,
            "real_training_triggered": False,
            "warnings": ["Manual confirmation does not publish a Skill or trigger real training."],
            **v731c_safety_flags(),
        },
        **v731c_safety_flags(),
    }


def get_draft_audit(draft_id: str) -> dict | None:
    draft = _read_draft(draft_id)
    if draft is None:
        return None
    return CodexSkillDraftAudit(
        draft_id=draft_id,
        events=draft.audit_events,
        event_count=len(draft.audit_events),
        warnings=["Audit records draft metadata actions only."],
        **v731c_safety_flags(),
    ).model_dump()


def _read_draft(draft_id: str) -> CodexSkillDraft | None:
    payload = read_payload(CODEX_SKILL_DRAFTS_DIR, draft_id)
    if payload:
        return CodexSkillDraft(**payload)
    return None


def _all_drafts() -> list[CodexSkillDraft]:
    return [CodexSkillDraft(**payload) for payload in read_payloads(CODEX_SKILL_DRAFTS_DIR)]
