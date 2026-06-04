import json
from pathlib import Path
from typing import Any

REGISTRY_PATH = Path(__file__).resolve().parent / "registry.json"


def append_personal_alpha_audit_log(event: dict[str, Any]) -> dict[str, Any]:
    registry = _read_registry()
    safe_event = _sanitize_event(event)
    registry.setdefault("audit_logs", []).append(safe_event)
    REGISTRY_PATH.write_text(json.dumps(registry, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return safe_event


def list_personal_alpha_audit_logs() -> list[dict[str, Any]]:
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
        "personal_alpha": {
            "enabled": True,
            "mode": "personal_local_alpha",
            "production_enabled": False,
            "team_mode_enabled": False,
            "real_case_processing_enabled": False,
            "real_case_processing_default": False,
            "material_content_reading_enabled": False,
            "ocr_live_enabled": False,
            "legal_search_live_enabled": False,
            "llm_live_enabled": False,
            "deepseek_live_enabled": False,
            "requires_manual_review": True,
            "local_only": True,
            "dry_run_only": True,
        },
        "allowed_external_roots": [
            "~/Lawyer-AI-Local-Cases",
            "~/AIHome-Law-Local-Sandbox",
        ],
        "blocked_git_paths": [
            "sandbox_cases",
            "real_cases",
            "case_workspaces",
            "Lawyer-AI-Local-Cases",
            "AIHome-Law-Local-Sandbox",
            "storage/runtime",
            "local.db",
            ".env",
        ],
        "audit_logs": [],
    }


def _sanitize_event(event: dict[str, Any]) -> dict[str, Any]:
    allowed_keys = {
        "audit_log_id",
        "event_type",
        "case_id",
        "workspace_id",
        "personal_alpha_dry_run_id",
        "result",
        "warnings",
        "created_at",
    }
    safe_event = {key: event.get(key) for key in allowed_keys if key in event}
    safe_event["local_case_root_redacted"] = "<local_case_root_redacted>"
    return safe_event
