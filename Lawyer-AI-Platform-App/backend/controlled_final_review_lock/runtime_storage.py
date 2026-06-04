import json
import re
from pathlib import Path
from typing import Any

from controlled_final_review_lock.schemas import RuntimeControlledFinalReviewLockStorageResult, utc_now

RUNTIME_FINAL_LOCK_STORAGE_RELATIVE_PATH = "storage/runtime/controlled_final_review_locks"


def store_controlled_final_review_lock(final_lock_id: str, record: dict[str, Any]) -> dict[str, Any]:
    safe_id = _safe_final_lock_id(final_lock_id)
    storage_dir = _runtime_storage_dir()
    storage_dir.mkdir(parents=True, exist_ok=True)
    storage_file = storage_dir / f"{safe_id}.json"
    storage_file.write_text(
        json.dumps(
            {
                "final_lock_id": safe_id,
                "case_id": record.get("case_id", ""),
                "workspace_id": record.get("workspace_id", ""),
                "draft_id": record.get("draft_id", ""),
                "review_id": record.get("review_id", ""),
                "revision_id": record.get("revision_id", ""),
                "lock_mode": record.get("lock_mode", ""),
                "mock_final_review_snapshot": record.get("mock_final_review_snapshot", {}),
                "final_review_checklist": record.get("final_review_checklist", []),
                "source_refs": record.get("source_refs", []),
                "created_at": record.get("created_at", utc_now()),
                "immutable_snapshot": True,
                "mock_or_redacted_only": True,
            },
            ensure_ascii=False,
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )
    return RuntimeControlledFinalReviewLockStorageResult(
        stored=True,
        storage_path=f"{RUNTIME_FINAL_LOCK_STORAGE_RELATIVE_PATH}/{safe_id}.json",
        raw_material_text_stored=False,
        raw_ocr_text_stored=False,
        raw_legal_search_results_stored=False,
        final_lock_snapshot_stored_in_git=False,
        immutable_snapshot=True,
        warnings=[
            "Mock final review lock snapshot stored in ignored runtime storage.",
            "Raw material text, raw OCR text, and raw legal search results were not stored.",
        ],
    ).model_dump()


def load_controlled_final_review_lock_record(final_lock_id: str) -> dict[str, Any]:
    safe_id = _safe_final_lock_id(final_lock_id)
    storage_file = _runtime_storage_dir() / f"{safe_id}.json"
    if not storage_file.exists():
        return {
            "final_lock_id": safe_id,
            "mock_final_review_snapshot": {},
            "final_review_checklist": [],
            "source_refs": [],
            "created_at": utc_now(),
            "immutable_snapshot": True,
            "warnings": ["Controlled final review lock record was not found."],
        }
    parsed = json.loads(storage_file.read_text(encoding="utf-8"))
    parsed["warnings"] = ["Loaded mock final review lock metadata only. Raw material, OCR, and legal search content are not stored."]
    return parsed


def _runtime_storage_dir() -> Path:
    return Path("/Users/wazhen/Lawyer-AI-Platform") / RUNTIME_FINAL_LOCK_STORAGE_RELATIVE_PATH


def _safe_final_lock_id(final_lock_id: str) -> str:
    safe = re.sub(r"[^A-Za-z0-9_-]", "_", final_lock_id or "")
    return safe[:80] or "controlled_final_review_lock_missing"
