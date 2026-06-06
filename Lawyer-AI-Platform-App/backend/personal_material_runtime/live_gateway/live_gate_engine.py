from uuid import uuid4

from personal_material_runtime.live_gateway.provider_registry import build_provider_readiness, list_provider_readiness
from personal_material_runtime.schemas import PersonalMaterialLiveGateList, PersonalMaterialLiveGateMockRequest, PersonalMaterialLiveGateStatus


def build_live_gate(provider_id: str, request: PersonalMaterialLiveGateMockRequest | None = None) -> PersonalMaterialLiveGateStatus | None:
    provider = build_provider_readiness(provider_id)
    if provider is None:
        return None
    return PersonalMaterialLiveGateStatus(
        gate_id=f"material_live_gate_{uuid4().hex[:10]}" if request else f"material_live_gate_{provider.provider_id}",
        provider_id=provider.provider_id,
        global_live_enabled=False,
        provider_live_enabled=False,
        key_loaded=provider.key_loaded,
        explicit_live_confirmation=bool(request.explicit_live_confirmation) if request else False,
        owner_authorized=bool(request.owner_authorized) if request else False,
        raw_content_boundary_acknowledged=bool(request.raw_content_boundary_acknowledged) if request else False,
        no_ai_prompt_injection_acknowledged=bool(request.no_ai_prompt_injection_acknowledged) if request else False,
        audit_acknowledged=bool(request.audit_acknowledged) if request else False,
        live_gate_status="blocked_by_default",
        live_blocked_reason="global_live_enabled=false; provider_live_enabled=false; v7.27 keeps OCR / Document live calls disabled",
        next_required_confirmation="v7_27_owner_live_connection_confirmation",
        warnings=[
            "Gate metadata does not execute OCR / document provider calls.",
            "Owner confirmation, raw-content boundary acknowledgement, no-AI-prompt acknowledgement, and audit metadata are required before any future live eligibility.",
        ],
    )


def create_mock_live_gate(request: PersonalMaterialLiveGateMockRequest) -> dict | None:
    gate = build_live_gate(request.provider_id, request)
    return gate.model_dump() if gate else None


def build_live_gate_list() -> dict:
    gates = [gate for provider in list_provider_readiness() if (gate := build_live_gate(provider.provider_id)) is not None]
    return PersonalMaterialLiveGateList(
        live_gates=gates,
        live_gate_count=len(gates),
        warnings=["All OCR / Document live gates are blocked by default in v7.27."],
    ).model_dump()

