import json
import re
from pathlib import Path
from typing import Any

from controlled_legal_search_pipeline.schemas import RuntimeLegalSearchStorageResult, utc_now

RUNTIME_LEGAL_SEARCH_STORAGE_RELATIVE_PATH = "storage/runtime/controlled_legal_search_previews"


def store_redacted_legal_search_preview(search_preview_id: str, preview: dict[str, Any]) -> dict[str, Any]:
    safe_id = _safe_search_preview_id(search_preview_id)
    storage_dir = _runtime_storage_dir()
    storage_dir.mkdir(parents=True, exist_ok=True)
    storage_file = storage_dir / f"{safe_id}.json"
    storage_file.write_text(
        json.dumps(
            {
                "search_preview_id": safe_id,
                "redacted_search_preview": preview.get("redacted_search_preview", ""),
                "citations": preview.get("citations", []),
                "source_refs": preview.get("source_refs", []),
                "created_at": utc_now(),
                "mock_or_redacted_only": True,
            },
            ensure_ascii=False,
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )
    return RuntimeLegalSearchStorageResult(
        stored=True,
        storage_path=f"{RUNTIME_LEGAL_SEARCH_STORAGE_RELATIVE_PATH}/{safe_id}.json",
        raw_query_stored=False,
        raw_results_stored=False,
        redacted_search_preview_stored=True,
        warnings=["Redacted legal search preview stored in ignored runtime storage.", "Raw query and raw results were not stored."],
    ).model_dump()


def load_redacted_legal_search_preview(search_preview_id: str) -> dict[str, Any]:
    safe_id = _safe_search_preview_id(search_preview_id)
    storage_file = _runtime_storage_dir() / f"{safe_id}.json"
    if not storage_file.exists():
        return {"search_preview_id": safe_id, "redacted_search_preview": "", "citations": [], "source_refs": [], "created_at": utc_now(), "warnings": ["Controlled legal search preview was not found."]}
    parsed = json.loads(storage_file.read_text(encoding="utf-8"))
    parsed["warnings"] = ["Loaded redacted legal search preview only. Raw query and raw results are not stored."]
    return parsed


def _runtime_storage_dir() -> Path:
    return Path("/Users/wazhen/Lawyer-AI-Platform") / RUNTIME_LEGAL_SEARCH_STORAGE_RELATIVE_PATH


def _safe_search_preview_id(search_preview_id: str) -> str:
    safe = re.sub(r"[^A-Za-z0-9_-]", "_", search_preview_id or "")
    return safe[:80] or "controlled_legal_search_preview_missing"
