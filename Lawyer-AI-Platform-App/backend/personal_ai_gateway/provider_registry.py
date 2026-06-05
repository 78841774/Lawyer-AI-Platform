from personal_ai_gateway.schemas import PersonalAIProvider, PersonalAIProviderList


PROVIDER_DEFINITIONS = [
    {
        "provider_id": "openai_provider",
        "label": "OpenAI / GPT Provider",
        "category": "ai_model",
        "requires_api_key": True,
    },
    {
        "provider_id": "deepseek_provider",
        "label": "DeepSeek Provider",
        "category": "ai_model",
        "requires_api_key": True,
    },
    {
        "provider_id": "local_model_provider",
        "label": "Local Model Provider",
        "category": "ai_model",
        "requires_api_key": False,
    },
]


def list_providers() -> dict:
    providers = [
        PersonalAIProvider(
            warnings=["Provider metadata only. v7.1 does not read API keys or execute live provider calls."],
            **definition,
        )
        for definition in PROVIDER_DEFINITIONS
    ]
    return PersonalAIProviderList(
        providers=providers,
        provider_count=len(providers),
        configured_provider_count=sum(1 for provider in providers if provider.configured),
        live_provider_count=sum(1 for provider in providers if provider.live_enabled),
        warnings=["AI providers are registered as mock-first placeholders. Provider secrets are never visible."],
    ).model_dump()


def get_provider(provider_id: str) -> PersonalAIProvider | None:
    for provider in list_providers()["providers"]:
        if provider.get("provider_id") == provider_id:
            return PersonalAIProvider(**provider)
    return None
