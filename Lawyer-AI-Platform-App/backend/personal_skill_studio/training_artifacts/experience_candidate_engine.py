from datetime import UTC, datetime
from uuid import uuid4

from personal_skill_studio.training_artifacts.experience_candidate_safety_engine import v731b_safety_flags
from personal_skill_studio.training_artifacts.schemas import ExperienceCandidate, ExperienceCandidateBuildRequest


CANDIDATE_TYPES = [
    ("fact_pattern", "事实模式"),
    ("issue_pattern", "争点模式"),
    ("evidence_pattern", "证据模式"),
    ("rule_application_pattern", "规则适用模式"),
    ("argument_strategy_pattern", "论证策略模式"),
    ("drafting_pattern", "文书起草模式"),
    ("risk_warning_pattern", "风险提示模式"),
    ("review_checklist_pattern", "复核清单模式"),
]


def build_experience_candidates(request: ExperienceCandidateBuildRequest) -> list[ExperienceCandidate]:
    return [_candidate(request, candidate_type, label) for candidate_type, label in CANDIDATE_TYPES]


def _candidate(request: ExperienceCandidateBuildRequest, candidate_type: str, label: str) -> ExperienceCandidate:
    candidate_id = f"v731b_exp_candidate_{candidate_type}_{uuid4().hex[:8]}"
    trace_id = f"{candidate_id}_source_trace"
    return ExperienceCandidate(
        candidate_id=candidate_id,
        candidate_type=candidate_type,
        owner_user_id=request.owner_user_id,
        source_ocr_job_id=request.source_ocr_job_id,
        source_legal_retrieval_job_id=request.source_legal_retrieval_job_id,
        pattern_label=label,
        structured_summary=[
            f"{label}结构化摘要",
            "来源于 demo-safe OCR / document parse summary",
            "结合 demo-safe legal retrieval candidates",
            "等待脱敏、抽象化与律师人工复核",
        ],
        source_trace_id=trace_id,
        audit_events=[
            _event(f"{candidate_id}_audit_build", "experience_candidate_build", trace_id, request.source_ocr_job_id, request.source_legal_retrieval_job_id),
        ],
        warnings=["Candidate is not Skill-ready until redacted and approved for Skill experience."],
        **v731b_safety_flags(),
    )


def _event(
    event_id: str,
    action: str,
    source_trace_id: str,
    ocr_job_id: str | None,
    legal_retrieval_job_id: str | None,
) -> dict[str, str | bool]:
    return {
        "event_id": event_id,
        "actor": "owner_local_demo",
        "action": action,
        "timestamp": datetime.now(UTC).isoformat(),
        "source_trace_id": source_trace_id,
        "material_boundary_decision": "redacted_experience_required",
        "ocr_job_id": ocr_job_id or "not_linked",
        "legal_retrieval_job_id": legal_retrieval_job_id or "not_linked",
        "experience_candidate_id": event_id.replace("_audit_build", ""),
        "redaction_status": "requires_redaction",
        "review_status": "pending_review",
        "metadata_only": True,
        "safety_decision": "not_skill_ready",
    }
