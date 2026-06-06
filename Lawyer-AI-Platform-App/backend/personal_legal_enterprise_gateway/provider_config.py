import os


def key_loaded_for(env_names: list[str]) -> bool:
    return any(name in os.environ for name in env_names)


def key_source_for(requires_api_key: bool, env_names: list[str]) -> str:
    if not requires_api_key:
        return "not_required"
    return "env" if key_loaded_for(env_names) else "unavailable"


def global_live_enabled() -> bool:
    return os.environ.get("LEGAL_ENTERPRISE_LIVE_MODE_ENABLED", "").strip().lower() in {"1", "true", "yes", "on"}


def provider_live_enabled(provider_id: str) -> bool:
    return global_live_enabled() and os.environ.get(f"LEGAL_ENTERPRISE_PROVIDER_{provider_id.upper()}_ENABLED", "").strip().lower() in {
        "1",
        "true",
        "yes",
        "on",
    }

