import json
from pathlib import Path
from typing import Any

REGISTRY_PATH = Path(__file__).resolve().parent / "registry.json"
RUNTIME_AUDIT_PATH = Path(__file__).resolve().parents[1] / "storage" / "runtime" / "personal_alpha_workspace" / "audit_logs.json"
SENSITIVE_PATTERNS = (
    "/",
    "\\",
    ".env",
    "local.db",
    "api_key",
    "apikey",
    "secret",
    "token",
    "Users/",
)


def append_personal_alpha_workspace_audit_log(event: dict[str, Any]) -> dict[str, Any]:
    safe_event = _sanitize_event(event)
    logs = _read_runtime_audit_logs()
    logs.append(safe_event)
    RUNTIME_AUDIT_PATH.parent.mkdir(parents=True, exist_ok=True)
    RUNTIME_AUDIT_PATH.write_text(json.dumps(logs, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return safe_event


def list_personal_alpha_workspace_audit_logs() -> list[dict[str, Any]]:
    logs = _read_runtime_audit_logs()
    if logs:
        return logs
    registry = _read_registry()
    registry_logs = registry.get("audit_logs", [])
    return registry_logs if isinstance(registry_logs, list) else []


def _read_registry() -> dict[str, Any]:
    try:
        parsed = json.loads(REGISTRY_PATH.read_text(encoding="utf-8"))
    except (FileNotFoundError, json.JSONDecodeError):
        return {"schema_version": "1.0.0", "personal_alpha_workspace": {}, "audit_logs": []}
    return parsed if isinstance(parsed, dict) else {"schema_version": "1.0.0", "personal_alpha_workspace": {}, "audit_logs": []}


def _read_runtime_audit_logs() -> list[dict[str, Any]]:
    try:
        parsed = json.loads(RUNTIME_AUDIT_PATH.read_text(encoding="utf-8"))
    except (FileNotFoundError, json.JSONDecodeError):
        return []
    return parsed if isinstance(parsed, list) else []


def _sanitize_event(event: dict[str, Any]) -> dict[str, Any]:
    allowed_keys = {
        "audit_log_id",
        "event_type",
        "case_id",
        "workspace_id",
        "workspace_run_id",
        "workflow_mode",
        "result",
        "warnings",
        "created_at",
    }
    return {key: _sanitize_value(event.get(key)) for key in allowed_keys if key in event}


def _sanitize_value(value: Any) -> Any:
    if isinstance(value, str):
        lowered = value.lower()
        if any(pattern.lower() in lowered for pattern in SENSITIVE_PATTERNS):
            return "[redacted]"
        return value
    if isinstance(value, list):
        return [_sanitize_value(item) for item in value]
    if isinstance(value, dict):
        return {str(key): _sanitize_value(item) for key, item in value.items()}
    return value
