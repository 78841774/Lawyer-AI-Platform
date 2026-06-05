from typing import Any

from fastapi import APIRouter, HTTPException

from personal_intelligence_gateway.audit_engine import build_audit_timeline
from personal_intelligence_gateway.confirmation_queue import build_confirmation_queue, submit_confirmation_action
from personal_intelligence_gateway.enterprise_query_runtime import (
    build_enterprise_query_list,
    create_mock_enterprise_query,
    get_enterprise_query,
)
from personal_intelligence_gateway.legal_search_runtime import build_legal_search_list, create_mock_legal_search, get_legal_search
from personal_intelligence_gateway.provider_registry import get_provider, list_providers
from personal_intelligence_gateway.safety_engine import build_safety_status
from personal_intelligence_gateway.schemas import (
    PersonalEnterpriseQueryMockRequest,
    PersonalIntelligenceConfirmationActionRequest,
    PersonalIntelligenceStatus,
    PersonalLegalSearchMockRequest,
)
from personal_intelligence_gateway.source_trace_engine import build_source_trace_list, get_source_trace


router = APIRouter(prefix="/personal-intelligence", tags=["personal-intelligence"])


@router.get("/status")
def intelligence_status() -> dict[str, Any]:
    return PersonalIntelligenceStatus(
        warnings=[
            "v7.3 法律与企业信息网关仅返回模拟 metadata。",
            "未调用真实法律检索或企业信息服务。",
            "律师确认必需，且不生成最终法律意见或最终报告。",
        ],
    ).model_dump()


@router.get("/providers")
def providers() -> dict[str, Any]:
    return list_providers()


@router.get("/providers/{provider_id}")
def provider_detail(provider_id: str) -> dict[str, Any]:
    provider = get_provider(provider_id)
    if provider is None:
        raise HTTPException(status_code=404, detail="Provider metadata 不存在")
    return provider.model_dump()


@router.post("/legal-search/mock")
def legal_search_mock(request: PersonalLegalSearchMockRequest) -> dict[str, Any]:
    return create_mock_legal_search(request)


@router.get("/legal-search")
def legal_search_list() -> dict[str, Any]:
    return build_legal_search_list()


@router.get("/legal-search/{legal_search_id}")
def legal_search_detail(legal_search_id: str) -> dict[str, Any]:
    result = get_legal_search(legal_search_id)
    if result is None:
        raise HTTPException(status_code=404, detail="legal_search_id 不存在")
    return result.model_dump()


@router.post("/enterprise-query/mock")
def enterprise_query_mock(request: PersonalEnterpriseQueryMockRequest) -> dict[str, Any]:
    return create_mock_enterprise_query(request)


@router.get("/enterprise-query")
def enterprise_query_list() -> dict[str, Any]:
    return build_enterprise_query_list()


@router.get("/enterprise-query/{enterprise_query_id}")
def enterprise_query_detail(enterprise_query_id: str) -> dict[str, Any]:
    result = get_enterprise_query(enterprise_query_id)
    if result is None:
        raise HTTPException(status_code=404, detail="enterprise_query_id 不存在")
    return result.model_dump()


@router.get("/source-traces")
def source_trace_list() -> dict[str, Any]:
    return build_source_trace_list()


@router.get("/source-traces/{source_trace_id}")
def source_trace_detail(source_trace_id: str) -> dict[str, Any]:
    trace = get_source_trace(source_trace_id)
    if trace is None:
        raise HTTPException(status_code=404, detail="source_trace_id 不存在")
    return trace.model_dump()


@router.get("/confirmation-queue")
def confirmation_queue() -> dict[str, Any]:
    return build_confirmation_queue()


@router.post("/confirmation-queue/{source_trace_id}/actions")
def confirmation_action(source_trace_id: str, request: PersonalIntelligenceConfirmationActionRequest) -> dict[str, Any]:
    return submit_confirmation_action(source_trace_id, request)


@router.get("/audit")
def audit() -> dict[str, Any]:
    return build_audit_timeline()


@router.get("/safety")
def safety() -> dict[str, Any]:
    return build_safety_status()
