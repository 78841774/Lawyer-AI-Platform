from typing import Any

from fastapi import APIRouter, HTTPException

from personal_ai_gateway.audit_engine import build_audit_timeline, build_run_list, get_run, list_runs
from personal_ai_gateway.live_gateway import (
    build_live_audit_timeline,
    build_live_run_list,
    build_live_safety_status,
    execute_live_gateway_run,
    get_live_run,
)
from personal_ai_gateway.prompt_registry import get_prompt_template, list_prompt_templates
from personal_ai_gateway.prompt_renderer import render_prompt_preview
from personal_ai_gateway.prompt_runtime import create_mock_run
from personal_ai_gateway.provider_config import build_live_gateway_status, get_live_provider_config, list_live_provider_configs
from personal_ai_gateway.provider_registry import get_provider, list_providers
from personal_ai_gateway.safety_engine import build_safety_status
from personal_ai_gateway.schemas import (
    PersonalAIGatewayStatus,
    PersonalAILiveRunRequest,
    PersonalAIMockRunRequest,
    PersonalAIPromptRenderPreviewRequest,
)
from personal_ai_gateway.token_usage_engine import summarize_token_usage


router = APIRouter(prefix="/personal-ai-gateway", tags=["personal-ai-gateway"])


@router.get("/status")
def gateway_status() -> dict[str, Any]:
    return PersonalAIGatewayStatus(
        warnings=[
            "v7.1 AI Gateway is mock-first and provider-gated.",
            "No live provider call is enabled in v7.1.",
            "AI output is draft-only and requires lawyer review.",
        ],
    ).model_dump()


@router.get("/providers")
def providers() -> dict[str, Any]:
    return list_providers()


@router.get("/providers/{provider_id}")
def provider_detail(provider_id: str) -> dict[str, Any]:
    provider = get_provider(provider_id)
    if provider is None:
        raise HTTPException(status_code=404, detail="Provider metadata not found")
    return provider.model_dump()


@router.get("/prompt-templates")
def prompt_templates() -> dict[str, Any]:
    return list_prompt_templates()


@router.get("/prompt-templates/{template_id}")
def prompt_template_detail(template_id: str) -> dict[str, Any]:
    template = get_prompt_template(template_id)
    if template is None:
        raise HTTPException(status_code=404, detail="Prompt template metadata not found")
    return template.model_dump()


@router.post("/prompt-render-preview")
def prompt_render_preview(request: PersonalAIPromptRenderPreviewRequest) -> dict[str, Any]:
    return render_prompt_preview(request)


@router.post("/runs/mock")
def mock_run(request: PersonalAIMockRunRequest) -> dict[str, Any]:
    return create_mock_run(request)


@router.get("/runs")
def runs() -> dict[str, Any]:
    return build_run_list()


@router.get("/runs/{ai_run_id}")
def run_detail(ai_run_id: str) -> dict[str, Any]:
    run = get_run(ai_run_id)
    if run is None:
        raise HTTPException(status_code=404, detail="AI run metadata not found")
    return run.model_dump()


@router.get("/audit")
def audit() -> dict[str, Any]:
    return build_audit_timeline()


@router.get("/token-usage/summary")
def token_usage_summary() -> dict[str, Any]:
    return summarize_token_usage(list_runs())


@router.get("/safety")
def safety() -> dict[str, Any]:
    return build_safety_status()


@router.get("/live/status")
def live_status() -> dict[str, Any]:
    return build_live_gateway_status()


@router.get("/live/providers")
def live_providers() -> dict[str, Any]:
    return list_live_provider_configs()


@router.get("/live/providers/{provider_id}")
def live_provider_detail(provider_id: str) -> dict[str, Any]:
    provider = get_live_provider_config(provider_id)
    if provider is None:
        raise HTTPException(status_code=404, detail="Live provider metadata not found")
    return provider.model_dump()


@router.post("/live/dry-run")
def live_dry_run(request: PersonalAILiveRunRequest) -> dict[str, Any]:
    request.dry_run = True
    return execute_live_gateway_run(request)


@router.post("/live/runs")
def live_run(request: PersonalAILiveRunRequest) -> dict[str, Any]:
    return execute_live_gateway_run(request)


@router.get("/live/runs")
def live_runs() -> dict[str, Any]:
    return build_live_run_list()


@router.get("/live/runs/{run_id}")
def live_run_detail(run_id: str) -> dict[str, Any]:
    run = get_live_run(run_id)
    if run is None:
        raise HTTPException(status_code=404, detail="AI live run metadata not found")
    return run.model_dump()


@router.get("/live/audit")
def live_audit() -> dict[str, Any]:
    return build_live_audit_timeline()


@router.get("/live/safety")
def live_safety() -> dict[str, Any]:
    return build_live_safety_status()
