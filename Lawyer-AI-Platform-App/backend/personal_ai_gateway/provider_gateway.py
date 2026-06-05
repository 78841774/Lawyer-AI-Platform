from personal_ai_gateway.provider_registry import get_provider


def validate_provider_for_mock_run(provider_id: str) -> list[str]:
    provider = get_provider(provider_id)
    if provider is None:
        return ["provider_id is not registered"]
    if not provider.mock_supported:
        return ["provider does not support mock mode"]
    if provider.live_enabled:
        return ["provider live mode must remain disabled in v7.1"]
    return []
