from personal_ai_gateway.provider_config import get_live_provider_config, live_mode_enabled
from personal_ai_gateway.schemas import PersonalAILiveRunRequest


def build_confirmations(request: PersonalAILiveRunRequest) -> dict[str, bool]:
    return {
        "explicit_live_confirmation": request.explicit_live_confirmation,
        "lawyer_review_acknowledged": request.lawyer_review_acknowledged,
        "draft_only_acknowledged": request.draft_only_acknowledged,
        "no_final_opinion_acknowledged": request.no_final_opinion_acknowledged,
        "no_final_report_acknowledged": request.no_final_report_acknowledged,
        "no_external_delivery_acknowledged": request.no_external_delivery_acknowledged,
    }


def validate_live_gate(request: PersonalAILiveRunRequest) -> list[str]:
    blocked: list[str] = []
    provider = get_live_provider_config(request.provider_id)
    if provider is None:
        return ["provider is not registered"]
    if request.dry_run:
        return []
    if not live_mode_enabled():
        blocked.append("AI_LIVE_MODE_ENABLED is false")
    if not provider.live_enabled:
        blocked.append("provider live_enabled is false")
    if provider.key_required and not provider.key_loaded:
        blocked.append("provider key_loaded is false")
    for name, value in build_confirmations(request).items():
        if not value:
            blocked.append(f"{name} is required")
    return blocked
