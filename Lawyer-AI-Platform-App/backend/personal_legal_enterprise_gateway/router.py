from typing import Any

from fastapi import APIRouter, HTTPException

from personal_legal_enterprise_gateway.audit_engine import build_audit_timeline
from personal_legal_enterprise_gateway.enterprise_lookup_engine import create_enterprise_lookup, get_enterprise_lookup, list_enterprise_lookups
from personal_legal_enterprise_gateway.health_engine import build_health_dry_run
from personal_legal_enterprise_gateway.legal_search_engine import create_legal_search, get_legal_search, list_legal_searches
from personal_legal_enterprise_gateway.live_gate_engine import build_live_gate, build_live_gate_list, create_mock_live_gate
from personal_legal_enterprise_gateway.provider_registry import build_categories, build_provider, build_provider_list, list_provider_metadata
from personal_legal_enterprise_gateway.readiness_engine import build_status
from personal_legal_enterprise_gateway.review_queue import build_review_queue, submit_review_action
from personal_legal_enterprise_gateway.safety_engine import build_safety_status
from personal_legal_enterprise_gateway.schemas import EnterpriseLookupRequest, LegalSearchRequest, LiveGateMockRequest, ReviewActionRequest
from personal_legal_enterprise_gateway.secret_boundary import build_secret_boundary
from personal_legal_enterprise_gateway.source_trace_engine import build_source_traces
from personal_legal_enterprise_gateway.usage_policy_engine import build_usage_policy


router = APIRouter(prefix="/personal-legal-enterprise", tags=["personal-legal-enterprise"])


def _ensure(payload):
    if payload is None:
        raise HTTPException(status_code=404, detail="metadata not found")
    return payload


@router.get("/status")
def status() -> dict[str, Any]:
    return build_status()


@router.get("/providers")
def providers() -> dict[str, Any]:
    return build_provider_list()


@router.get("/providers/{provider_id}")
def provider_detail(provider_id: str) -> dict[str, Any]:
    return _ensure(build_provider(provider_id)).model_dump()


@router.get("/providers/{provider_id}/secret-boundary")
def provider_secret_boundary(provider_id: str) -> dict[str, Any]:
    return _ensure(build_secret_boundary(provider_id)).model_dump()


@router.get("/providers/{provider_id}/live-gate")
def provider_live_gate(provider_id: str) -> dict[str, Any]:
    return _ensure(build_live_gate(provider_id)).model_dump()


@router.get("/providers/{provider_id}/usage-policy")
def provider_usage_policy(provider_id: str) -> dict[str, Any]:
    return _ensure(build_usage_policy(provider_id)).model_dump()


@router.get("/providers/{provider_id}/health/dry-run")
def provider_health(provider_id: str) -> dict[str, Any]:
    return _ensure(build_health_dry_run(provider_id)).model_dump()


@router.get("/categories")
def categories() -> dict[str, Any]:
    return build_categories()


@router.get("/categories/{category}/providers")
def category_providers(category: str) -> dict[str, Any]:
    providers = [provider for provider in list_provider_metadata() if provider.provider_category == category]
    return build_provider_list(providers)


@router.post("/live-gates/mock")
def live_gates_mock(request: LiveGateMockRequest) -> dict[str, Any]:
    return _ensure(create_mock_live_gate(request))


@router.get("/live-gates")
def live_gates() -> dict[str, Any]:
    return build_live_gate_list()


@router.post("/legal-search/dry-run")
def legal_search_dry_run(request: LegalSearchRequest) -> dict[str, Any]:
    return create_legal_search(request, dry_run=True)


@router.post("/legal-search/runs")
def legal_search_run(request: LegalSearchRequest) -> dict[str, Any]:
    return create_legal_search(request, dry_run=False)


@router.get("/legal-search/runs")
def legal_search_runs() -> dict[str, Any]:
    return list_legal_searches()


@router.get("/legal-search/runs/{run_id}")
def legal_search_run_detail(run_id: str) -> dict[str, Any]:
    return _ensure(get_legal_search(run_id)).model_dump()


@router.post("/enterprise-lookup/dry-run")
def enterprise_lookup_dry_run(request: EnterpriseLookupRequest) -> dict[str, Any]:
    return create_enterprise_lookup(request, dry_run=True)


@router.post("/enterprise-lookup/runs")
def enterprise_lookup_run(request: EnterpriseLookupRequest) -> dict[str, Any]:
    return create_enterprise_lookup(request, dry_run=False)


@router.get("/enterprise-lookup/runs")
def enterprise_lookup_runs() -> dict[str, Any]:
    return list_enterprise_lookups()


@router.get("/enterprise-lookup/runs/{run_id}")
def enterprise_lookup_run_detail(run_id: str) -> dict[str, Any]:
    return _ensure(get_enterprise_lookup(run_id)).model_dump()


@router.get("/review-queue")
def review_queue() -> dict[str, Any]:
    return build_review_queue()


@router.post("/review-queue/{review_item_id}/actions/mock")
def review_action(review_item_id: str, request: ReviewActionRequest) -> dict[str, Any]:
    return submit_review_action(review_item_id, request)


@router.get("/source-traces")
def source_traces() -> dict[str, Any]:
    return build_source_traces()


@router.get("/audit")
def audit() -> dict[str, Any]:
    return build_audit_timeline()


@router.get("/safety")
def safety() -> dict[str, Any]:
    return build_safety_status()

