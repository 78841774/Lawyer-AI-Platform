import json
import re
from pathlib import Path
from typing import Any

RUNTIME_FINAL_PACKET_STORAGE_RELATIVE_PATH = "storage/runtime/personal_alpha_final_packet/packets"
REPO_ROOT = Path("/Users/wazhen/Lawyer-AI-Platform")


def store_final_packet_record(record: dict[str, Any]) -> dict[str, Any]:
    safe_record = _safe_record(record)
    storage_dir = REPO_ROOT / RUNTIME_FINAL_PACKET_STORAGE_RELATIVE_PATH
    storage_dir.mkdir(parents=True, exist_ok=True)
    packet_id = _safe_id(str(safe_record.get("packet_id", "")), "final_review_packet_missing")
    storage_file = storage_dir / f"{packet_id}.json"
    storage_file.write_text(json.dumps(safe_record, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return {
        "stored": True,
        "storage_path": f"{RUNTIME_FINAL_PACKET_STORAGE_RELATIVE_PATH}/{packet_id}.json",
        "mock_or_redacted_only": True,
        "raw_content_included": False,
        "final_legal_opinion_generated": False,
        "final_report_generated": False,
        "warnings": ["Final review packet record stored in ignored runtime storage."],
    }


def list_final_packet_records() -> list[dict[str, Any]]:
    storage_dir = REPO_ROOT / RUNTIME_FINAL_PACKET_STORAGE_RELATIVE_PATH
    if not storage_dir.exists():
        return []
    records: list[dict[str, Any]] = []
    for file_path in sorted(storage_dir.glob("*.json")):
        parsed = _load_json(file_path)
        if isinstance(parsed, dict):
            records.append(_safe_record(parsed))
    return records


def get_final_packet_record(packet_id: str) -> dict[str, Any] | None:
    safe_packet_id = _safe_id(packet_id, "")
    if not safe_packet_id:
        return None
    storage_file = REPO_ROOT / RUNTIME_FINAL_PACKET_STORAGE_RELATIVE_PATH / f"{safe_packet_id}.json"
    parsed = _load_json(storage_file)
    if not isinstance(parsed, dict):
        return None
    return _safe_record(parsed)


def list_final_packet_records_for_run(workspace_run_id: str) -> list[dict[str, Any]]:
    return [
        record
        for record in list_final_packet_records()
        if str(record.get("workspace_run_id", "")) == workspace_run_id
    ]


def _load_json(file_path: Path) -> Any:
    try:
        return json.loads(file_path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return None


def _safe_record(record: dict[str, Any]) -> dict[str, Any]:
    packet = record.get("packet", {}) if isinstance(record.get("packet", {}), dict) else {}
    return {
        "packet_id": _safe_id(str(record.get("packet_id", "")), "final_review_packet_missing"),
        "workspace_run_id": _safe_id(str(record.get("workspace_run_id", "")), "workspace_run_missing"),
        "status": str(record.get("status", "packet_created")),
        "can_proceed_to_controlled_final_review": bool(record.get("can_proceed_to_controlled_final_review", True)),
        "packet": _safe_packet(packet),
        "reviewer_id": _safe_id(str(record.get("reviewer_id", "local_demo_reviewer")), "local_demo_reviewer"),
        "safety_checklist": record.get("safety_checklist", {}) if isinstance(record.get("safety_checklist", {}), dict) else {},
        "mock_or_redacted_only": True,
        "raw_content_included": False,
        "final_legal_opinion_generated": False,
        "final_report_generated": False,
        "manual_review_confirmed": bool(record.get("manual_review_confirmed", True)),
        "metadata_only_confirmation": bool(record.get("metadata_only_confirmation", True)),
        "no_final_legal_opinion_confirmation": bool(record.get("no_final_legal_opinion_confirmation", True)),
        "no_final_report_generation_confirmation": bool(record.get("no_final_report_generation_confirmation", True)),
        "warnings": [str(item) for item in record.get("warnings", []) if isinstance(item, str)],
        "created_at": str(record.get("created_at", "")),
    }


def _safe_packet(packet: dict[str, Any]) -> dict[str, Any]:
    return {
        "title": str(packet.get("title", "Personal Alpha Controlled Final Review Packet")),
        "case_id": _safe_id(str(packet.get("case_id", "")), ""),
        "workspace_id": _safe_id(str(packet.get("workspace_id", "")), ""),
        "workflow_mode": str(packet.get("workflow_mode", "")),
        "packet_sections": packet.get("packet_sections", []) if isinstance(packet.get("packet_sections", []), list) else [],
        "mock_or_redacted_only": True,
        "raw_content_included": False,
        "final_legal_opinion_generated": False,
        "final_report_generated": False,
    }


def _safe_id(value: str, fallback: str) -> str:
    safe = re.sub(r"[^A-Za-z0-9_-]", "_", value or "")
    return safe[:120] or fallback
