from datetime import datetime, timezone
from uuid import uuid4

from fastapi import HTTPException

from personal_intelligence_gateway.audit_engine import record_audit_event
from personal_intelligence_gateway.provider_registry import get_provider, validate_provider
from personal_intelligence_gateway.safety_engine import default_safety_flags
from personal_intelligence_gateway.schemas import (
    PersonalLegalSearchList,
    PersonalLegalSearchMockRequest,
    PersonalLegalSearchResult,
)
from personal_intelligence_gateway.source_trace_engine import create_source_traces
from personal_intelligence_gateway.storage import LEGAL_SEARCH_DIR, read_payload, read_payloads, write_payload


LEGAL_SEARCH_SCOPES = {
    "regulation_search",
    "case_law_search",
    "judgment_rule_search",
    "article_detail_preview",
    "case_detail_preview",
}


def create_mock_legal_search(request: PersonalLegalSearchMockRequest) -> dict:
    provider = get_provider(request.provider_id)
    if provider is None:
        raise HTTPException(status_code=404, detail="provider_id 未注册")
    blocked_reasons = [
        *validate_provider(request.provider_id, "legal_search"),
        *validate_legal_search_request(request),
    ]
    if blocked_reasons:
        raise HTTPException(status_code=400, detail={"message": "模拟法律检索请求被阻断。", "blocked_reasons": blocked_reasons})

    legal_search_id = f"personal_legal_search_{uuid4().hex[:12]}"
    created_at = datetime.now(timezone.utc).isoformat()
    traces = create_source_traces(
        provider_id=request.provider_id,
        query_id=legal_search_id,
        source_definitions=[
            {
                "source_type": "legal_regulation",
                "external_source_label": "法律法规检索候选来源 metadata",
                "source_category": "法律法规",
            },
            {
                "source_type": "legal_case",
                "external_source_label": "司法案例检索候选来源 metadata",
                "source_category": "司法案例",
            },
            {
                "source_type": "judgment_rule",
                "external_source_label": "裁判规则候选来源 metadata",
                "source_category": "裁判规则",
            },
        ],
        created_at=created_at,
    )
    result = PersonalLegalSearchResult(
        legal_search_id=legal_search_id,
        case_id=request.case_id,
        provider_id=request.provider_id,
        query_summary=f"模拟检索：{_safe_preview(request.query)}",
        search_scope=request.search_scope,
        jurisdiction=request.jurisdiction,
        legal_area=request.legal_area,
        result_count=3,
        mock_results=[
            {"result_id": "mock_legal_result_1", "source_type": "legal_regulation", "title": "法律法规候选 metadata", "placeholder_only": True},
            {"result_id": "mock_legal_result_2", "source_type": "legal_case", "title": "司法案例候选 metadata", "placeholder_only": True},
            {"result_id": "mock_legal_result_3", "source_type": "judgment_rule", "title": "裁判规则候选 metadata", "placeholder_only": True},
        ],
        citation_candidates=[
            {"source_trace_id": trace.source_trace_id, "citation_status": trace.citation_status, "lawyer_confirmed": False}
            for trace in traces
        ],
        source_trace_ids=[trace.source_trace_id for trace in traces],
        safety_flags=default_safety_flags(),
        created_at=created_at,
        warnings=["仅模拟结果，未调用真实法律检索服务，未返回法条全文或案例原文。"],
    )
    write_payload(LEGAL_SEARCH_DIR, legal_search_id, result.model_dump())
    record_audit_event(
        action="legal_search_mock_created",
        actor="system",
        provider_id=request.provider_id,
        query_id=legal_search_id,
        timestamp=created_at,
    )
    return result.model_dump()


def list_legal_searches() -> list[PersonalLegalSearchResult]:
    return [PersonalLegalSearchResult(**payload) for payload in read_payloads(LEGAL_SEARCH_DIR)]


def get_legal_search(legal_search_id: str) -> PersonalLegalSearchResult | None:
    payload = read_payload(LEGAL_SEARCH_DIR, legal_search_id)
    return PersonalLegalSearchResult(**payload) if payload else None


def build_legal_search_list() -> dict:
    searches = sorted(list_legal_searches(), key=lambda search: search.created_at, reverse=True)
    return PersonalLegalSearchList(
        legal_search=searches,
        result_count=len(searches),
        warnings=["法律检索列表仅包含模拟 metadata。"],
    ).model_dump()


def validate_legal_search_request(request: PersonalLegalSearchMockRequest) -> list[str]:
    blocked: list[str] = []
    if not request.query.strip():
        blocked.append("query 不能为空")
    if request.search_scope not in LEGAL_SEARCH_SCOPES:
        blocked.append("search_scope 不支持")
    if not request.explicit_mock_confirmation:
        blocked.append("explicit_mock_confirmation 必须为 true")
    if not request.explicit_no_live_call_confirmation:
        blocked.append("explicit_no_live_call_confirmation 必须为 true")
    if not request.explicit_no_final_opinion_confirmation:
        blocked.append("explicit_no_final_opinion_confirmation 必须为 true")
    return blocked


def _safe_preview(value: str) -> str:
    return value.strip()[:80] or "未填写查询词"
