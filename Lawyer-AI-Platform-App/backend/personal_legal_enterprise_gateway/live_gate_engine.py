from uuid import uuid4

from personal_legal_enterprise_gateway.provider_config import global_live_enabled, provider_live_enabled
from personal_legal_enterprise_gateway.provider_registry import build_provider, list_provider_metadata
from personal_legal_enterprise_gateway.schemas import LiveGateList, LiveGateMockRequest, LiveGateStatus


def build_live_gate(provider_id: str, request: LiveGateMockRequest | None = None) -> LiveGateStatus | None:
    provider = build_provider(provider_id)
    if provider is None:
        return None
    provider_enabled = provider_live_enabled(provider.provider_id)
    return LiveGateStatus(
        gate_id=f"legal_enterprise_gate_{uuid4().hex[:10]}" if request else f"legal_enterprise_gate_{provider.provider_id}",
        provider_id=provider.provider_id,
        global_live_enabled=global_live_enabled(),
        provider_live_enabled=provider_enabled,
        key_loaded=provider.key_loaded,
        explicit_live_confirmation=bool(request.explicit_live_confirmation) if request else False,
        owner_authorized=bool(request.owner_authorized) if request else False,
        lawyer_review_acknowledged=bool(request.lawyer_review_acknowledged) if request else False,
        external_transfer_acknowledged=bool(request.external_transfer_acknowledged) if request else False,
        source_trace_acknowledged=bool(request.source_trace_acknowledged) if request else False,
        no_training_use_acknowledged=bool(request.no_training_use_acknowledged) if request else False,
        audit_acknowledged=bool(request.audit_acknowledged) if request else False,
        live_gate_status="blocked_by_default",
        live_blocked_reason="global_live_enabled=false; provider_live_enabled=false; v7.29 keeps legal / enterprise live calls disabled",
        next_required_confirmation="explicit_live_confirmation",
        warnings=["Gate metadata only. No legal / enterprise provider network call is executed."],
    )


def build_live_gate_list() -> dict:
    gates = [gate for provider in list_provider_metadata() if (gate := build_live_gate(provider.provider_id)) is not None]
    return LiveGateList(live_gates=gates, live_gate_count=len(gates)).model_dump()


def create_mock_live_gate(request: LiveGateMockRequest) -> dict | None:
    gate = build_live_gate(request.provider_id, request)
    return gate.model_dump() if gate else None

