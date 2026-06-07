import json
import os
from pathlib import Path
from typing import Any

from personal_skill_studio.training_artifacts.storage import RUNTIME_ROOT


DEFAULT_PROVIDER_SECRET_FILE = RUNTIME_ROOT / "provider_secrets.local.json"


def credential_loaded_for_alias(alias: str) -> bool:
    return bool(os.environ.get(alias)) or bool(_credential_from_file(alias))


def credential_value_for_alias(alias: str) -> str | None:
    return os.environ.get(alias) or _credential_from_file(alias)


def adapter_url_for_keys(keys: list[str]) -> str | None:
    config = _load_config()
    adapters = config.get("adapters", {}) if isinstance(config.get("adapters"), dict) else {}
    for key in keys:
        value = os.environ.get(key) or adapters.get(key) or config.get(key)
        if isinstance(value, str) and value.strip():
            return value.strip()
    return None


def provider_secret_file_configured() -> bool:
    return _secret_file_path().exists()


def _credential_from_file(alias: str) -> str | None:
    config = _load_config()
    credentials = config.get("credentials", {}) if isinstance(config.get("credentials"), dict) else {}
    value = credentials.get(alias) or config.get(alias)
    return value.strip() if isinstance(value, str) and value.strip() else None


def _load_config() -> dict[str, Any]:
    path = _secret_file_path()
    if not path.exists():
        return {}
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return {}
    return payload if isinstance(payload, dict) else {}


def _secret_file_path() -> Path:
    configured = os.environ.get("LAWYER_AI_PROVIDER_SECRETS_FILE")
    return Path(configured).expanduser() if configured else DEFAULT_PROVIDER_SECRET_FILE
