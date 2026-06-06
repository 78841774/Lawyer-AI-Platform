from personal_provider_readiness.live_gate_engine import build_live_gate
from personal_provider_readiness.provider_registry import get_provider
from personal_provider_readiness.schemas import ProviderHealthDryRun


def build_health_dry_run(provider_id: str) -> ProviderHealthDryRun | None:
    provider = get_provider(provider_id)
    if provider is None:
        return None
    gate = build_live_gate(provider.provider_id)
    return ProviderHealthDryRun(
        provider_id=provider.provider_id,
        config_detected=True,
        key_loaded=provider.key_loaded,
        live_gate_status=gate.live_gate_status if gate else "blocked_by_default",
        adapter_registered=provider.adapter_registered,
        dry_run_ready=True,
        live_blocked_reason=gate.live_blocked_reason if gate else "global_live_disabled",
        next_required_confirmation=gate.next_required_confirmation if gate else "explicit_live_confirmation",
        network_call_executed=False,
        warnings=[
            "Dry-run health check does not call the provider network.",
            "It only reports configuration, key_loaded boolean metadata, adapter state, and blocked gate reason.",
        ],
    )

