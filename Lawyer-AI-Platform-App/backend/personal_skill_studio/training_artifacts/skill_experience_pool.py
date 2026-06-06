from datetime import UTC, datetime
from uuid import uuid4

from personal_skill_studio.training_artifacts.schemas import (
    ExperienceCandidate,
    SkillExperienceImportRequest,
    SkillExperienceImportResponse,
    SkillExperiencePoolEntry,
    SkillExperiencePoolList,
    SkillExperiencePoolStatus,
)
from personal_skill_studio.training_artifacts.skill_experience_safety_engine import v731c_safety_flags
from personal_skill_studio.training_artifacts.storage import (
    EXPERIENCE_CANDIDATES_DIR,
    SKILL_EXPERIENCE_POOL_DIR,
    read_payload,
    read_payloads,
    write_payload,
)


def pool_status() -> dict:
    entries = _all_entries()
    return SkillExperiencePoolStatus(
        experience_count=len(entries),
        unbound_experience_count=sum(1 for entry in entries if entry.skill_binding_status == "unbound"),
        warnings=["Only approved v7.31b experience candidates may enter the v7.31c Skill Experience Pool."],
        **v731c_safety_flags(),
    ).model_dump()


def import_approved_experience(request: SkillExperienceImportRequest) -> dict:
    candidate_payloads = _candidate_payloads(request.source_candidate_ids)
    imported_entries: list[SkillExperiencePoolEntry] = []
    rejected_candidate_ids: list[str] = []

    for payload in candidate_payloads:
        candidate = ExperienceCandidate(**payload)
        if not _eligible(candidate):
            rejected_candidate_ids.append(candidate.candidate_id)
            continue
        existing = _find_by_candidate(candidate.candidate_id)
        entry = existing or _entry_from_candidate(candidate)
        write_payload(SKILL_EXPERIENCE_POOL_DIR, entry.experience_id, entry.model_dump())
        imported_entries.append(entry)

    return SkillExperienceImportResponse(
        imported_experiences=imported_entries,
        imported_count=len(imported_entries),
        rejected_count=len(rejected_candidate_ids),
        rejected_candidate_ids=rejected_candidate_ids,
        warnings=["Rejected candidates are left unchanged and are not imported into the Skill Experience Pool."],
        **v731c_safety_flags(),
    ).model_dump()


def list_pool_entries() -> dict:
    entries = _all_entries()
    return SkillExperiencePoolList(
        experiences=entries,
        experience_count=len(entries),
        unbound_experience_count=sum(1 for entry in entries if entry.skill_binding_status == "unbound"),
        warnings=["Experience entries are redacted and abstracted metadata only."],
        **v731c_safety_flags(),
    ).model_dump()


def get_pool_entry(experience_id: str) -> dict | None:
    entry = _read_entry(experience_id)
    return entry.model_dump() if entry else None


def mark_entries_bound(experience_ids: list[str]) -> None:
    now = _now()
    for experience_id in experience_ids:
        entry = _read_entry(experience_id)
        if entry is None:
            continue
        entry.skill_binding_status = "bound_to_draft_target"
        entry.updated_at = now
        write_payload(SKILL_EXPERIENCE_POOL_DIR, entry.experience_id, entry.model_dump())


def read_entries_by_ids(experience_ids: list[str]) -> list[SkillExperiencePoolEntry]:
    ids = experience_ids or [entry.experience_id for entry in _all_entries()]
    entries: list[SkillExperiencePoolEntry] = []
    for experience_id in ids:
        entry = _read_entry(experience_id)
        if entry:
            entries.append(entry)
    return entries


def _candidate_payloads(candidate_ids: list[str]) -> list[dict]:
    if not candidate_ids:
        return read_payloads(EXPERIENCE_CANDIDATES_DIR)
    payloads: list[dict] = []
    for candidate_id in candidate_ids:
        payload = read_payload(EXPERIENCE_CANDIDATES_DIR, candidate_id)
        if payload:
            payloads.append(payload)
    return payloads


def _eligible(candidate: ExperienceCandidate) -> bool:
    return (
        candidate.review_status == "approved_for_skill_experience"
        and candidate.redaction_status == "passed"
        and candidate.skill_experience_ready
        and bool(candidate.source_trace_id)
        and bool(candidate.audit_events)
        and not candidate.provider_call_executed
    )


def _entry_from_candidate(candidate: ExperienceCandidate) -> SkillExperiencePoolEntry:
    now = _now()
    experience_id = f"skill_exp_v731c_{candidate.candidate_type}_{uuid4().hex[:10]}"
    pattern = candidate.pattern_label
    return SkillExperiencePoolEntry(
        experience_id=experience_id,
        source_candidate_id=candidate.candidate_id,
        experience_type=candidate.candidate_type,
        fact_pattern=f"{pattern} fact pattern metadata",
        issue_pattern=f"{pattern} issue pattern metadata",
        evidence_pattern=f"{pattern} evidence pattern metadata",
        rule_application_pattern=f"{pattern} rule application metadata",
        argument_strategy_pattern=f"{pattern} argument strategy metadata",
        drafting_pattern=f"{pattern} drafting pattern metadata",
        risk_warning_pattern=f"{pattern} risk warning metadata",
        review_checklist_pattern=f"{pattern} review checklist metadata",
        redaction_summary="redacted and reviewer-approved experience metadata",
        abstraction_summary="abstracted lawyer work-product experience structure",
        source_trace_id=candidate.source_trace_id,
        audit_id=f"{experience_id}_audit_import",
        created_at=now,
        updated_at=now,
        warnings=["Imported only after v7.31b redaction and manual review approval."],
        **v731c_safety_flags(),
    )


def _find_by_candidate(candidate_id: str) -> SkillExperiencePoolEntry | None:
    return next((entry for entry in _all_entries() if entry.source_candidate_id == candidate_id), None)


def _read_entry(experience_id: str) -> SkillExperiencePoolEntry | None:
    payload = read_payload(SKILL_EXPERIENCE_POOL_DIR, experience_id)
    if payload:
        return SkillExperiencePoolEntry(**payload)
    return None


def _all_entries() -> list[SkillExperiencePoolEntry]:
    return [SkillExperiencePoolEntry(**payload) for payload in read_payloads(SKILL_EXPERIENCE_POOL_DIR)]


def _now() -> str:
    return datetime.now(UTC).isoformat()
