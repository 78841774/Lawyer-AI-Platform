import json
import re
from pathlib import Path
from typing import Any

from controlled_report_draft_pipeline.schemas import RuntimeControlledReportDraftStorageResult, utc_now

RUNTIME_REPORT_DRAFT_STORAGE_RELATIVE_PATH = "storage/runtime/controlled_report_drafts"


def store_controlled_report_draft(draft_id: str, record: dict[str, Any]) -> dict[str, Any]:
    safe_id = _safe_draft_id(draft_id)
    storage_dir = _runtime_storage_dir()
    storage_dir.mkdir(parents=True, exist_ok=True)
    storage_file = storage_dir / f"{safe_id}.json"
    storage_file.write_text(
        json.dumps(
            {
                "draft_id": safe_id,
                "case_id": record.get("case_id", ""),
                "workspace_id": record.get("workspace_id", ""),
                "mock_assembled_report": record.get("mock_assembled_report", {}),
                "source_refs": record.get("source_refs", []),
                "citations": record.get("citations", []),
                "created_at": record.get("created_at", utc_now()),
                "mock_or_redacted_only": True,
            },
            ensure_ascii=False,
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )
    return RuntimeControlledReportDraftStorageResult(
        stored=True,
        storage_path=f"{RUNTIME_REPORT_DRAFT_STORAGE_RELATIVE_PATH}/{safe_id}.json",
        raw_material_text_stored=False,
        raw_ocr_text_stored=False,
        raw_legal_search_results_stored=False,
        report_draft_stored_in_git=False,
        warnings=[
            "Mock report draft stored in ignored runtime storage.",
            "Raw material text, raw OCR text, and raw legal search results were not stored.",
        ],
    ).model_dump()


def load_controlled_report_draft(draft_id: str) -> dict[str, Any]:
    safe_id = _safe_draft_id(draft_id)
    storage_file = _runtime_storage_dir() / f"{safe_id}.json"
    if not storage_file.exists():
        return {
            "draft_id": safe_id,
            "mock_assembled_report": {},
            "source_refs": [],
            "citations": [],
            "created_at": utc_now(),
            "warnings": ["Controlled report draft was not found."],
        }
    parsed = json.loads(storage_file.read_text(encoding="utf-8"))
    parsed["warnings"] = ["Loaded mock report draft only. Raw material, OCR, and legal search content are not stored."]
    return parsed


def _runtime_storage_dir() -> Path:
    return Path("/Users/wazhen/Lawyer-AI-Platform") / RUNTIME_REPORT_DRAFT_STORAGE_RELATIVE_PATH


def _safe_draft_id(draft_id: str) -> str:
    safe = re.sub(r"[^A-Za-z0-9_-]", "_", draft_id or "")
    return safe[:80] or "controlled_report_draft_missing"

