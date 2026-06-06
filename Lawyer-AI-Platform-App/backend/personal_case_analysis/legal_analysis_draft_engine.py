from datetime import datetime, timezone
from uuid import uuid4

from fastapi import HTTPException

from personal_case_analysis.audit_engine import record_audit_event
from personal_case_analysis.fact_analysis_engine import get_fact_draft
from personal_case_analysis.review_queue import create_review_item
from personal_case_analysis.schemas import (
    LegalAnalysisDraft,
    LegalAnalysisDraftList,
    LegalDraftGateReport,
    LegalDraftMockRequest,
    LegalDraftQualityReport,
    LegalDraftReviewConfirmation,
    LegalDraftReviewConfirmRequest,
    LegalDraftVersionList,
    LegalDraftVersionMockRequest,
    LegalDraftVersionRecord,
)
from personal_case_analysis.skill_loader import get_skill_baseline
from personal_case_analysis.source_trace_engine import create_source_trace
from personal_case_analysis.storage import (
    LEGAL_DRAFTS_DIR,
    LEGAL_DRAFT_VERSIONS_DIR,
    read_payload,
    read_payloads,
    write_payload,
)


def _now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


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


def create_legal_analysis_draft(request: LegalDraftMockRequest) -> dict:
    blocked = _validate_request(request)
    if blocked:
        raise HTTPException(status_code=400, detail={"message": "法律分析 draft 请求被阻断。", "blocked_reasons": blocked})
    baseline = get_skill_baseline(request.case_legal_analysis_skill_id)
    legal_draft_id = f"legal_analysis_draft_{uuid4().hex[:12]}"
    created_at = _now()
    trace = create_source_trace(
        source_trace_id=f"case_analysis_source_trace_{legal_draft_id}_1",
        source_type="legal_analysis_draft_metadata",
        source_label="法律分析草稿 metadata 来源追踪",
        linked_object_type="legal_analysis_draft",
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
        legal_analysis_summary_draft="法律分析摘要 draft metadata：基于已确认事实输入和来源追踪，形成供律师复核的争议、请求权、抗辩和风险框架。",
        legal_relationship_draft="法律关系 draft metadata：初步围绕合同关系、履行义务、违约责任和损失举证展开，需律师复核。",
        legal_reasoning_draft=[
            "先核对事实输入是否已由用户本人确认，再判断法律关系和争议焦点。",
            "请求权基础、抗辩路径和举证责任仅作为草稿框架，不是最终法律结论。",
            "法律检索与企业信息候选来源需进入 Source Trace 和律师复核后才能进一步使用。",
        ],
        dispute_focus_draft=["合同履行范围", "付款节点与违约责任", "损失范围与因果关系", "通知义务和证据链完整性"],
        issue_spotting_draft=["合同成立及履行争议", "违约责任构成", "损失及举证责任"],
        claim_basis_draft=["请求权基础候选 metadata，需法律检索和律师确认", "利息/违约金调整风险待复核"],
        defense_path_draft=["合同履行抗辩路径 metadata", "证据不足或损失扩大抗辩 metadata"],
        burden_of_proof_draft=["主张合同关系和违约事实的一方承担初步举证责任", "损失金额与因果关系需补充证据链"],
        legal_search_questions_draft=["检索同类合同逾期履行裁判规则", "检索违约金调整相关裁判观点"],
        risk_flags_draft=["事实输入需确认", "引用候选不是最终引用", "不构成最终法律意见"],
        next_action_checklist_draft=["律师复核事实输入", "补齐来源追踪", "复核法律检索候选", "标记低置信度项", "必要时请求用户补充事实"],
        source_trace_ids=source_trace_ids,
        warnings=[
            "法律分析草稿仅为 metadata draft。",
            "不生成最终法律意见，不生成最终报告。",
            "不会写入训练集、更新 Skill、发布 Skill 或触发外部交付。",
        ],
        created_at=created_at,
    )
    write_payload(LEGAL_DRAFTS_DIR, legal_draft_id, record.model_dump())
    review_item = create_review_item(
        linked_object_type="legal_analysis_draft",
        linked_object_id=legal_draft_id,
        case_id=request.case_id,
        review_focus=["法律分析摘要", "争议焦点", "请求权基础", "抗辩路径", "风险提示", "下一步清单"],
        risk_flags=["final_opinion_forbidden", "final_report_forbidden", "source_trace_required"],
        created_at=created_at,
    )
    create_legal_draft_version(
        legal_draft_id,
        LegalDraftVersionMockRequest(
            created_from="ai_draft",
            change_summary="初始 AI 法律分析草稿 metadata",
            explicit_owner_confirmation=True,
            explicit_no_final_opinion_confirmation=True,
            explicit_no_training_data_confirmation=True,
        ),
    )
    record_audit_event(action="legal_analysis_draft_mock_created", actor="system", object_type="legal_analysis_draft", object_id=legal_draft_id, timestamp=created_at)
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


def create_legal_draft_version(legal_draft_id: str, request: LegalDraftVersionMockRequest) -> LegalDraftVersionRecord | None:
    if get_legal_draft(legal_draft_id) is None:
        return None
    existing = [record for record in list_legal_draft_versions_raw(legal_draft_id)]
    version = LegalDraftVersionRecord(
        version_id=f"legal_draft_version_{uuid4().hex[:12]}",
        legal_draft_id=legal_draft_id,
        version_number=len(existing) + 1,
        created_from=request.created_from,
        change_summary=request.change_summary,
        owner_confirmed=bool(request.explicit_owner_confirmation),
        review_ready=bool(request.explicit_owner_confirmation and request.explicit_no_final_opinion_confirmation),
        created_at=_now(),
        warnings=["版本记录仅为法律分析草稿 metadata，不生成最终法律意见或报告。"],
    )
    write_payload(LEGAL_DRAFT_VERSIONS_DIR, version.version_id, version.model_dump())
    return version


def list_legal_draft_versions_raw(legal_draft_id: str) -> list[LegalDraftVersionRecord]:
    return [
        LegalDraftVersionRecord(**payload)
        for payload in read_payloads(LEGAL_DRAFT_VERSIONS_DIR)
        if payload.get("legal_draft_id") == legal_draft_id
    ]


def list_legal_draft_versions(legal_draft_id: str) -> LegalDraftVersionList | None:
    if get_legal_draft(legal_draft_id) is None:
        return None
    versions = sorted(list_legal_draft_versions_raw(legal_draft_id), key=lambda version: version.version_number)
    return LegalDraftVersionList(
        legal_draft_id=legal_draft_id,
        versions=versions,
        version_count=len(versions),
        warnings=["版本历史仅用于用户本人和律师复核草稿变化，不写训练集。"],
    )


def build_legal_draft_quality(legal_draft_id: str) -> LegalDraftQualityReport | None:
    if get_legal_draft(legal_draft_id) is None:
        return None
    return LegalDraftQualityReport(
        legal_draft_id=legal_draft_id,
        overall_score=81,
        dimension_scores={
            "legal_summary_clarity": 82,
            "dispute_focus_coverage": 80,
            "claim_basis_coverage": 78,
            "defense_path_coverage": 76,
            "risk_note_value": 84,
            "source_trace_readiness": 79,
            "next_step_actionability": 86,
        },
        optimization_suggestions=[
            "建议补齐低置信度事实后再强化请求权基础。",
            "建议将法律检索候选补入 Source Trace 后再进入律师复核。",
            "建议区分原告诉请路径与被告抗辩路径，避免草稿被误读为最终意见。",
        ],
        warnings=["质量评分仅为参考 metadata，不代表法律正确性保证。"],
    )


def build_legal_draft_gate(legal_draft_id: str) -> LegalDraftGateReport | None:
    if get_legal_draft(legal_draft_id) is None:
        return None
    return LegalDraftGateReport(
        gate_id=f"legal_draft_gate_{legal_draft_id}",
        legal_draft_id=legal_draft_id,
        gate_score=79,
        optimization_required=True,
        low_confidence_flags=["source_trace_review_pending", "lawyer_review_pending", "citation_not_finalized"],
        missing_information_checklist=["补充事实输入确认记录", "补充法律检索候选来源", "补充律师复核备注"],
        review_ready=False,
        warnings=["Gate 仅作为质量参考，不阻断下一步，不触发最终意见、报告或交付。"],
    )


def confirm_legal_draft_for_review(legal_draft_id: str, request: LegalDraftReviewConfirmRequest) -> LegalDraftReviewConfirmation | None:
    draft = get_legal_draft(legal_draft_id)
    if draft is None:
        return None
    confirmed = (
        request.explicit_owner_confirmation
        and request.explicit_lawyer_review_confirmation
        and request.explicit_no_final_opinion_confirmation
        and request.explicit_no_final_report_confirmation
        and request.explicit_no_external_delivery_confirmation
    )
    timestamp = _now()
    review_item = create_review_item(
        linked_object_type="legal_analysis_draft",
        linked_object_id=legal_draft_id,
        case_id=draft.case_id,
        review_focus=["法律分析草稿复核", "来源追踪完整性", "最终意见禁止边界"],
        risk_flags=["draft_only", "not_final_legal_opinion", "not_final_report"],
        created_at=timestamp,
    )
    record_audit_event(action="legal_analysis_draft_confirm_for_review", actor=request.reviewer_id, object_type="legal_analysis_draft", object_id=legal_draft_id, timestamp=timestamp)
    return LegalDraftReviewConfirmation(
        legal_draft_id=legal_draft_id,
        review_item_id=review_item.review_item_id,
        owner_confirmed=confirmed,
        review_ready=confirmed,
        warnings=[
            "确认仅表示进入律师复核队列。",
            "不生成最终法律意见、最终报告、真实文件或外部交付。",
        ],
    )
