import os


def key_loaded_for_env_names(key_env_names: list[str]) -> bool:
    return any(name in os.environ for name in key_env_names)


def key_source_for_env_names(requires_api_key: bool, key_env_names: list[str]) -> str:
    if not requires_api_key:
        return "not_required"
    return "env" if key_loaded_for_env_names(key_env_names) else "unavailable"

