import json
import re
from pathlib import Path
from typing import Any

from controlled_material_processing.schemas import RuntimeStorageResult, utc_now

RUNTIME_STORAGE_RELATIVE_PATH = "storage/runtime/controlled_material_previews"


def store_redacted_preview(preview_id: str, redacted_preview: str) -> dict[str, Any]:
    safe_preview_id = _safe_preview_id(preview_id)
    storage_dir = _runtime_storage_dir()
    storage_dir.mkdir(parents=True, exist_ok=True)
    storage_file = storage_dir / f"{safe_preview_id}.json"
    storage_file.write_text(
        json.dumps(
            {
                "preview_id": safe_preview_id,
                "redacted_preview": redacted_preview,
                "created_at": utc_now(),
                "mock_or_redacted_only": True,
            },
            ensure_ascii=False,
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )
    return RuntimeStorageResult(
        stored=True,
        storage_path=f"{RUNTIME_STORAGE_RELATIVE_PATH}/{safe_preview_id}.json",
        raw_content_stored=False,
        redacted_preview_stored=True,
        warnings=[
            "Redacted preview stored in ignored runtime storage.",
            "Raw text was not stored.",
        ],
    ).model_dump()


def load_redacted_preview(preview_id: str) -> dict[str, Any]:
    safe_preview_id = _safe_preview_id(preview_id)
    storage_file = _runtime_storage_dir() / f"{safe_preview_id}.json"
    if not storage_file.exists():
        return {
            "preview_id": safe_preview_id,
            "redacted_preview": "",
            "created_at": utc_now(),
            "mock_or_redacted_only": True,
            "warnings": ["Controlled read preview was not found in runtime storage."],
        }
    parsed = json.loads(storage_file.read_text(encoding="utf-8"))
    return {
        "preview_id": str(parsed.get("preview_id", safe_preview_id)),
        "redacted_preview": str(parsed.get("redacted_preview", "")),
        "created_at": str(parsed.get("created_at", utc_now())),
        "mock_or_redacted_only": True,
        "warnings": ["Loaded redacted preview only. Raw text is not stored."],
    }


def _runtime_storage_dir() -> Path:
    return _repo_root() / RUNTIME_STORAGE_RELATIVE_PATH


def _safe_preview_id(preview_id: str) -> str:
    safe = re.sub(r"[^A-Za-z0-9_-]", "_", preview_id or "")
    return safe[:80] or "controlled_preview_missing"


def _repo_root() -> Path:
    return Path(__file__).resolve().parents[3]
