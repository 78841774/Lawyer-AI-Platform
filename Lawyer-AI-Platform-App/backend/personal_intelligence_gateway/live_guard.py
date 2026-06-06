from personal_intelligence_gateway.provider_config import (
    enterprise_live_mode_enabled,
    get_live_provider_config,
    legal_live_mode_enabled,
)
from personal_intelligence_gateway.schemas import PersonalIntelligenceLiveRunRequest


REQUIRED_CONFIRMATIONS = {
    "explicit_live_confirmation": "explicit_live_confirmation is required",
    "query_owner_confirmation": "query_owner_confirmation is required",
    "raw_content_handling_acknowledged": "raw_content_handling_acknowledged is required",
    "no_ai_prompt_injection_acknowledged": "no_ai_prompt_injection_acknowledged is required",
    "lawyer_review_acknowledged": "lawyer_review_acknowledged is required",
    "draft_only_acknowledged": "draft_only_acknowledged is required",
    "no_final_citation_acknowledged": "no_final_citation_acknowledged is required",
}


def live_mode_enabled_for(run_type: str) -> bool:
    if run_type == "enterprise":
        return enterprise_live_mode_enabled()
    return legal_live_mode_enabled()


def validate_live_gate(request: PersonalIntelligenceLiveRunRequest, *, run_type: str) -> list[str]:
    provider = get_live_provider_config(request.provider_id)
    blocked: list[str] = []
    if provider is None:
        return ["provider_id is not registered"]
    if run_type == "legal" and provider.provider_type != "legal_search":
        blocked.append("provider_type must be legal_search")
    if run_type == "enterprise" and provider.provider_type != "enterprise_info":
        blocked.append("provider_type must be enterprise_info")
    if request.dry_run:
        return blocked
    if not live_mode_enabled_for(run_type):
        blocked.append(f"{run_type}_live_mode_enabled is false")
    if not provider.live_supported:
        blocked.append("provider live_supported is false")
    if not provider.live_enabled:
        blocked.append("provider live_enabled is false")
    if provider.key_required and not provider.key_loaded:
        blocked.append("provider key_loaded is false")
    for field_name, reason in REQUIRED_CONFIRMATIONS.items():
        if not getattr(request, field_name):
            blocked.append(reason)
    return blocked
