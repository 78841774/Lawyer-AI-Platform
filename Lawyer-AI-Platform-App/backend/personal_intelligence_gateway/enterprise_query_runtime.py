from datetime import datetime, timezone
from uuid import uuid4

from fastapi import HTTPException

from personal_intelligence_gateway.audit_engine import record_audit_event
from personal_intelligence_gateway.provider_registry import get_provider, validate_provider
from personal_intelligence_gateway.safety_engine import default_safety_flags
from personal_intelligence_gateway.schemas import (
    PersonalEnterpriseQueryList,
    PersonalEnterpriseQueryMockRequest,
    PersonalEnterpriseQueryResult,
)
from personal_intelligence_gateway.source_trace_engine import create_source_traces
from personal_intelligence_gateway.storage import ENTERPRISE_QUERY_DIR, read_payload, read_payloads, write_payload


ENTERPRISE_QUERY_SCOPES = {
    "business_profile_preview",
    "shareholder_officer_preview",
    "operating_status_preview",
    "judicial_risk_preview",
    "enforcement_signal_preview",
}


def create_mock_enterprise_query(request: PersonalEnterpriseQueryMockRequest) -> dict:
    provider = get_provider(request.provider_id)
    if provider is None:
        raise HTTPException(status_code=404, detail="provider_id 未注册")
    blocked_reasons = [
        *validate_provider(request.provider_id, "enterprise_intelligence"),
        *validate_enterprise_query_request(request),
    ]
    if blocked_reasons:
        raise HTTPException(status_code=400, detail={"message": "模拟企业信息查询请求被阻断。", "blocked_reasons": blocked_reasons})

    enterprise_query_id = f"personal_enterprise_query_{uuid4().hex[:12]}"
    created_at = datetime.now(timezone.utc).isoformat()
    traces = create_source_traces(
        provider_id=request.provider_id,
        query_id=enterprise_query_id,
        source_definitions=[
            {
                "source_type": "enterprise_profile",
                "external_source_label": "企业工商信息候选来源 metadata",
                "source_category": "企业工商信息",
            },
            {
                "source_type": "enterprise_risk",
                "external_source_label": "企业司法风险候选来源 metadata",
                "source_category": "司法风险",
            },
            {
                "source_type": "enforcement_signal",
                "external_source_label": "执行信息候选来源 metadata",
                "source_category": "执行信息",
            },
        ],
        created_at=created_at,
    )
    result = PersonalEnterpriseQueryResult(
        enterprise_query_id=enterprise_query_id,
        case_id=request.case_id,
        provider_id=request.provider_id,
        company_match_summary=f"模拟匹配企业：{_safe_preview(request.company_name)}",
        risk_signal_summary="仅模拟风险信号汇总，未调用真实企业信息服务。",
        query_scope=request.query_scope,
        mock_results=[
            {"result_id": "mock_enterprise_result_1", "source_type": "enterprise_profile", "title": "企业工商信息 metadata", "placeholder_only": True},
            {"result_id": "mock_enterprise_result_2", "source_type": "enterprise_risk", "title": "司法风险 metadata", "placeholder_only": True},
            {"result_id": "mock_enterprise_result_3", "source_type": "enforcement_signal", "title": "执行信息 metadata", "placeholder_only": True},
        ],
        source_trace_ids=[trace.source_trace_id for trace in traces],
        safety_flags=default_safety_flags(),
        created_at=created_at,
        warnings=["仅模拟结果，未调用真实企业信息服务，未返回企业工商原文。"],
    )
    write_payload(ENTERPRISE_QUERY_DIR, enterprise_query_id, result.model_dump())
    record_audit_event(
        action="enterprise_query_mock_created",
        actor="system",
        provider_id=request.provider_id,
        query_id=enterprise_query_id,
        timestamp=created_at,
    )
    return result.model_dump()


def list_enterprise_queries() -> list[PersonalEnterpriseQueryResult]:
    return [PersonalEnterpriseQueryResult(**payload) for payload in read_payloads(ENTERPRISE_QUERY_DIR)]


def get_enterprise_query(enterprise_query_id: str) -> PersonalEnterpriseQueryResult | None:
    payload = read_payload(ENTERPRISE_QUERY_DIR, enterprise_query_id)
    return PersonalEnterpriseQueryResult(**payload) if payload else None


def build_enterprise_query_list() -> dict:
    queries = sorted(list_enterprise_queries(), key=lambda query: query.created_at, reverse=True)
    return PersonalEnterpriseQueryList(
        enterprise_query=queries,
        result_count=len(queries),
        warnings=["企业信息查询列表仅包含模拟 metadata。"],
    ).model_dump()


def validate_enterprise_query_request(request: PersonalEnterpriseQueryMockRequest) -> list[str]:
    blocked: list[str] = []
    if not request.company_name.strip():
        blocked.append("company_name 不能为空")
    if request.query_scope not in ENTERPRISE_QUERY_SCOPES:
        blocked.append("query_scope 不支持")
    if not request.explicit_mock_confirmation:
        blocked.append("explicit_mock_confirmation 必须为 true")
    if not request.explicit_no_live_call_confirmation:
        blocked.append("explicit_no_live_call_confirmation 必须为 true")
    if not request.explicit_no_final_opinion_confirmation:
        blocked.append("explicit_no_final_opinion_confirmation 必须为 true")
    return blocked


def _safe_preview(value: str) -> str:
    return value.strip()[:80] or "未填写企业名称"
