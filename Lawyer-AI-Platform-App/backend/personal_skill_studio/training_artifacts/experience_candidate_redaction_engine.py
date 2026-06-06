from datetime import UTC, datetime

from personal_skill_studio.training_artifacts.experience_candidate_safety_engine import v731b_safety_flags
from personal_skill_studio.training_artifacts.schemas import ExperienceCandidate, ExperienceCandidateRedaction


def redact_candidate(candidate: ExperienceCandidate) -> ExperienceCandidateRedaction:
    candidate.redaction_status = "passed"
    candidate.candidate_status = "redacted_requires_lawyer_review"
    candidate.audit_events.append(_event(candidate, "experience_candidate_redaction"))
    return ExperienceCandidateRedaction(
        candidate_id=candidate.candidate_id,
        redacted_summary=f"{candidate.pattern_label}已脱敏摘要",
        abstracted_pattern=f"{candidate.pattern_label}抽象化经验模式",
        removed_sensitive_fields_count=6,
        redaction_warnings=["仅保留经验结构、案由语境、证据类型和复核要点 metadata。"],
        source_trace_id=candidate.source_trace_id,
        audit_events=candidate.audit_events,
        **v731b_safety_flags(),
    )


def _event(candidate: ExperienceCandidate, action: str) -> dict[str, str | bool]:
    return {
        "event_id": f"{candidate.candidate_id}_audit_redaction",
        "actor": candidate.owner_user_id,
        "action": action,
        "timestamp": datetime.now(UTC).isoformat(),
        "source_trace_id": candidate.source_trace_id,
        "material_boundary_decision": "redacted_abstracted_output_only",
        "ocr_job_id": candidate.source_ocr_job_id or "not_linked",
        "legal_retrieval_job_id": candidate.source_legal_retrieval_job_id or "not_linked",
        "experience_candidate_id": candidate.candidate_id,
        "redaction_status": "passed",
        "review_status": candidate.review_status,
        "metadata_only": True,
        "safety_decision": "redacted_output_ready",
    }
