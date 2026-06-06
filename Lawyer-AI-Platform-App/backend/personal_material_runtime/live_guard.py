from personal_material_runtime.provider_config import document_live_mode_enabled, get_live_provider_config, ocr_live_mode_enabled
from personal_material_runtime.schemas import PersonalMaterialLiveRunRequest


REQUIRED_CONFIRMATIONS = {
    "explicit_live_confirmation": "explicit_live_confirmation is required",
    "material_owner_confirmation": "material_owner_confirmation is required",
    "raw_content_handling_acknowledged": "raw_content_handling_acknowledged is required",
    "no_ai_prompt_injection_acknowledged": "no_ai_prompt_injection_acknowledged is required",
    "lawyer_review_acknowledged": "lawyer_review_acknowledged is required",
    "draft_only_acknowledged": "draft_only_acknowledged is required",
}


def live_mode_enabled_for(run_type: str) -> bool:
    if run_type == "ocr":
        return ocr_live_mode_enabled()
    return document_live_mode_enabled()


def validate_live_gate(request: PersonalMaterialLiveRunRequest, *, run_type: str) -> list[str]:
    provider = get_live_provider_config(request.provider_id)
    blocked: list[str] = []
    if provider is None:
        return ["provider_id is not registered"]
    if run_type == "ocr" and provider.provider_type != "ocr":
        blocked.append("provider_type must be ocr")
    if run_type == "document" and provider.provider_type != "document_parser":
        blocked.append("provider_type must be document_parser")
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
