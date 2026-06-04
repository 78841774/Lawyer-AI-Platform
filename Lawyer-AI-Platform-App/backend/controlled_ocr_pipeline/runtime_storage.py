import json
import re
from pathlib import Path
from typing import Any

from controlled_ocr_pipeline.schemas import RuntimeOCRStorageResult, utc_now

RUNTIME_OCR_STORAGE_RELATIVE_PATH = "storage/runtime/controlled_ocr_previews"


def store_redacted_ocr_preview(ocr_preview_id: str, redacted_ocr_preview: str) -> dict[str, Any]:
    safe_ocr_preview_id = _safe_ocr_preview_id(ocr_preview_id)
    storage_dir = _runtime_storage_dir()
    storage_dir.mkdir(parents=True, exist_ok=True)
    storage_file = storage_dir / f"{safe_ocr_preview_id}.json"
    storage_file.write_text(
        json.dumps(
            {
                "ocr_preview_id": safe_ocr_preview_id,
                "redacted_ocr_preview": redacted_ocr_preview,
                "created_at": utc_now(),
                "mock_or_redacted_only": True,
            },
            ensure_ascii=False,
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )
    return RuntimeOCRStorageResult(
        stored=True,
        storage_path=f"{RUNTIME_OCR_STORAGE_RELATIVE_PATH}/{safe_ocr_preview_id}.json",
        raw_ocr_text_stored=False,
        redacted_ocr_preview_stored=True,
        warnings=[
            "Redacted OCR preview stored in ignored runtime storage.",
            "Raw OCR text was not stored.",
        ],
    ).model_dump()


def load_redacted_ocr_preview(ocr_preview_id: str) -> dict[str, Any]:
    safe_ocr_preview_id = _safe_ocr_preview_id(ocr_preview_id)
    storage_file = _runtime_storage_dir() / f"{safe_ocr_preview_id}.json"
    if not storage_file.exists():
        return {
            "ocr_preview_id": safe_ocr_preview_id,
            "redacted_ocr_preview": "",
            "created_at": utc_now(),
            "mock_or_redacted_only": True,
            "warnings": ["Controlled OCR preview was not found in runtime storage."],
        }
    parsed = json.loads(storage_file.read_text(encoding="utf-8"))
    return {
        "ocr_preview_id": str(parsed.get("ocr_preview_id", safe_ocr_preview_id)),
        "redacted_ocr_preview": str(parsed.get("redacted_ocr_preview", "")),
        "created_at": str(parsed.get("created_at", utc_now())),
        "mock_or_redacted_only": True,
        "warnings": ["Loaded redacted OCR preview only. Raw OCR text is not stored."],
    }


def _runtime_storage_dir() -> Path:
    return _repo_root() / RUNTIME_OCR_STORAGE_RELATIVE_PATH


def _safe_ocr_preview_id(ocr_preview_id: str) -> str:
    safe = re.sub(r"[^A-Za-z0-9_-]", "_", ocr_preview_id or "")
    return safe[:80] or "controlled_ocr_preview_missing"


def _repo_root() -> Path:
    return Path(__file__).resolve().parents[3]
