from datetime import datetime, timezone
from uuid import uuid4

from fastapi import HTTPException

from personal_case_analysis.audit_engine import record_audit_event
from personal_case_analysis.review_queue import create_review_item
from personal_case_analysis.schemas import FactAnalysisDraft, FactAnalysisDraftList, FactDraftMockRequest
from personal_case_analysis.skill_loader import get_skill_baseline
from personal_case_analysis.source_trace_engine import create_source_trace
from personal_case_analysis.storage import FACT_DRAFTS_DIR, read_payload, read_payloads, write_payload


def _validate_request(request: FactDraftMockRequest) -> list[str]:
    blocked: list[str] = []
    for field in [
        "explicit_mock_confirmation",
        "explicit_no_training_data_confirmation",
        "explicit_no_raw_content_confirmation",
        "explicit_lawyer_review_confirmation",
    ]:
        if not getattr(request, field):
            blocked.append(f"{field} 必须为 true")
    if not request.case_id.strip():
        blocked.append("case_id 不能为空")
    return blocked


def create_mock_fact_draft(request: FactDraftMockRequest) -> dict:
    blocked = _validate_request(request)
    if blocked:
        raise HTTPException(status_code=400, detail={"message": "事实分析 draft 请求被阻断。", "blocked_reasons": blocked})
    baseline = get_skill_baseline(request.case_fact_extraction_skill_id)
    fact_draft_id = f"case_fact_draft_{uuid4().hex[:12]}"
    created_at = datetime.now(timezone.utc).isoformat()
    trace = create_source_trace(
        source_trace_id=f"case_analysis_source_trace_{fact_draft_id}_1",
        source_type="fact_analysis_metadata",
        source_label="事实分析 draft metadata",
        linked_object_type="fact_draft",
        linked_object_id=fact_draft_id,
        case_id=request.case_id,
        run_id=request.run_id,
        created_at=created_at,
    )
    source_trace_ids = list(dict.fromkeys([*request.source_trace_ids, trace.source_trace_id]))
    record = FactAnalysisDraft(
        fact_draft_id=fact_draft_id,
        run_id=request.run_id,
        case_id=request.case_id,
        source_skill_id=baseline.source_skill_id,
        source_package_id=baseline.source_package_id,
        fact_summary_draft="本阶段仅生成未结案件事实摘要 draft metadata：需律师结合材料原文复核后使用。",
        evidence_mapping_draft=[
            {"fact": "合同关系 metadata 待复核", "evidence": "material metadata / source trace", "review_status": "pending_lawyer_review"},
            {"fact": "履行与付款节点 metadata 待复核", "evidence": "document parse metadata", "review_status": "pending_lawyer_review"},
        ],
        timeline_draft=[
            {"node": "合同形成", "status": "metadata_placeholder"},
            {"node": "履行争议", "status": "metadata_placeholder"},
            {"node": "律师复核", "status": "required"},
        ],
        disputed_facts_draft=["付款节点是否明确", "交付/验收事实是否完整"],
        missing_facts_draft=["缺少律师确认后的关键证据链", "缺少来源追踪完整性确认"],
        confidence_metadata={
            "overall_confidence": 62,
            "low_confidence": True,
            "reason": "metadata-only draft; raw material not read",
            "baseline_detected": baseline.baseline_detected,
        },
        source_trace_ids=source_trace_ids,
        warnings=[
            "事实分析 draft 不读取 raw full content。",
            "OCR 原文不会自动进入 AI prompt。",
            "该结果不构成最终事实认定，也不产生训练数据。",
        ],
        created_at=created_at,
    )
    write_payload(FACT_DRAFTS_DIR, fact_draft_id, record.model_dump())
    review_item = create_review_item(
        linked_object_type="fact_draft",
        linked_object_id=fact_draft_id,
        case_id=request.case_id,
        review_focus=["事实摘要可读性", "证据映射可复核性", "缺失事实提示价值", "来源追踪完整性"],
        risk_flags=["low_confidence_metadata_only"],
        created_at=created_at,
    )
    record_audit_event(action="fact_draft_mock_created", actor="system", object_type="fact_draft", object_id=fact_draft_id, timestamp=created_at)
    payload = record.model_dump()
    payload["review_item_ids"] = [review_item.review_item_id]
    return payload


def get_fact_draft(fact_draft_id: str) -> FactAnalysisDraft | None:
    payload = read_payload(FACT_DRAFTS_DIR, fact_draft_id)
    return FactAnalysisDraft(**payload) if payload else None


def list_fact_drafts() -> list[FactAnalysisDraft]:
    return [FactAnalysisDraft(**payload) for payload in read_payloads(FACT_DRAFTS_DIR)]


def build_fact_draft_list() -> dict:
    drafts = sorted(list_fact_drafts(), key=lambda draft: draft.created_at, reverse=True)
    return FactAnalysisDraftList(
        fact_drafts=drafts,
        draft_count=len(drafts),
        warnings=["事实分析列表仅包含 draft metadata，不包含 raw material 或训练样本。"],
    ).model_dump()
