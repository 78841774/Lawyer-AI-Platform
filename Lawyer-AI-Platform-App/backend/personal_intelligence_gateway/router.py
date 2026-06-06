from typing import Any

from fastapi import APIRouter, HTTPException

from personal_intelligence_gateway.audit_engine import build_audit_timeline, build_live_audit_timeline
from personal_intelligence_gateway.confirmation_queue import build_confirmation_queue, submit_confirmation_action
from personal_intelligence_gateway.enterprise_live_gateway import execute_enterprise_live_run, get_enterprise_live_run, list_enterprise_live_runs
from personal_intelligence_gateway.enterprise_query_runtime import (
    build_enterprise_query_list,
    create_mock_enterprise_query,
    get_enterprise_query,
)
from personal_intelligence_gateway.legal_live_gateway import (
    build_live_review_queue,
    execute_legal_live_run,
    get_legal_live_run,
    list_legal_live_runs,
    submit_live_review_action,
)
from personal_intelligence_gateway.legal_search_runtime import build_legal_search_list, create_mock_legal_search, get_legal_search
from personal_intelligence_gateway.provider_config import (
    enterprise_live_mode_enabled,
    get_live_provider_config,
    legal_live_mode_enabled,
    list_live_provider_configs,
)
from personal_intelligence_gateway.provider_registry import get_provider, list_providers
from personal_intelligence_gateway.safety_engine import build_live_safety_status, build_safety_status
from personal_intelligence_gateway.schemas import (
    PersonalEnterpriseQueryMockRequest,
    PersonalIntelligenceConfirmationActionRequest,
    PersonalIntelligenceLiveGatewayStatus,
    PersonalIntelligenceLiveReviewActionRequest,
    PersonalIntelligenceLiveRunRequest,
    PersonalIntelligenceStatus,
    PersonalLegalSearchMockRequest,
)
from personal_intelligence_gateway.source_trace_engine import build_live_source_trace_list, build_source_trace_list, get_live_source_trace, get_source_trace


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


@router.get("/live/status")
def intelligence_live_status() -> dict[str, Any]:
    legal_enabled = legal_live_mode_enabled()
    enterprise_enabled = enterprise_live_mode_enabled()
    return PersonalIntelligenceLiveGatewayStatus(
        legal_live_mode_enabled=legal_enabled,
        enterprise_live_mode_enabled=enterprise_enabled,
        live_mode_enabled=legal_enabled or enterprise_enabled,
        warnings=[
            "Legal / Enterprise API Live Gateway is disabled by default in v7.14.",
            "Dry-run is available and does not call legal or enterprise providers.",
            "Citation and enterprise results are metadata candidates only and are not final citations.",
        ],
    ).model_dump()


@router.get("/live/providers")
def intelligence_live_providers() -> dict[str, Any]:
    return list_live_provider_configs()


@router.get("/live/providers/{provider_id}")
def intelligence_live_provider_detail(provider_id: str) -> dict[str, Any]:
    provider = get_live_provider_config(provider_id)
    if provider is None:
        raise HTTPException(status_code=404, detail="Live provider metadata not found")
    return provider.model_dump()


@router.post("/live/legal-search/dry-run")
def legal_search_live_dry_run(request: PersonalIntelligenceLiveRunRequest) -> dict[str, Any]:
    return execute_legal_live_run(request, dry_run=True)


@router.post("/live/legal-search/runs")
def legal_search_live_run(request: PersonalIntelligenceLiveRunRequest) -> dict[str, Any]:
    return execute_legal_live_run(request, dry_run=False)


@router.get("/live/legal-search/runs")
def legal_search_live_runs() -> dict[str, Any]:
    return list_legal_live_runs()


@router.get("/live/legal-search/runs/{run_id}")
def legal_search_live_run_detail(run_id: str) -> dict[str, Any]:
    run = get_legal_live_run(run_id)
    if run is None:
        raise HTTPException(status_code=404, detail="Legal live run metadata not found")
    return run.model_dump()


@router.post("/live/enterprise-query/dry-run")
def enterprise_query_live_dry_run(request: PersonalIntelligenceLiveRunRequest) -> dict[str, Any]:
    return execute_enterprise_live_run(request, dry_run=True)


@router.post("/live/enterprise-query/runs")
def enterprise_query_live_run(request: PersonalIntelligenceLiveRunRequest) -> dict[str, Any]:
    return execute_enterprise_live_run(request, dry_run=False)


@router.get("/live/enterprise-query/runs")
def enterprise_query_live_runs() -> dict[str, Any]:
    return list_enterprise_live_runs()


@router.get("/live/enterprise-query/runs/{run_id}")
def enterprise_query_live_run_detail(run_id: str) -> dict[str, Any]:
    run = get_enterprise_live_run(run_id)
    if run is None:
        raise HTTPException(status_code=404, detail="Enterprise live run metadata not found")
    return run.model_dump()


@router.get("/live/review-queue")
def intelligence_live_review_queue() -> dict[str, Any]:
    return build_live_review_queue()


@router.post("/live/review-queue/{review_item_id}/actions")
def intelligence_live_review_action(review_item_id: str, request: PersonalIntelligenceLiveReviewActionRequest) -> dict[str, Any]:
    return submit_live_review_action(review_item_id, request)


@router.get("/live/source-traces")
def intelligence_live_source_traces() -> dict[str, Any]:
    return build_live_source_trace_list()


@router.get("/live/source-traces/{source_trace_id}")
def intelligence_live_source_trace_detail(source_trace_id: str) -> dict[str, Any]:
    trace = get_live_source_trace(source_trace_id)
    if trace is None:
        raise HTTPException(status_code=404, detail="Live source_trace_id not found")
    return trace.model_dump()


@router.get("/live/audit")
def intelligence_live_audit() -> dict[str, Any]:
    return build_live_audit_timeline()


@router.get("/live/safety")
def intelligence_live_safety() -> dict[str, Any]:
    return build_live_safety_status()
