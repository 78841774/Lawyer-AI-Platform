from personal_legal_enterprise_gateway.live_gate_engine import build_live_gate
from personal_legal_enterprise_gateway.provider_registry import build_provider
from personal_legal_enterprise_gateway.schemas import HealthDryRun


def build_health_dry_run(provider_id: str) -> HealthDryRun | None:
    provider = build_provider(provider_id)
    if provider is None:
        return None
    gate = build_live_gate(provider.provider_id)
    return HealthDryRun(
        provider_id=provider.provider_id,
        key_loaded=provider.key_loaded,
        live_gate_status=gate.live_gate_status if gate else "blocked_by_default",
        adapter_registered=provider.adapter_registered,
        network_call_executed=False,
        live_blocked_reason=gate.live_blocked_reason if gate else "global_live_disabled",
        warnings=["Health check is dry-run metadata only and does not access provider networks."],
    )

