from personal_provider_readiness.provider_registry import list_provider_metadata
from personal_production_pilot.schemas import ProviderGate, ProviderGateSummary


def build_provider_gate_summary() -> dict:
    gates = [
        ProviderGate(
            provider_id=provider.provider_id,
            display_name=provider.provider_name,
            category=provider.provider_category,
            live_enabled=provider.live_call_allowed,
            dry_run_ready=provider.dry_run_supported,
            adapter_status="adapter_registered" if provider.adapter_registered else "gated_or_adapter_unavailable",
            warnings=[
                "Live mode is disabled by default and routed through v7.26 provider readiness plus v7.27 OCR / Document connection metadata.",
                "External provider use requires explicit confirmation in a later target version.",
                "API key values are not read or returned.",
            ],
        )
        for provider in list_provider_metadata()
    ]
    return ProviderGateSummary(
        provider_gates=gates,
        provider_count=len(gates),
        live_enabled_count=sum(1 for gate in gates if gate.live_enabled),
        dry_run_ready_count=sum(1 for gate in gates if gate.dry_run_ready),
        warnings=["Provider gates are aggregated from readiness metadata; no API key value lookup, file upload, or provider call is performed."],
    ).model_dump()
