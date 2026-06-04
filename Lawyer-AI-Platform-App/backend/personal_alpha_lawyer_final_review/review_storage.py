import json
import re
from pathlib import Path
from typing import Any

RUNTIME_LAWYER_FINAL_REVIEW_STORAGE_RELATIVE_PATH = "storage/runtime/personal_alpha_lawyer_final_review/actions"
REPO_ROOT = Path("/Users/wazhen/Lawyer-AI-Platform")


def store_lawyer_final_review_action(record: dict[str, Any]) -> dict[str, Any]:
    safe_record = _safe_record(record)
    storage_dir = REPO_ROOT / RUNTIME_LAWYER_FINAL_REVIEW_STORAGE_RELATIVE_PATH
    storage_dir.mkdir(parents=True, exist_ok=True)
    action_id = _safe_id(str(safe_record.get("action_id", "")), "lawyer_final_review_action_missing")
    storage_file = storage_dir / f"{action_id}.json"
    storage_file.write_text(json.dumps(safe_record, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return {
        "stored": True,
        "storage_path": f"{RUNTIME_LAWYER_FINAL_REVIEW_STORAGE_RELATIVE_PATH}/{action_id}.json",
        "mock_or_redacted_only": True,
        "raw_content_included": False,
        "final_legal_opinion_generated": False,
        "final_report_generated": False,
        "warnings": ["Lawyer final review action stored in ignored runtime storage."],
    }


def list_lawyer_final_review_actions(packet_id: str) -> list[dict[str, Any]]:
    return [
        record
        for record in list_all_lawyer_final_review_actions()
        if str(record.get("packet_id", "")) == packet_id
    ]


def list_all_lawyer_final_review_actions() -> list[dict[str, Any]]:
    storage_dir = REPO_ROOT / RUNTIME_LAWYER_FINAL_REVIEW_STORAGE_RELATIVE_PATH
    if not storage_dir.exists():
        return []
    records: list[dict[str, Any]] = []
    for file_path in sorted(storage_dir.glob("*.json")):
        parsed = _load_json(file_path)
        if isinstance(parsed, dict):
            records.append(_safe_record(parsed))
    return records


def get_lawyer_final_review_action(action_id: str) -> dict[str, Any] | None:
    safe_action_id = _safe_id(action_id, "")
    if not safe_action_id:
        return None
    storage_file = REPO_ROOT / RUNTIME_LAWYER_FINAL_REVIEW_STORAGE_RELATIVE_PATH / f"{safe_action_id}.json"
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
        "action_id": _safe_id(str(record.get("action_id", "")), "lawyer_final_review_action_missing"),
        "packet_id": _safe_id(str(record.get("packet_id", "")), "final_review_packet_missing"),
        "workspace_run_id": _safe_id(str(record.get("workspace_run_id", "")), "workspace_run_missing"),
        "action": str(record.get("action", "")),
        "reviewer_id": _safe_id(str(record.get("reviewer_id", "local_demo_lawyer")), "local_demo_lawyer"),
        "reason": str(record.get("reason", "")),
        "status": str(record.get("status", "lawyer_final_review_action_recorded")),
        "ready_for_controlled_final_lock": bool(record.get("ready_for_controlled_final_lock", False)),
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


def _safe_id(value: str, fallback: str) -> str:
    safe = re.sub(r"[^A-Za-z0-9_-]", "_", value or "")
    return safe[:120] or fallback
