from personal_live_connection.provider_registry import build_provider
from personal_live_connection.schemas import LiveConnectionSecretBoundary


def build_secret_boundary(provider_id: str) -> LiveConnectionSecretBoundary | None:
    provider = build_provider(provider_id)
    if provider is None:
        return None
    return LiveConnectionSecretBoundary(
        provider_id=provider.provider_id,
        key_env_name=provider.key_env_name,
        key_loaded=provider.key_loaded,
        key_source=provider.key_source,
        key_required=provider.key_required,
        warnings=["Only key_loaded boolean metadata and key_env_name are returned. No key value is read or returned."],
    )

