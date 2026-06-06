from datetime import UTC, datetime

from personal_skill_studio.training_artifacts.experience_candidate_safety_engine import v731b_safety_flags
from personal_skill_studio.training_artifacts.schemas import ExperienceCandidate, ExperienceCandidateReview, ExperienceCandidateReviewRequest


STATUS_BY_ACTION = {
    "approve": "approved_for_skill_experience",
    "reject": "rejected",
    "request_changes": "changes_requested",
}


def review_candidate(candidate: ExperienceCandidate, request: ExperienceCandidateReviewRequest) -> ExperienceCandidateReview:
    review_status = STATUS_BY_ACTION.get(request.action, "changes_requested")
    approved = review_status == "approved_for_skill_experience" and candidate.redaction_status == "passed"
    candidate.review_status = review_status
    candidate.skill_experience_ready = approved
    candidate.candidate_status = "approved_redacted_experience" if approved else review_status
    candidate.audit_events.append(_event(candidate, request.action, review_status))
    return ExperienceCandidateReview(
        candidate_id=candidate.candidate_id,
        action=request.action,
        review_status=review_status,
        reviewer_id=request.reviewer_id,
        reviewer_note=request.reviewer_note,
        approved_for_skill_experience=approved,
        skill_experience_ready=approved,
        warnings=["Review approval only enables later Skill experience pool import; it does not publish a Skill."],
        **v731b_safety_flags(),
    )


def _event(candidate: ExperienceCandidate, action: str, review_status: str) -> dict[str, str | bool]:
    return {
        "event_id": f"{candidate.candidate_id}_audit_review_{action}",
        "actor": candidate.owner_user_id,
        "action": f"experience_candidate_review_{action}",
        "timestamp": datetime.now(UTC).isoformat(),
        "source_trace_id": candidate.source_trace_id,
        "material_boundary_decision": "manual_review_required_before_skill_experience",
        "ocr_job_id": candidate.source_ocr_job_id or "not_linked",
        "legal_retrieval_job_id": candidate.source_legal_retrieval_job_id or "not_linked",
        "experience_candidate_id": candidate.candidate_id,
        "redaction_status": candidate.redaction_status,
        "review_status": review_status,
        "metadata_only": True,
        "safety_decision": "approved_for_later_pool" if review_status == "approved_for_skill_experience" else "not_skill_ready",
    }
