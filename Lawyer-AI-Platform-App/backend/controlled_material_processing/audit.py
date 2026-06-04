import json
from pathlib import Path
from typing import Any

REGISTRY_PATH = Path(__file__).resolve().parent / "registry.json"


def append_controlled_material_audit_log(event: dict[str, Any]) -> dict[str, Any]:
    registry = _read_registry()
    safe_event = _sanitize_event(event)
    registry.setdefault("audit_logs", []).append(safe_event)
    REGISTRY_PATH.write_text(json.dumps(registry, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return safe_event


def list_controlled_material_audit_logs() -> list[dict[str, Any]]:
    registry = _read_registry()
    logs = registry.get("audit_logs", [])
    return logs if isinstance(logs, list) else []


def _read_registry() -> dict[str, Any]:
    try:
        parsed = json.loads(REGISTRY_PATH.read_text(encoding="utf-8"))
    except (FileNotFoundError, json.JSONDecodeError):
        return _default_registry()
    return parsed if isinstance(parsed, dict) else _default_registry()


def _sanitize_event(event: dict[str, Any]) -> dict[str, Any]:
    allowed_keys = {
        "audit_log_id",
        "event_type",
        "case_id",
        "workspace_id",
        "controlled_read_id",
        "material_id",
        "filename_redacted",
        "result",
        "warnings",
        "created_at",
    }
    safe_event = {key: event.get(key) for key in allowed_keys if key in event}
    safe_event["local_case_root_redacted"] = "<local_case_root_redacted>"
    return safe_event


def _default_registry() -> dict[str, Any]:
    return {
        "schema_version": "1.0.0",
        "controlled_material_processing": {
            "enabled": True,
            "mode": "local_only_controlled",
            "production_enabled": False,
            "real_material_reading_enabled": False,
            "real_material_reading_default": False,
            "requires_explicit_read_confirmation": True,
            "requires_manual_review": True,
            "ocr_live_enabled": False,
            "llm_live_enabled": False,
            "legal_search_live_enabled": False,
            "deepseek_live_enabled": False,
            "store_extracted_text_in_git": False,
            "store_material_content_in_git": False,
            "source_trace_enabled": True,
            "report_draft_enabled": True,
            "final_legal_opinion_enabled": False,
        },
        "audit_logs": [],
    }
