import os

from personal_ai_gateway.schemas import (
    PersonalAILiveGatewayStatus,
    PersonalAILiveProviderConfig,
    PersonalAILiveProviderConfigList,
)


PROVIDER_CONFIGS = [
    {
        "provider_id": "openai",
        "display_name": "OpenAI",
        "provider_type": "ai_model",
        "key_env": "OPENAI_API_KEY",
        "model_options": ["gpt-4.1-mini", "gpt-4.1", "gpt-5-mini"],
        "timeout_seconds": 45,
    },
    {
        "provider_id": "deepseek",
        "display_name": "DeepSeek",
        "provider_type": "ai_model",
        "key_env": "DEEPSEEK_API_KEY",
        "model_options": ["deepseek-chat", "deepseek-reasoner"],
        "timeout_seconds": 45,
    },
    {
        "provider_id": "local_model_placeholder",
        "display_name": "Local Model Placeholder",
        "provider_type": "local_model",
        "key_env": None,
        "model_options": ["local-placeholder"],
        "timeout_seconds": 30,
    },
]


def live_mode_enabled() -> bool:
    return _env_flag("AI_LIVE_MODE_ENABLED", default=False)


def list_live_provider_configs() -> dict:
    providers = [_build_provider_config(definition) for definition in PROVIDER_CONFIGS]
    return PersonalAILiveProviderConfigList(
        providers=providers,
        provider_count=len(providers),
        live_provider_count=sum(1 for provider in providers if provider.live_enabled),
        key_loaded_count=sum(1 for provider in providers if provider.key_loaded),
        live_mode_enabled=live_mode_enabled(),
        warnings=[
            "live provider disabled by default.",
            "API key state is returned only as key_loaded true/false; key values are never returned.",
        ],
    ).model_dump()


def get_live_provider_config(provider_id: str) -> PersonalAILiveProviderConfig | None:
    for payload in list_live_provider_configs()["providers"]:
        if payload["provider_id"] == provider_id:
            return PersonalAILiveProviderConfig(**payload)
    return None


def build_live_gateway_status() -> dict:
    providers = [PersonalAILiveProviderConfig(**payload) for payload in list_live_provider_configs()["providers"]]
    return PersonalAILiveGatewayStatus(
        live_mode_enabled=live_mode_enabled(),
        provider_count=len(providers),
        live_provider_count=sum(1 for provider in providers if provider.live_enabled),
        key_loaded_count=sum(1 for provider in providers if provider.key_loaded),
        warnings=[
            "v7.12 AI live gateway is provider-gated.",
            "live provider disabled by default.",
            "Dry-run is available before any live attempt.",
        ],
    ).model_dump()


def _build_provider_config(definition: dict) -> PersonalAILiveProviderConfig:
    key_env = definition.get("key_env")
    key_required = bool(key_env)
    key_loaded = bool(os.environ.get(str(key_env))) if key_env else False
    live_enabled = (
        live_mode_enabled()
        and _env_flag(f"AI_LIVE_PROVIDER_{definition['provider_id'].upper()}_ENABLED", default=False)
        and (key_loaded or not key_required)
    )
    key_source = "env" if key_loaded else "not_required" if not key_required else "unavailable"
    return PersonalAILiveProviderConfig(
        provider_id=definition["provider_id"],
        display_name=definition["display_name"],
        provider_type=definition["provider_type"],
        live_supported=True,
        live_enabled=live_enabled,
        key_required=key_required,
        key_loaded=key_loaded,
        key_source=key_source,
        model_options=definition["model_options"],
        timeout_seconds=definition["timeout_seconds"],
        safety_notes=[
            "API key is read only by backend environment lookup.",
            "Frontend receives key_loaded only, never the key value.",
            "Live call requires explicit confirmation and remains draft-only.",
        ],
    )


def _env_flag(name: str, default: bool = False) -> bool:
    value = os.environ.get(name)
    if value is None:
        return default
    return value.strip().lower() in {"1", "true", "yes", "on"}
