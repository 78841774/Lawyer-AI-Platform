import json
import re
from pathlib import Path
from typing import Any

from controlled_revision_workflow.schemas import RuntimeControlledRevisionStorageResult, utc_now

RUNTIME_REVISION_STORAGE_RELATIVE_PATH = "storage/runtime/controlled_revisions"


def store_controlled_revision(revision_id: str, record: dict[str, Any]) -> dict[str, Any]:
    safe_id = _safe_revision_id(revision_id)
    storage_dir = _runtime_storage_dir()
    storage_dir.mkdir(parents=True, exist_ok=True)
    storage_file = storage_dir / f"{safe_id}.json"
    storage_file.write_text(
        json.dumps(
            {
                "revision_id": safe_id,
                "case_id": record.get("case_id", ""),
                "workspace_id": record.get("workspace_id", ""),
                "review_id": record.get("review_id", ""),
                "draft_id": record.get("draft_id", ""),
                "requested_action": record.get("requested_action", ""),
                "mock_revision_plan": record.get("mock_revision_plan", {}),
                "revision_checklist": record.get("revision_checklist", []),
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
    return RuntimeControlledRevisionStorageResult(
        stored=True,
        storage_path=f"{RUNTIME_REVISION_STORAGE_RELATIVE_PATH}/{safe_id}.json",
        raw_material_text_stored=False,
        raw_ocr_text_stored=False,
        raw_legal_search_results_stored=False,
        revision_output_stored_in_git=False,
        warnings=[
            "Mock revision plan stored in ignored runtime storage.",
            "Raw material text, raw OCR text, and raw legal search results were not stored.",
        ],
    ).model_dump()


def load_controlled_revision_record(revision_id: str) -> dict[str, Any]:
    safe_id = _safe_revision_id(revision_id)
    storage_file = _runtime_storage_dir() / f"{safe_id}.json"
    if not storage_file.exists():
        return {
            "revision_id": safe_id,
            "mock_revision_plan": {},
            "revision_checklist": [],
            "source_refs": [],
            "created_at": utc_now(),
            "warnings": ["Controlled revision record was not found."],
        }
    parsed = json.loads(storage_file.read_text(encoding="utf-8"))
    parsed["warnings"] = ["Loaded mock revision metadata only. Raw material, OCR, and legal search content are not stored."]
    return parsed


def _runtime_storage_dir() -> Path:
    return Path("/Users/wazhen/Lawyer-AI-Platform") / RUNTIME_REVISION_STORAGE_RELATIVE_PATH


def _safe_revision_id(revision_id: str) -> str:
    safe = re.sub(r"[^A-Za-z0-9_-]", "_", revision_id or "")
    return safe[:80] or "controlled_revision_missing"

