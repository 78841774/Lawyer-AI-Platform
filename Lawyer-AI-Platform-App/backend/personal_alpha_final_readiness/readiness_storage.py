import json
import re
from pathlib import Path
from typing import Any

RUNTIME_FINAL_READINESS_STORAGE_RELATIVE_PATH = "storage/runtime/personal_alpha_final_readiness"
REPO_ROOT = Path("/Users/wazhen/Lawyer-AI-Platform")


def store_final_readiness_snapshot(workspace_run_id: str, snapshot: dict[str, Any]) -> dict[str, Any]:
    safe_run_id = _safe_id(workspace_run_id, "workspace_run_missing")
    storage_dir = REPO_ROOT / RUNTIME_FINAL_READINESS_STORAGE_RELATIVE_PATH
    storage_dir.mkdir(parents=True, exist_ok=True)
    storage_file = storage_dir / f"{safe_run_id}.json"
    safe_snapshot = _safe_snapshot(safe_run_id, snapshot)
    storage_file.write_text(json.dumps(safe_snapshot, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return {
        "stored": True,
        "storage_path": f"{RUNTIME_FINAL_READINESS_STORAGE_RELATIVE_PATH}/{safe_run_id}.json",
        "mock_or_redacted_only": True,
        "raw_content_included": False,
        "final_legal_opinion_generated": False,
        "warnings": ["Final readiness snapshot stored in ignored runtime storage."],
    }


def _safe_snapshot(workspace_run_id: str, snapshot: dict[str, Any]) -> dict[str, Any]:
    return {
        "workspace_run_id": workspace_run_id,
        "case_id": str(snapshot.get("case_id", "")),
        "workspace_id": str(snapshot.get("workspace_id", "")),
        "workflow_mode": str(snapshot.get("workflow_mode", "")),
        "status": str(snapshot.get("status", "mock_final_readiness_ready")),
        "summary": snapshot.get("summary", {}),
        "stages": snapshot.get("stages", []),
        "blocked_stages": snapshot.get("blocked_stages", []),
        "safety_checklist": snapshot.get("safety_checklist", {}),
        "decision_metadata": snapshot.get("decision_metadata", {}),
        "mock_or_redacted_only": True,
        "raw_content_included": False,
        "final_legal_opinion_generated": False,
        "advisory_only": True,
        "warnings": snapshot.get("warnings", []),
        "created_at": str(snapshot.get("created_at", "")),
    }


def _safe_id(value: str, fallback: str) -> str:
    safe = re.sub(r"[^A-Za-z0-9_-]", "_", value or "")
    return safe[:100] or fallback
