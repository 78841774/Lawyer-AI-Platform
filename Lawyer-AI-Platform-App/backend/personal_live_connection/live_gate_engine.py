from uuid import uuid4

from personal_live_connection.provider_registry import build_provider, global_live_enabled, provider_live_enabled
from personal_live_connection.schemas import LiveConnectionLiveGate, LiveConnectionRunRequest


def build_live_gate(provider_id: str, request: LiveConnectionRunRequest | None = None) -> LiveConnectionLiveGate | None:
    provider = build_provider(provider_id)
    if provider is None:
        return None
    provider_enabled = provider_live_enabled(provider.provider_id)
    manual = bool(request.manual_confirmation) if request else False
    owner = bool(request.owner_confirmation) if request else False
    lawyer = bool(request.lawyer_gate_acknowledged) if request else False
    raw_boundary = bool(request.raw_content_boundary_acknowledged) if request else False
    allowed = bool(global_live_enabled() and provider_enabled and provider.key_loaded and manual and owner and lawyer and raw_boundary)
    return LiveConnectionLiveGate(
        gate_id=f"personal_live_gate_{uuid4().hex[:10]}" if request else f"personal_live_gate_{provider.provider_id}",
        provider_id=provider.provider_id,
        global_live_enabled=global_live_enabled(),
        provider_live_enabled=provider_enabled,
        key_loaded=provider.key_loaded,
        manual_confirmation_received=manual,
        owner_confirmation_received=owner,
        lawyer_gate_acknowledged=lawyer,
        raw_content_boundary_acknowledged=raw_boundary,
        live_call_allowed=allowed,
        live_call_executed=False,
        network_call_executed=False,
        live_gate_status="eligible_but_adapter_not_executed" if allowed else "blocked_by_default",
        live_blocked_reason="adapter_execution_disabled_in_v7_28" if allowed else _blocked_reason(provider, provider_enabled, manual, owner, lawyer, raw_boundary),
        next_required_confirmation="provider_adapter_implementation" if allowed else "manual_live_confirmation",
        warnings=[
            "Live gate evaluates metadata only.",
            "v7.28 does not execute a provider network call from this unified gateway.",
        ],
    )


def _blocked_reason(provider, provider_enabled: bool, manual: bool, owner: bool, lawyer: bool, raw_boundary: bool) -> str:
    reasons = []
    if not global_live_enabled():
        reasons.append("global_live_disabled")
    if not provider_enabled:
        reasons.append("provider_live_disabled")
    if provider.key_required and not provider.key_loaded:
        reasons.append("key_not_loaded")
    if not manual:
        reasons.append("manual_confirmation_missing")
    if not owner:
        reasons.append("owner_confirmation_missing")
    if not lawyer:
        reasons.append("lawyer_gate_missing")
    if not raw_boundary:
        reasons.append("raw_content_boundary_missing")
    return "; ".join(reasons)

