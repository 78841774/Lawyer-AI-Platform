import json
from pathlib import Path
from typing import Any

from personal_alpha_case_os.export_package_safety import sanitize_export_token
from personal_alpha_case_os.runtime_guard import ensure_runtime_path, get_runtime_root

REPO_ROOT = Path("/Users/wazhen/Lawyer-AI-Platform")
RUNTIME_EXPORT_PACKAGE_STORAGE_RELATIVE_PATH = "personal_alpha_case_os/export_packages"
STORAGE_DIR = ensure_runtime_path(get_runtime_root() / RUNTIME_EXPORT_PACKAGE_STORAGE_RELATIVE_PATH)


def store_export_package_record(record: dict[str, Any], content: dict[str, Any] | str) -> dict[str, Any]:
    safe_record = _safe_record(record)
    STORAGE_DIR.mkdir(parents=True, exist_ok=True)
    package_id = safe_record["package_id"]
    content_file_name = safe_record["content_file_name"]
    record_file = STORAGE_DIR / f"record_{package_id}.json"
    content_file = STORAGE_DIR / content_file_name
    if safe_record["format"] == "markdown":
        content_file.write_text(str(content) + "\n", encoding="utf-8")
    else:
        content_file.write_text(json.dumps(content, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    record_file.write_text(json.dumps(safe_record, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return {
        "stored": True,
        "file_created": True,
        "file_path_redacted": True,
        "file_name": safe_record["file_name"],
        "storage_mode": "ignored_runtime_storage",
        "mock_or_redacted_only": True,
        "raw_content_included": False,
        "warnings": ["Export package stored in ignored runtime storage."],
    }


def list_export_package_records(case_id: str) -> list[dict[str, Any]]:
    if not STORAGE_DIR.exists():
        return []
    safe_case_id = sanitize_export_token(case_id, "")
    if not safe_case_id:
        return []
    records: list[dict[str, Any]] = []
    for file_path in sorted(STORAGE_DIR.glob("record_*.json")):
        parsed = _load_json(file_path)
        if isinstance(parsed, dict):
            record = _safe_record(parsed)
            if record.get("case_id") == safe_case_id:
                records.append(record)
    return sorted(records, key=lambda item: str(item.get("created_at", "")))


def get_export_package_record(case_id: str, package_id: str) -> dict[str, Any] | None:
    safe_case_id = sanitize_export_token(case_id, "")
    safe_package_id = sanitize_export_token(package_id, "")
    if not safe_case_id or not safe_package_id:
        return None
    record_file = STORAGE_DIR / f"record_{safe_package_id}.json"
    parsed = _load_json(record_file)
    if not isinstance(parsed, dict):
        return None
    record = _safe_record(parsed)
    if record.get("case_id") != safe_case_id:
        return None
    return record


def load_export_package_content(record: dict[str, Any]) -> dict[str, Any] | str | None:
    content_file_name = sanitize_export_token(str(record.get("content_file_name", "")), "")
    if not content_file_name:
        return None
    content_file = STORAGE_DIR / content_file_name
    try:
        text = content_file.read_text(encoding="utf-8")
    except OSError:
        return None
    if record.get("format") == "markdown":
        return text
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        return None


def public_record(record: dict[str, Any]) -> dict[str, Any]:
    safe = _safe_record(record)
    return {
        "package_id": safe["package_id"],
        "case_id": safe["case_id"],
        "format": safe["format"],
        "status": safe["status"],
        "reviewer_id": safe["reviewer_id"],
        "storage_mode": "ignored_runtime_storage",
        "file_path_redacted": True,
        "file_name": safe["file_name"],
        "mock_or_redacted_only": True,
        "raw_content_included": False,
        "created_at": safe["created_at"],
    }


def _safe_record(record: dict[str, Any]) -> dict[str, Any]:
    package_id = sanitize_export_token(str(record.get("package_id", "")), "case_os_export_package_missing")
    case_id = sanitize_export_token(str(record.get("case_id", "")), "")
    package_format = "markdown" if str(record.get("format", "")) == "markdown" else "json"
    content_suffix = "md" if package_format == "markdown" else "json"
    return {
        "package_id": package_id,
        "case_id": case_id,
        "format": package_format,
        "status": str(record.get("status", "export_package_created")),
        "reviewer_id": sanitize_export_token(str(record.get("reviewer_id", "local_demo_lawyer")), "local_demo_lawyer"),
        "file_name": str(record.get("file_name") or f"redacted_or_safe_metadata_filename_{content_suffix}"),
        "content_file_name": sanitize_export_token(str(record.get("content_file_name", "")), f"package_{package_id}_{content_suffix}"),
        "content_summary": record.get("content_summary", {}) if isinstance(record.get("content_summary", {}), dict) else {},
        "safety_check": record.get("safety_check", {}) if isinstance(record.get("safety_check", {}), dict) else {},
        "unsafe_items": record.get("unsafe_items", []) if isinstance(record.get("unsafe_items", []), list) else [],
        "manual_review_confirmed": bool(record.get("manual_review_confirmed", True)),
        "lawyer_review_confirmed": bool(record.get("lawyer_review_confirmed", True)),
        "metadata_only_confirmation": bool(record.get("metadata_only_confirmation", True)),
        "redacted_only_confirmation": bool(record.get("redacted_only_confirmation", True)),
        "no_raw_content_confirmation": bool(record.get("no_raw_content_confirmation", True)),
        "no_final_legal_opinion_confirmation": bool(record.get("no_final_legal_opinion_confirmation", True)),
        "no_final_report_generation_confirmation": bool(record.get("no_final_report_generation_confirmation", True)),
        "warnings": [str(item) for item in record.get("warnings", []) if isinstance(item, str)],
        "created_at": str(record.get("created_at", "")),
    }


def _load_json(file_path: Path) -> Any:
    try:
        return json.loads(file_path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return None
