from datetime import datetime, timezone
from uuid import uuid4

from fastapi import HTTPException

from personal_case_analysis.audit_engine import record_audit_event
from personal_case_analysis.fact_analysis_engine import get_fact_draft
from personal_case_analysis.review_queue import create_review_item
from personal_case_analysis.schemas import LegalAnalysisDraft, LegalAnalysisDraftList, LegalDraftMockRequest
from personal_case_analysis.skill_loader import get_skill_baseline
from personal_case_analysis.source_trace_engine import create_source_trace
from personal_case_analysis.storage import LEGAL_DRAFTS_DIR, read_payload, read_payloads, write_payload


def _validate_request(request: LegalDraftMockRequest) -> list[str]:
    blocked: list[str] = []
    for field in [
        "explicit_mock_confirmation",
        "explicit_no_training_data_confirmation",
        "explicit_no_raw_content_confirmation",
        "explicit_lawyer_review_confirmation",
        "explicit_no_final_opinion_confirmation",
    ]:
        if not getattr(request, field):
            blocked.append(f"{field} 必须为 true")
    if not request.case_id.strip():
        blocked.append("case_id 不能为空")
    if request.fact_draft_id and get_fact_draft(request.fact_draft_id) is None:
        blocked.append("fact_draft_id 不存在")
    return blocked


def create_mock_legal_draft(request: LegalDraftMockRequest) -> dict:
    blocked = _validate_request(request)
    if blocked:
        raise HTTPException(status_code=400, detail={"message": "法律分析 draft 请求被阻断。", "blocked_reasons": blocked})
    baseline = get_skill_baseline(request.case_legal_analysis_skill_id)
    legal_draft_id = f"case_legal_draft_{uuid4().hex[:12]}"
    created_at = datetime.now(timezone.utc).isoformat()
    trace = create_source_trace(
        source_trace_id=f"case_analysis_source_trace_{legal_draft_id}_1",
        source_type="legal_analysis_metadata",
        source_label="法律分析 draft metadata",
        linked_object_type="legal_draft",
        linked_object_id=legal_draft_id,
        case_id=request.case_id,
        created_at=created_at,
    )
    source_trace_ids = list(dict.fromkeys([*request.source_trace_ids, trace.source_trace_id]))
    record = LegalAnalysisDraft(
        legal_draft_id=legal_draft_id,
        fact_draft_id=request.fact_draft_id,
        case_id=request.case_id,
        source_skill_id=baseline.source_skill_id,
        source_package_id=baseline.source_package_id,
        legal_relationship_draft="本阶段仅生成法律关系 draft metadata：需律师结合事实、法条和类案来源复核。",
        issue_spotting_draft=["合同成立及履行争议", "违约责任构成", "损失及举证责任"],
        claim_basis_draft=["请求权基础候选 metadata，需法律检索和律师确认", "利息/违约金调整风险待复核"],
        defense_path_draft=["合同履行抗辩路径 metadata", "证据不足或损失扩大抗辩 metadata"],
        burden_of_proof_draft=["主张合同关系和违约事实的一方承担初步举证责任", "损失金额与因果关系需补充证据链"],
        legal_search_questions_draft=["检索同类买卖合同逾期付款裁判规则", "检索违约金调整相关裁判观点"],
        risk_flags_draft=["事实 draft 尚未律师确认", "引用候选不是最终引用", "不构成最终法律意见"],
        next_action_checklist_draft=["律师复核事实 draft", "补齐来源追踪", "发起法律检索 metadata 复核", "标记低置信度项"],
        source_trace_ids=source_trace_ids,
        warnings=[
            "法律分析 Skill 不直接读取 raw material。",
            "法律分析 draft 不生成最终法律意见或最终报告。",
            "本结果不会写入训练集或自动更新 Skill。",
        ],
        created_at=created_at,
    )
    write_payload(LEGAL_DRAFTS_DIR, legal_draft_id, record.model_dump())
    review_item = create_review_item(
        linked_object_type="legal_draft",
        linked_object_id=legal_draft_id,
        case_id=request.case_id,
        review_focus=["法律关系 draft 质量", "争议焦点完整性", "请求权基础覆盖", "风险提示价值"],
        risk_flags=["final_opinion_forbidden", "citation_not_finalized"],
        created_at=created_at,
    )
    record_audit_event(action="legal_draft_mock_created", actor="system", object_type="legal_draft", object_id=legal_draft_id, timestamp=created_at)
    payload = record.model_dump()
    payload["review_item_ids"] = [review_item.review_item_id]
    return payload


def get_legal_draft(legal_draft_id: str) -> LegalAnalysisDraft | None:
    payload = read_payload(LEGAL_DRAFTS_DIR, legal_draft_id)
    return LegalAnalysisDraft(**payload) if payload else None


def list_legal_drafts() -> list[LegalAnalysisDraft]:
    return [LegalAnalysisDraft(**payload) for payload in read_payloads(LEGAL_DRAFTS_DIR)]


def build_legal_draft_list() -> dict:
    drafts = sorted(list_legal_drafts(), key=lambda draft: draft.created_at, reverse=True)
    return LegalAnalysisDraftList(
        legal_drafts=drafts,
        draft_count=len(drafts),
        warnings=["法律分析列表仅包含 draft metadata，不包含最终法律意见或最终报告。"],
    ).model_dump()
