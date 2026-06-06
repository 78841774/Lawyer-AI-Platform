from personal_material_runtime.live_gateway.provider_registry import build_provider_readiness
from personal_material_runtime.schemas import PersonalMaterialLiveSecretBoundary


def build_secret_boundary(provider_id: str) -> PersonalMaterialLiveSecretBoundary | None:
    provider = build_provider_readiness(provider_id)
    if provider is None:
        return None
    return PersonalMaterialLiveSecretBoundary(
        provider_id=provider.provider_id,
        key_env_names=provider.key_env_names,
        key_required=provider.key_required,
        key_loaded=provider.key_loaded,
        key_source=provider.key_source,
        warnings=[
            "Only key_loaded boolean metadata is returned.",
            "No key value, prefix, suffix, masked key, token value, or secret value is returned or stored.",
        ],
    )

