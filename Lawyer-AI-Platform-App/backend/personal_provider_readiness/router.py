from typing import Any

from fastapi import APIRouter, HTTPException

from personal_provider_readiness.audit_engine import build_audit_timeline
from personal_provider_readiness.live_gate_engine import build_live_gate, build_live_gate_list, create_mock_live_gate
from personal_provider_readiness.provider_health_engine import build_health_dry_run
from personal_provider_readiness.provider_registry import build_provider_list, get_provider, list_provider_metadata
from personal_provider_readiness.readiness_engine import build_status
from personal_provider_readiness.safety_engine import build_safety_status
from personal_provider_readiness.schemas import CategorySummary, CategorySummaryList, LiveGateMockRequest, SecretBoundaryStatus
from personal_provider_readiness.usage_policy_engine import build_usage_policy


router = APIRouter(prefix="/personal-provider-readiness", tags=["personal-provider-readiness"])


@router.get("/status")
def status() -> dict[str, Any]:
    return build_status()


@router.get("/providers")
def providers() -> dict[str, Any]:
    return build_provider_list()


@router.get("/providers/{provider_id}")
def provider_detail(provider_id: str) -> dict[str, Any]:
    provider = get_provider(provider_id)
    if provider is None:
        raise HTTPException(status_code=404, detail="provider_id 不存在")
    return provider.model_dump()


@router.get("/providers/{provider_id}/secret-boundary")
def provider_secret_boundary(provider_id: str) -> dict[str, Any]:
    provider = get_provider(provider_id)
    if provider is None:
        raise HTTPException(status_code=404, detail="provider_id 不存在")
    return SecretBoundaryStatus(
        provider_id=provider.provider_id,
        key_env_names=provider.key_env_names,
        requires_api_key=provider.requires_api_key,
        key_loaded=provider.key_loaded,
        key_source=provider.key_source,
        warnings=["Only key_loaded boolean metadata is returned. No key value, prefix, suffix, or masked key is returned."],
    ).model_dump()


@router.get("/providers/{provider_id}/live-gate")
def provider_live_gate(provider_id: str) -> dict[str, Any]:
    gate = build_live_gate(provider_id)
    if gate is None:
        raise HTTPException(status_code=404, detail="provider_id 不存在")
    return gate.model_dump()


@router.get("/providers/{provider_id}/usage-policy")
def provider_usage_policy(provider_id: str) -> dict[str, Any]:
    usage = build_usage_policy(provider_id)
    if usage is None:
        raise HTTPException(status_code=404, detail="provider_id 不存在")
    return usage.model_dump()


@router.get("/providers/{provider_id}/health/dry-run")
def provider_health_dry_run(provider_id: str) -> dict[str, Any]:
    health = build_health_dry_run(provider_id)
    if health is None:
        raise HTTPException(status_code=404, detail="provider_id 不存在")
    return health.model_dump()


@router.get("/categories")
def categories() -> dict[str, Any]:
    providers = list_provider_metadata()
    summaries = []
    for category in sorted({provider.provider_category for provider in providers}):
        category_providers = [provider for provider in providers if provider.provider_category == category]
        summaries.append(
            CategorySummary(
                category=category,
                provider_count=len(category_providers),
                key_loaded_count=sum(1 for provider in category_providers if provider.key_loaded),
                dry_run_ready_count=sum(1 for provider in category_providers if provider.dry_run_supported),
                live_disabled_count=len(category_providers),
                blocked_provider_count=len(category_providers),
            )
        )
    return CategorySummaryList(categories=summaries, category_count=len(summaries)).model_dump()


@router.get("/categories/{category}/providers")
def category_providers(category: str) -> dict[str, Any]:
    providers = [provider for provider in list_provider_metadata() if provider.provider_category == category]
    return build_provider_list() | {
        "providers": [provider.model_dump() for provider in providers],
        "provider_count": len(providers),
        "key_loaded_count": sum(1 for provider in providers if provider.key_loaded),
        "dry_run_ready_count": sum(1 for provider in providers if provider.dry_run_supported),
        "live_disabled_count": len(providers),
        "blocked_provider_count": len(providers),
    }


@router.post("/live-gates/mock")
def live_gates_mock(request: LiveGateMockRequest) -> dict[str, Any]:
    gate = create_mock_live_gate(request)
    if gate is None:
        raise HTTPException(status_code=404, detail="provider_id 不存在")
    return gate


@router.get("/live-gates")
def live_gates() -> dict[str, Any]:
    return build_live_gate_list()


@router.get("/audit")
def audit() -> dict[str, Any]:
    return build_audit_timeline()


@router.get("/safety")
def safety() -> dict[str, Any]:
    return build_safety_status()

