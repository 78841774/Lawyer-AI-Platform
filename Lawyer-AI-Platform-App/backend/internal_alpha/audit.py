import json
from pathlib import Path
from typing import Any

REGISTRY_PATH = Path(__file__).resolve().parent / "registry.json"


def append_internal_alpha_audit_log(event: dict[str, Any]) -> dict[str, Any]:
    registry = _read_registry()
    safe_event = _sanitize_event(event)
    registry.setdefault("audit_logs", []).append(safe_event)
    REGISTRY_PATH.write_text(json.dumps(registry, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return safe_event


def list_internal_alpha_audit_logs() -> list[dict[str, Any]]:
    registry = _read_registry()
    logs = registry.get("audit_logs", [])
    return logs if isinstance(logs, list) else []


def _read_registry() -> dict[str, Any]:
    try:
        parsed = json.loads(REGISTRY_PATH.read_text(encoding="utf-8"))
    except (FileNotFoundError, json.JSONDecodeError):
        return _default_registry()
    return parsed if isinstance(parsed, dict) else _default_registry()


def _default_registry() -> dict[str, Any]:
    return {
        "schema_version": "1.0.0",
        "internal_alpha": {
            "enabled": True,
            "mode": "local_internal_alpha",
            "production_enabled": False,
            "team_mode_enabled": False,
            "real_case_processing_enabled": False,
            "real_case_processing_default": False,
            "workspace_runtime_auto_enable": False,
            "skill_aware_case_processing_auto_enable": False,
            "requires_manual_review": True,
            "local_only": True,
        },
        "readiness": {
            "sqlite_local_alpha_ready": True,
            "postgresql_ready_check": True,
            "alembic_ready_check": True,
            "secret_management_check": True,
            "backup_check": False,
            "logging_check": True,
            "permission_boundary_check": True,
        },
        "audit_logs": [],
    }


def _sanitize_event(event: dict[str, Any]) -> dict[str, Any]:
    allowed_keys = {
        "audit_log_id",
        "event_type",
        "case_id",
        "workspace_id",
        "alpha_dry_run_id",
        "local_sandbox_dry_run_id",
        "provider_mode",
        "ocr_mode",
        "legal_search_mode",
        "result",
        "warnings",
        "created_at",
    }
    safe_event = {key: event.get(key) for key in allowed_keys if key in event}
    safe_event["local_case_root_redacted"] = "<local_case_root_redacted>"
    return safe_event
