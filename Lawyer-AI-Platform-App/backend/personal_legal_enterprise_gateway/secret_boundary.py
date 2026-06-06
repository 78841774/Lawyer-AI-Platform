from personal_legal_enterprise_gateway.provider_registry import build_provider
from personal_legal_enterprise_gateway.schemas import SecretBoundaryStatus


def build_secret_boundary(provider_id: str) -> SecretBoundaryStatus | None:
    provider = build_provider(provider_id)
    if provider is None:
        return None
    return SecretBoundaryStatus(
        provider_id=provider.provider_id,
        key_env_names=provider.key_env_names,
        requires_api_key=provider.requires_api_key,
        key_loaded=provider.key_loaded,
        key_source=provider.key_source,
        warnings=["Only key_loaded boolean metadata is returned; no key value, prefix, suffix, or masked key is returned."],
    )

