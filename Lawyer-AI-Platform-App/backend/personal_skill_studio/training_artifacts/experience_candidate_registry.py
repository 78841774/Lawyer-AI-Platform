from personal_skill_studio.training_artifacts.experience_candidate_engine import build_experience_candidates
from personal_skill_studio.training_artifacts.experience_candidate_redaction_engine import redact_candidate
from personal_skill_studio.training_artifacts.experience_candidate_review_queue import review_candidate
from personal_skill_studio.training_artifacts.experience_candidate_safety_engine import v731b_safety_flags
from personal_skill_studio.training_artifacts.schemas import (
    ExperienceCandidate,
    ExperienceCandidateAudit,
    ExperienceCandidateBuildRequest,
    ExperienceCandidateList,
    ExperienceCandidateReviewRequest,
)
from personal_skill_studio.training_artifacts.storage import EXPERIENCE_CANDIDATES_DIR, read_payload, read_payloads, write_payload


def build_candidates(request: ExperienceCandidateBuildRequest) -> dict:
    candidates = build_experience_candidates(request)
    for candidate in candidates:
        write_payload(EXPERIENCE_CANDIDATES_DIR, candidate.candidate_id, candidate.model_dump())
    return ExperienceCandidateList(
        candidates=candidates,
        candidate_count=len(candidates),
        approved_for_skill_experience_count=0,
        warnings=["Candidates require redaction and manual review before later Skill experience pool import."],
        **v731b_safety_flags(),
    ).model_dump()


def list_candidates() -> dict:
    candidates = _all_candidates()
    return ExperienceCandidateList(
        candidates=candidates,
        candidate_count=len(candidates),
        approved_for_skill_experience_count=sum(1 for candidate in candidates if candidate.review_status == "approved_for_skill_experience"),
        warnings=["Only approved_for_skill_experience candidates may be used by v7.31c."],
        **v731b_safety_flags(),
    ).model_dump()


def get_candidate(candidate_id: str) -> dict | None:
    candidate = _read_candidate(candidate_id)
    return candidate.model_dump() if candidate else None


def redact_experience_candidate(candidate_id: str) -> dict | None:
    candidate = _read_candidate(candidate_id)
    if candidate is None:
        return None
    redaction = redact_candidate(candidate)
    write_payload(EXPERIENCE_CANDIDATES_DIR, candidate.candidate_id, candidate.model_dump())
    return redaction.model_dump()


def review_experience_candidate(candidate_id: str, request: ExperienceCandidateReviewRequest) -> dict | None:
    candidate = _read_candidate(candidate_id)
    if candidate is None:
        return None
    review = review_candidate(candidate, request)
    write_payload(EXPERIENCE_CANDIDATES_DIR, candidate.candidate_id, candidate.model_dump())
    return {"candidate": candidate.model_dump(), "review": review.model_dump(), **v731b_safety_flags()}


def get_candidate_audit(candidate_id: str) -> dict | None:
    candidate = _read_candidate(candidate_id)
    if candidate is None:
        return None
    return ExperienceCandidateAudit(
        candidate_id=candidate_id,
        events=candidate.audit_events,
        event_count=len(candidate.audit_events),
        warnings=["Audit is metadata-only and records no source material text."],
        **v731b_safety_flags(),
    ).model_dump()


def _read_candidate(candidate_id: str) -> ExperienceCandidate | None:
    payload = read_payload(EXPERIENCE_CANDIDATES_DIR, candidate_id)
    if payload:
        return ExperienceCandidate(**payload)
    for payload in read_payloads(EXPERIENCE_CANDIDATES_DIR):
        candidate = ExperienceCandidate(**payload)
        if candidate.candidate_id == candidate_id:
            return candidate
    return None


def _all_candidates() -> list[ExperienceCandidate]:
    return [ExperienceCandidate(**payload) for payload in read_payloads(EXPERIENCE_CANDIDATES_DIR)]
