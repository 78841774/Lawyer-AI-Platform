import json
import re
from pathlib import Path
from typing import Any

RUNTIME_FINAL_GATE_DECISION_STORAGE_RELATIVE_PATH = "storage/runtime/personal_alpha_final_gate/decisions"
REPO_ROOT = Path("/Users/wazhen/Lawyer-AI-Platform")


def append_final_gate_decision(workspace_run_id: str, record: dict[str, Any]) -> dict[str, Any]:
    safe_run_id = _safe_id(workspace_run_id, "workspace_run_missing")
    storage_file = _decision_storage_file(safe_run_id)
    storage_file.parent.mkdir(parents=True, exist_ok=True)
    decisions = _read_decisions_from_file(storage_file)
    safe_record = _safe_decision_record(record, safe_run_id)
    decisions.append(safe_record)
    storage_file.write_text(json.dumps({"workspace_run_id": safe_run_id, "decisions": decisions}, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return safe_record


def list_final_gate_decisions(workspace_run_id: str) -> list[dict[str, Any]]:
    safe_run_id = _safe_id(workspace_run_id, "workspace_run_missing")
    return _read_decisions_from_file(_decision_storage_file(safe_run_id))


def _decision_storage_file(workspace_run_id: str) -> Path:
    return REPO_ROOT / RUNTIME_FINAL_GATE_DECISION_STORAGE_RELATIVE_PATH / f"{workspace_run_id}.json"


def _read_decisions_from_file(storage_file: Path) -> list[dict[str, Any]]:
    if not storage_file.exists():
        return []
    try:
        parsed = json.loads(storage_file.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return []
    decisions = parsed.get("decisions", []) if isinstance(parsed, dict) else []
    return [item for item in decisions if isinstance(item, dict)]


def _safe_decision_record(record: dict[str, Any], workspace_run_id: str) -> dict[str, Any]:
    allowed_keys = {
        "gate_decision_id",
        "workspace_run_id",
        "decision",
        "reviewer_id",
        "reason",
        "status",
        "can_proceed_to_controlled_final_review",
        "mock_or_redacted_only",
        "raw_content_included",
        "final_legal_opinion_generated",
        "final_report_generated",
        "manual_review_confirmed",
        "metadata_only_confirmation",
        "no_final_legal_opinion_confirmation",
        "warnings",
        "created_at",
    }
    safe = {key: record.get(key) for key in allowed_keys if key in record}
    safe["workspace_run_id"] = workspace_run_id
    safe["mock_or_redacted_only"] = True
    safe["raw_content_included"] = False
    safe["final_legal_opinion_generated"] = False
    safe["final_report_generated"] = False
    return safe


def _safe_id(value: str, fallback: str) -> str:
    safe = re.sub(r"[^A-Za-z0-9_-]", "_", value or "")
    return safe[:100] or fallback
