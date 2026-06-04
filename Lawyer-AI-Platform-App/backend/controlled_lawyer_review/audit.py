import json
from pathlib import Path
from typing import Any

REGISTRY_PATH = Path(__file__).resolve().parent / "registry.json"


def append_controlled_lawyer_review_audit_log(event: dict[str, Any]) -> dict[str, Any]:
    registry = _read_registry()
    safe_event = _sanitize_event(event)
    registry.setdefault("audit_logs", []).append(safe_event)
    REGISTRY_PATH.write_text(json.dumps(registry, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return safe_event


def list_controlled_lawyer_review_audit_logs() -> list[dict[str, Any]]:
    registry = _read_registry()
    logs = registry.get("audit_logs", [])
    return logs if isinstance(logs, list) else []


def _read_registry() -> dict[str, Any]:
    try:
        parsed = json.loads(REGISTRY_PATH.read_text(encoding="utf-8"))
    except (FileNotFoundError, json.JSONDecodeError):
        return {"schema_version": "1.0.0", "controlled_lawyer_review": {}, "audit_logs": []}
    return parsed if isinstance(parsed, dict) else {"schema_version": "1.0.0", "controlled_lawyer_review": {}, "audit_logs": []}


def _sanitize_event(event: dict[str, Any]) -> dict[str, Any]:
    allowed_keys = {
        "audit_log_id",
        "event_type",
        "review_id",
        "draft_id",
        "case_id",
        "workspace_id",
        "action",
        "result",
        "warnings",
        "created_at",
    }
    return {key: event.get(key) for key in allowed_keys if key in event}

