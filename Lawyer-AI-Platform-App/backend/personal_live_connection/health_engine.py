from personal_live_connection.live_gate_engine import build_live_gate
from personal_live_connection.provider_registry import build_provider
from personal_live_connection.schemas import LiveConnectionHealthDryRun


def build_health_dry_run(provider_id: str) -> LiveConnectionHealthDryRun | None:
    provider = build_provider(provider_id)
    if provider is None:
        return None
    gate = build_live_gate(provider.provider_id)
    return LiveConnectionHealthDryRun(
        provider_id=provider.provider_id,
        key_loaded=provider.key_loaded,
        adapter_registered=provider.adapter_registered,
        live_blocked_reason=gate.live_blocked_reason if gate else "global_live_disabled",
        warnings=["Dry-run health does not call provider networks or upload materials."],
    )

