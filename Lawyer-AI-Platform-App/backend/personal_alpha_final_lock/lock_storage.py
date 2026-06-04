import json
import re
from pathlib import Path
from typing import Any

RUNTIME_FINAL_LOCK_STORAGE_RELATIVE_PATH = "storage/runtime/personal_alpha_final_lock/locks"
REPO_ROOT = Path("/Users/wazhen/Lawyer-AI-Platform")


def store_final_lock_record(record: dict[str, Any]) -> dict[str, Any]:
    safe_record = _safe_record(record)
    storage_dir = REPO_ROOT / RUNTIME_FINAL_LOCK_STORAGE_RELATIVE_PATH
    storage_dir.mkdir(parents=True, exist_ok=True)
    lock_id = _safe_id(str(safe_record.get("lock_id", "")), "personal_alpha_final_lock_missing")
    storage_file = storage_dir / f"{lock_id}.json"
    storage_file.write_text(json.dumps(safe_record, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return {
        "stored": True,
        "storage_path": f"{RUNTIME_FINAL_LOCK_STORAGE_RELATIVE_PATH}/{lock_id}.json",
        "mock_or_redacted_only": True,
        "raw_content_included": False,
        "final_legal_opinion_generated": False,
        "final_report_generated": False,
        "warnings": ["Final lock record stored in ignored runtime storage."],
    }


def list_final_lock_records() -> list[dict[str, Any]]:
    storage_dir = REPO_ROOT / RUNTIME_FINAL_LOCK_STORAGE_RELATIVE_PATH
    if not storage_dir.exists():
        return []
    records: list[dict[str, Any]] = []
    for file_path in sorted(storage_dir.glob("*.json")):
        parsed = _load_json(file_path)
        if isinstance(parsed, dict):
            records.append(_safe_record(parsed))
    return records


def list_final_lock_records_for_packet(packet_id: str) -> list[dict[str, Any]]:
    return [
        record
        for record in list_final_lock_records()
        if str(record.get("packet_id", "")) == packet_id
    ]


def get_final_lock_record(lock_id: str) -> dict[str, Any] | None:
    safe_lock_id = _safe_id(lock_id, "")
    if not safe_lock_id:
        return None
    storage_file = REPO_ROOT / RUNTIME_FINAL_LOCK_STORAGE_RELATIVE_PATH / f"{safe_lock_id}.json"
    parsed = _load_json(storage_file)
    if not isinstance(parsed, dict):
        return None
    return _safe_record(parsed)


def _load_json(file_path: Path) -> Any:
    try:
        return json.loads(file_path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return None


def _safe_record(record: dict[str, Any]) -> dict[str, Any]:
    return {
        "lock_id": _safe_id(str(record.get("lock_id", "")), "personal_alpha_final_lock_missing"),
        "packet_id": _safe_id(str(record.get("packet_id", "")), "final_review_packet_missing"),
        "workspace_run_id": _safe_id(str(record.get("workspace_run_id", "")), "workspace_run_missing"),
        "status": str(record.get("status", "final_lock_created")),
        "reviewer_id": _safe_id(str(record.get("reviewer_id", "local_demo_lawyer")), "local_demo_lawyer"),
        "lock_record": _safe_lock_record(record.get("lock_record", {})),
        "safety_checklist": record.get("safety_checklist", {}) if isinstance(record.get("safety_checklist", {}), dict) else {},
        "mock_or_redacted_only": True,
        "raw_content_included": False,
        "final_legal_opinion_generated": False,
        "final_report_generated": False,
        "manual_review_confirmed": bool(record.get("manual_review_confirmed", True)),
        "lawyer_review_confirmed": bool(record.get("lawyer_review_confirmed", True)),
        "metadata_only_confirmation": bool(record.get("metadata_only_confirmation", True)),
        "no_final_legal_opinion_confirmation": bool(record.get("no_final_legal_opinion_confirmation", True)),
        "no_final_report_generation_confirmation": bool(record.get("no_final_report_generation_confirmation", True)),
        "warnings": [str(item) for item in record.get("warnings", []) if isinstance(item, str)],
        "created_at": str(record.get("created_at", "")),
    }


def _safe_lock_record(value: Any) -> dict[str, Any]:
    if not isinstance(value, dict):
        return {}
    locked_metadata = value.get("locked_metadata", {}) if isinstance(value.get("locked_metadata", {}), dict) else {}
    return {
        "lock_id": _safe_id(str(value.get("lock_id", "")), "personal_alpha_final_lock_missing"),
        "packet_id": _safe_id(str(value.get("packet_id", "")), "final_review_packet_missing"),
        "workspace_run_id": _safe_id(str(value.get("workspace_run_id", "")), "workspace_run_missing"),
        "locked_metadata": {
            "packet_id": _safe_id(str(locked_metadata.get("packet_id", "")), "final_review_packet_missing"),
            "latest_lawyer_review_action": str(locked_metadata.get("latest_lawyer_review_action", "")),
            "safety_checklist": locked_metadata.get("safety_checklist", {}) if isinstance(locked_metadata.get("safety_checklist", {}), dict) else {},
            "lock_type": "metadata_only_personal_alpha_final_lock",
        },
        "mock_or_redacted_only": True,
        "raw_content_included": False,
        "final_legal_opinion_generated": False,
        "final_report_generated": False,
    }


def _safe_id(value: str, fallback: str) -> str:
    safe = re.sub(r"[^A-Za-z0-9_-]", "_", value or "")
    return safe[:120] or fallback
