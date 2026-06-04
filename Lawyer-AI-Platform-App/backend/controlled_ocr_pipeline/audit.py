import json
from pathlib import Path
from typing import Any

REGISTRY_PATH = Path(__file__).resolve().parent / "registry.json"


def append_controlled_ocr_audit_log(event: dict[str, Any]) -> dict[str, Any]:
    registry = _read_registry()
    safe_event = _sanitize_event(event)
    registry.setdefault("audit_logs", []).append(safe_event)
    REGISTRY_PATH.write_text(json.dumps(registry, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return safe_event


def list_controlled_ocr_audit_logs() -> list[dict[str, Any]]:
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
        "ocr_preview_id",
        "material_id",
        "filename_redacted",
        "result",
        "warnings",
        "created_at",
    }
    return {key: event.get(key) for key in allowed_keys if key in event}


def _default_registry() -> dict[str, Any]:
    return {
        "schema_version": "1.0.0",
        "controlled_ocr_pipeline": {
            "enabled": True,
            "mode": "local_only_controlled_ocr",
            "production_enabled": False,
            "ocr_live_enabled": False,
            "ocr_live_default": False,
            "mock_ocr_enabled": True,
            "requires_explicit_ocr_confirmation": True,
            "requires_manual_review": True,
            "allowed_file_extensions": [".pdf", ".png", ".jpg", ".jpeg", ".txt"],
            "max_file_size_bytes": 5000000,
            "read_pdf_binary_enabled": False,
            "read_image_binary_enabled": False,
            "extract_real_ocr_text_enabled": False,
            "store_raw_ocr_text_in_git": False,
            "store_redacted_ocr_preview_in_git": False,
            "runtime_storage_enabled": True,
            "runtime_storage_path": "storage/runtime/controlled_ocr_previews",
            "source_trace_enabled": True,
            "final_legal_opinion_enabled": False,
        },
        "audit_logs": [],
    }
