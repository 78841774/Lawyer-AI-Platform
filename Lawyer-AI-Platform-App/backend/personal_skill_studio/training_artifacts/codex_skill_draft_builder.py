from datetime import UTC, datetime
from uuid import uuid4

from personal_skill_studio.training_artifacts.schemas import (
    CodexSkillDraft,
    CodexSkillDraftAuditEvent,
    CodexSkillDraftBuildRequest,
    CodexSkillDraftBuildResponse,
    CodexSkillDraftSection,
    SkillExperiencePoolEntry,
)
from personal_skill_studio.training_artifacts.skill_experience_binding_engine import read_binding
from personal_skill_studio.training_artifacts.skill_experience_pool import read_entries_by_ids
from personal_skill_studio.training_artifacts.skill_experience_safety_engine import v731c_safety_flags


def build_draft(request: CodexSkillDraftBuildRequest) -> dict:
    entries = _resolve_entries(request)
    draft = _draft_from_entries(request, entries)
    return CodexSkillDraftBuildResponse(
        draft=draft,
        included_experience_count=len(entries),
        warnings=["Draft construction is metadata-only and awaits later pre-publish gate work."],
        **v731c_safety_flags(),
    ).model_dump()


def _resolve_entries(request: CodexSkillDraftBuildRequest) -> list[SkillExperiencePoolEntry]:
    if request.binding_id:
        binding = read_binding(request.binding_id)
        if binding:
            return read_entries_by_ids(binding.experience_ids)
    return read_entries_by_ids(request.experience_ids)


def _draft_from_entries(request: CodexSkillDraftBuildRequest, entries: list[SkillExperiencePoolEntry]) -> CodexSkillDraft:
    now = datetime.now(UTC).isoformat()
    draft_id = f"codex_skill_draft_v731c_{uuid4().hex[:10]}"
    source_trace_ids = sorted({entry.source_trace_id for entry in entries})
    source_candidate_ids = sorted({entry.source_candidate_id for entry in entries})
    experience_ids = [entry.experience_id for entry in entries]
    case_cause_scope = entries[0].case_cause if entries else "demo_safe_case_cause_scope"
    sections = _sections(draft_id, entries)
    return CodexSkillDraft(
        draft_id=draft_id,
        draft_name=request.draft_name,
        skill_purpose="Use approved lawyer experience metadata to guide controlled case-analysis drafting workflows.",
        trigger_conditions=["authorized owner-only review workflow", "approved experience metadata available"],
        input_requirements=["redacted experience pool entry", "source trace metadata", "manual reviewer confirmation"],
        workflow_steps=[
            "select approved experience metadata",
            "map patterns to draft sections",
            "run manual structure confirmation",
            "defer any publish gate to a later stage",
        ],
        experience_patterns=[entry.experience_type for entry in entries],
        case_cause_scope=case_cause_scope,
        evidence_handling_rules=["use evidence pattern metadata only", "preserve source-trace references"],
        legal_retrieval_usage_rules=["use retrieval candidates as reference metadata only"],
        redaction_rules=["keep all draft sections redacted and abstracted"],
        source_trace_rules=["each section must retain source trace ids"],
        audit_rules=["record import, binding, build, and review events"],
        manual_review_rules=["lawyer confirmation required before any future packaging stage"],
        prohibited_usage=[
            "do not publish Skill",
            "do not trigger real training",
            "do not generate final legal opinions",
            "do not create external delivery",
        ],
        quality_checklist=["experience approved", "redaction passed", "source trace present", "manual review pending"],
        sample_safe_prompts=["Generate a controlled draft outline from approved experience metadata."],
        sample_safe_outputs=["A redacted Skill draft section set requiring manual confirmation."],
        created_from_experience_ids=experience_ids,
        source_candidate_ids=source_candidate_ids,
        source_trace_ids=source_trace_ids,
        sections=sections,
        audit_events=[_event(draft_id, "codex_skill_draft_build", now)],
        created_at=now,
        updated_at=now,
        warnings=["Draft is not publishable and is not a formal training set."],
        **v731c_safety_flags(),
    )


def _sections(draft_id: str, entries: list[SkillExperiencePoolEntry]) -> list[CodexSkillDraftSection]:
    section_defs = [
        ("purpose", "Skill Purpose", "purpose metadata"),
        ("workflow", "Controlled Workflow", "workflow metadata"),
        ("patterns", "Experience Patterns", "pattern metadata"),
        ("safety", "Safety Boundary", "safety metadata"),
        ("review", "Manual Review Gate", "review metadata"),
    ]
    experience_ids = [entry.experience_id for entry in entries]
    source_trace_ids = sorted({entry.source_trace_id for entry in entries})
    return [
        CodexSkillDraftSection(
            section_id=f"{draft_id}_section_{section_type}",
            section_type=section_type,
            title=title,
            metadata_items=[label],
            source_experience_ids=experience_ids,
            source_trace_ids=source_trace_ids,
            **v731c_safety_flags(),
        )
        for section_type, title, label in section_defs
    ]


def _event(draft_id: str, action: str, timestamp: str) -> CodexSkillDraftAuditEvent:
    return CodexSkillDraftAuditEvent(
        event_id=f"{draft_id}_audit_{action}",
        draft_id=draft_id,
        action=action,
        timestamp=timestamp,
    )
