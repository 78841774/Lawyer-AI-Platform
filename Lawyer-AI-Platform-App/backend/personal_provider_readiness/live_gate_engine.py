from uuid import uuid4

from personal_provider_readiness.provider_registry import get_provider, list_provider_metadata
from personal_provider_readiness.schemas import LiveGateList, LiveGateMockRequest, LiveGateStatus


def build_live_gate(provider_id: str, request: LiveGateMockRequest | None = None) -> LiveGateStatus | None:
    provider = get_provider(provider_id)
    if provider is None:
        return None
    return LiveGateStatus(
        gate_id=f"live_gate_{uuid4().hex[:10]}" if request else f"live_gate_{provider.provider_id}",
        provider_id=provider.provider_id,
        global_live_enabled=False,
        provider_live_enabled=False,
        key_loaded=provider.key_loaded,
        explicit_live_confirmation=bool(request.explicit_live_confirmation) if request else False,
        owner_authorized=bool(request.owner_authorized) if request else False,
        external_transfer_acknowledged=bool(request.external_transfer_acknowledged) if request else False,
        no_training_use_acknowledged=bool(request.no_training_use_acknowledged) if request else False,
        audit_acknowledged=bool(request.audit_acknowledged) if request else False,
        live_gate_status="blocked_by_default",
        live_blocked_reason="global_live_enabled=false; provider_live_enabled=false; v7.26 is readiness-only",
        next_required_confirmation="v7.27_target_provider_connection_confirmation",
        warnings=[
            "Even if key_loaded=true, v7.26 does not allow or execute live provider calls.",
            "The gate record is dry-run metadata only.",
        ],
    )


def build_live_gate_list() -> dict:
    gates = [build_live_gate(provider.provider_id) for provider in list_provider_metadata()]
    safe_gates = [gate for gate in gates if gate is not None]
    return LiveGateList(live_gates=safe_gates, live_gate_count=len(safe_gates)).model_dump()


def create_mock_live_gate(request: LiveGateMockRequest) -> dict | None:
    gate = build_live_gate(request.provider_id, request)
    return gate.model_dump() if gate else None

