from datetime import UTC, datetime
from uuid import uuid4

from personal_skill_studio.training_artifacts.experience_candidate_safety_engine import v731b_safety_flags
from personal_skill_studio.training_artifacts.schemas import LegalRetrievalCandidate, LegalRetrievalJob, LegalRetrievalJobRequest


def build_legal_retrieval_job(request: LegalRetrievalJobRequest) -> LegalRetrievalJob:
    job_id = f"v731b_legal_retrieval_{uuid4().hex[:12]}"
    trace_id = f"{job_id}_source_trace"
    statute_candidates = [
        _candidate(job_id, "statute", "《民法典》合同编相关条款候选", "合同成立、履行、违约责任的规则候选摘要", trace_id),
        _candidate(job_id, "statute", "证据规则候选", "举证责任、证明标准、证据关联性的规则候选摘要", trace_id),
    ]
    similar_case_candidates = [
        _candidate(job_id, "similar_case", "类案裁判规则摘要候选", "同类争议中履行事实、证据链与抗辩路径的裁判规则摘要", trace_id),
        _candidate(job_id, "similar_case", "类案风险提示候选", "争点偏离、证据缺口与请求范围风险的摘要候选", trace_id),
    ]
    return LegalRetrievalJob(
        retrieval_job_id=job_id,
        source_ocr_job_id=request.source_ocr_job_id,
        query_label=request.query_label,
        retrieval_timestamp=datetime.now(UTC).isoformat(),
        statute_candidates=statute_candidates,
        similar_case_candidates=similar_case_candidates,
        source_trace_id=trace_id,
        audit_events=[
            _event(f"{job_id}_audit_create", "create_demo_safe_legal_retrieval_job", trace_id),
            _event(f"{job_id}_audit_candidates", "generate_demo_safe_legal_candidates", trace_id),
        ],
        warnings=["Legal retrieval candidates are demo-safe summaries; no provider call or key lookup is executed."],
        **v731b_safety_flags(),
    )


def _candidate(job_id: str, candidate_type: str, title: str, summary: str, trace_id: str) -> LegalRetrievalCandidate:
    return LegalRetrievalCandidate(
        candidate_id=f"{job_id}_{candidate_type}_{uuid4().hex[:8]}",
        candidate_type=candidate_type,
        title=title,
        summary=summary,
        source_trace_id=trace_id,
        **v731b_safety_flags(),
    )


def _event(event_id: str, action: str, source_trace_id: str) -> dict[str, str | bool]:
    return {
        "event_id": event_id,
        "actor": "owner_local_demo",
        "action": action,
        "timestamp": datetime.now(UTC).isoformat(),
        "source_trace_id": source_trace_id,
        "material_boundary_decision": "demo_safe_legal_retrieval_metadata",
        "metadata_only": True,
        "safety_decision": "no_provider_call",
    }
