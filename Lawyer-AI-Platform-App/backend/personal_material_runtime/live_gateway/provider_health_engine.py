from personal_material_runtime.live_gateway.live_gate_engine import build_live_gate
from personal_material_runtime.live_gateway.provider_registry import build_provider_readiness
from personal_material_runtime.schemas import PersonalMaterialLiveHealthDryRun


def build_health_dry_run(provider_id: str) -> PersonalMaterialLiveHealthDryRun | None:
    provider = build_provider_readiness(provider_id)
    if provider is None:
        return None
    gate = build_live_gate(provider.provider_id)
    return PersonalMaterialLiveHealthDryRun(
        provider_id=provider.provider_id,
        config_detected=True,
        key_loaded=provider.key_loaded,
        live_gate_status=gate.live_gate_status if gate else "blocked_by_default",
        adapter_registered=provider.adapter_registered,
        dry_run_ready=True,
        live_blocked_reason=gate.live_blocked_reason if gate else "global_live_disabled",
        next_required_confirmation=gate.next_required_confirmation if gate else "v7_27_owner_live_connection_confirmation",
        network_call_executed=False,
        upload_executed=False,
        raw_content_uploaded=False,
        warnings=[
            "Dry-run health check only reports configuration metadata.",
            "No provider network call, file upload, raw OCR text exposure, or document content exposure occurs.",
        ],
    )

