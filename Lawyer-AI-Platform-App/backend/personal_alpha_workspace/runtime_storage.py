import json
import re
from pathlib import Path
from typing import Any

from personal_alpha_workspace.schemas import RuntimePersonalAlphaWorkspaceStorageResult, utc_now

RUNTIME_WORKSPACE_STORAGE_RELATIVE_PATH = "storage/runtime/personal_alpha_workspace"


def store_personal_alpha_workspace_run(workspace_run_id: str, record: dict[str, Any]) -> dict[str, Any]:
    safe_id = _safe_workspace_run_id(workspace_run_id)
    storage_dir = _runtime_storage_dir()
    storage_dir.mkdir(parents=True, exist_ok=True)
    storage_file = storage_dir / f"{safe_id}.json"
    storage_file.write_text(
        json.dumps(
            {
                "workspace_run_id": safe_id,
                "case_id": record.get("case_id", ""),
                "workspace_id": record.get("workspace_id", ""),
                "workflow_mode": record.get("workflow_mode", ""),
                "stage_statuses": record.get("stage_statuses", []),
                "workspace_snapshot": record.get("workspace_snapshot", {}),
                "unified_audit_timeline": record.get("unified_audit_timeline", []),
                "source_refs": record.get("source_refs", []),
                "created_at": record.get("created_at", utc_now()),
                "mock_or_redacted_only": True,
            },
            ensure_ascii=False,
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )
    return RuntimePersonalAlphaWorkspaceStorageResult(
        stored=True,
        storage_path=f"{RUNTIME_WORKSPACE_STORAGE_RELATIVE_PATH}/{safe_id}.json",
        raw_material_text_stored=False,
        raw_ocr_text_stored=False,
        raw_legal_search_results_stored=False,
        workspace_snapshot_stored_in_git=False,
        mock_or_redacted_only=True,
        warnings=[
            "Personal alpha workspace snapshot stored in ignored runtime storage.",
            "Raw material text, raw OCR text, and raw legal search results were not stored.",
        ],
    ).model_dump()


def load_personal_alpha_workspace_run_record(workspace_run_id: str) -> dict[str, Any]:
    safe_id = _safe_workspace_run_id(workspace_run_id)
    storage_file = _runtime_storage_dir() / f"{safe_id}.json"
    if not storage_file.exists():
        return {
            "workspace_run_id": safe_id,
            "stage_statuses": [],
            "workspace_snapshot": {},
            "unified_audit_timeline": [],
            "source_refs": [],
            "created_at": utc_now(),
            "warnings": ["Personal alpha workspace run record was not found."],
        }
    parsed = json.loads(storage_file.read_text(encoding="utf-8"))
    parsed["warnings"] = ["Loaded mock personal alpha workspace metadata only. Raw material, OCR, and legal search content are not stored."]
    return parsed


def _runtime_storage_dir() -> Path:
    return Path("/Users/wazhen/Lawyer-AI-Platform") / RUNTIME_WORKSPACE_STORAGE_RELATIVE_PATH


def _safe_workspace_run_id(workspace_run_id: str) -> str:
    safe = re.sub(r"[^A-Za-z0-9_-]", "_", workspace_run_id or "")
    return safe[:80] or "personal_alpha_workspace_run_missing"
