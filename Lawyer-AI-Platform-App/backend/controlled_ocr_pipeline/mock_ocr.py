from pathlib import Path
from typing import Any
from uuid import uuid4

from controlled_ocr_pipeline.audit import append_controlled_ocr_audit_log
from controlled_ocr_pipeline.guards import MAX_FILE_SIZE_BYTES, run_all_controlled_ocr_guards
from controlled_ocr_pipeline.redaction import build_redacted_ocr_preview
from controlled_ocr_pipeline.runtime_storage import load_redacted_ocr_preview, store_redacted_ocr_preview
from controlled_ocr_pipeline.schemas import (
    ControlledOCRPreviewRecord,
    ControlledOCRPreviewRequest,
    ControlledOCRPreviewResult,
    ControlledOCRSourceRef,
    ControlledOCRStatus,
    utc_now,
)


def get_controlled_ocr_status() -> dict[str, Any]:
    return ControlledOCRStatus(
        warnings=[
            "v4.4 is local-only controlled OCR preview.",
            "Mock OCR is enabled by default.",
            "No real OCR provider, LLM, legal database, or DeepSeek live provider is called.",
            "PDF and image binary content is not read in v4.4.",
            "Manual lawyer review and explicit OCR confirmation are required.",
        ]
    ).model_dump()


def run_mock_ocr_preview(request: ControlledOCRPreviewRequest) -> dict[str, Any]:
    created_at = utc_now()
    ocr_preview_id = f"controlled_ocr_preview_{uuid4().hex[:12]}"
    audit_log_id = f"controlled_ocr_audit_{uuid4().hex[:12]}"
    guard_results = run_all_controlled_ocr_guards(request)
    allowed_to_continue = all(bool(result.get("allowed")) for result in guard_results)
    warnings = _collect_warnings(guard_results)
    file_path = Path(request.local_file_path).expanduser().resolve()
    file_extension = file_path.suffix.lower()
    file_size = file_path.stat().st_size if file_path.exists() and file_path.is_file() else 0

    if not request.preview_only:
        allowed_to_continue = False
        warnings.append("preview_only must remain true for v4.4 controlled OCR preview.")

    if not allowed_to_continue:
        append_controlled_ocr_audit_log(
            {
                "audit_log_id": audit_log_id,
                "event_type": "controlled_ocr_preview",
                "case_id": request.case_id,
                "workspace_id": request.workspace_id,
                "ocr_preview_id": ocr_preview_id,
                "material_id": request.material_id,
                "filename_redacted": _safe_filename(request.filename_redacted),
                "result": "blocked_by_controlled_ocr_guard",
                "warnings": warnings,
                "created_at": created_at,
            }
        )
        return ControlledOCRPreviewResult(
            ocr_preview_id=ocr_preview_id,
            case_id=request.case_id,
            workspace_id=request.workspace_id,
            material_id=request.material_id,
            filename_redacted=_safe_filename(request.filename_redacted),
            file_extension=file_extension,
            file_size_bytes=file_size,
            ocr_called=False,
            real_ocr_called=False,
            mock_ocr_used=False,
            raw_ocr_text_stored=False,
            redacted_ocr_preview_created=False,
            redacted_ocr_preview="",
            redacted_ocr_preview_storage_path="storage/runtime/controlled_ocr_previews",
            source_refs=[],
            guard_results=guard_results,
            audit_log_id=audit_log_id,
            allowed_to_continue=False,
            warnings=list(dict.fromkeys(warnings)),
            created_at=created_at,
        ).model_dump()

    mock_ocr_text = _build_mock_ocr_text(request, file_path, file_extension)
    redaction_result = build_redacted_ocr_preview(mock_ocr_text)
    storage_result = store_redacted_ocr_preview(ocr_preview_id, redaction_result["redacted_ocr_preview"])
    source_refs = _source_refs(ocr_preview_id, request)
    warnings.extend(redaction_result.get("warnings", []))
    warnings.extend(storage_result.get("warnings", []))

    append_controlled_ocr_audit_log(
        {
            "audit_log_id": audit_log_id,
            "event_type": "controlled_ocr_preview",
            "case_id": request.case_id,
            "workspace_id": request.workspace_id,
            "ocr_preview_id": ocr_preview_id,
            "material_id": request.material_id,
            "filename_redacted": _safe_filename(request.filename_redacted),
            "result": "redacted_ocr_preview_created",
            "warnings": warnings,
            "created_at": created_at,
        }
    )
    return ControlledOCRPreviewResult(
        ocr_preview_id=ocr_preview_id,
        case_id=request.case_id,
        workspace_id=request.workspace_id,
        material_id=request.material_id,
        filename_redacted=_safe_filename(request.filename_redacted),
        file_extension=file_extension,
        file_size_bytes=file_size,
        ocr_called=True,
        real_ocr_called=False,
        mock_ocr_used=True,
        raw_ocr_text_stored=False,
        redacted_ocr_preview_created=True,
        redacted_ocr_preview=redaction_result["redacted_ocr_preview"],
        redacted_ocr_preview_storage_path=storage_result["storage_path"],
        source_refs=source_refs,
        guard_results=guard_results,
        audit_log_id=audit_log_id,
        allowed_to_continue=True,
        warnings=list(dict.fromkeys(warnings)),
        created_at=created_at,
    ).model_dump()


def get_controlled_ocr_preview(ocr_preview_id: str) -> dict[str, Any]:
    loaded = load_redacted_ocr_preview(ocr_preview_id)
    return ControlledOCRPreviewRecord(
        ocr_preview_id=str(loaded.get("ocr_preview_id", ocr_preview_id)),
        redacted_ocr_preview=str(loaded.get("redacted_ocr_preview", "")),
        source_refs=[
            {
                "source_ref_id": "source_ref_controlled_ocr_preview_loaded_001",
                "source_type": "controlled_ocr_preview",
                "ocr_preview_id": ocr_preview_id,
                "relative_path": "<local_file_path_redacted>",
                "quote": "Loaded redacted OCR preview only. Raw OCR text is not stored.",
                "provider": "controlled_ocr",
                "provider_mode": "mock",
                "mock_or_redacted_only": True,
            }
        ],
        warnings=list(loaded.get("warnings", [])),
        created_at=str(loaded.get("created_at", utc_now())),
    ).model_dump()


def _build_mock_ocr_text(request: ControlledOCRPreviewRequest, file_path: Path, file_extension: str) -> str:
    base = "\n".join(
        [
            "Controlled OCR preview placeholder.",
            "No real OCR provider was called.",
            "This preview is mock-only and requires manual lawyer review.",
        ]
    )
    if file_extension == ".txt":
        seed = file_path.read_bytes()[:MAX_FILE_SIZE_BYTES].decode("utf-8", errors="replace")
        return f"{base}\n\nMock OCR seed preview:\n{seed}"
    return f"{base}\n\nPDF and image binary content was not read. File extension: {file_extension}"


def _source_refs(ocr_preview_id: str, request: ControlledOCRPreviewRequest) -> list[dict[str, Any]]:
    return [
        ControlledOCRSourceRef(
            source_ref_id="source_ref_controlled_ocr_preview_001",
            ocr_preview_id=ocr_preview_id,
            material_id=request.material_id,
            filename=_safe_filename(request.filename_redacted),
            relative_path="<local_file_path_redacted>",
            quote="Redacted OCR preview source placeholder. Raw OCR text is not returned.",
            provider="controlled_ocr",
            provider_mode="mock",
            mock_or_redacted_only=True,
        ).model_dump()
    ]


def _collect_warnings(guard_results: list[dict[str, Any]]) -> list[str]:
    warnings = [
        "v4.4 controlled OCR preview only.",
        "Mock OCR by default.",
        "No real OCR provider was called.",
        "No LLM, legal database, or DeepSeek live provider was called.",
        "PDF and image binary content is not read in v4.4.",
        "Raw OCR text is not returned, logged, or stored in Git.",
    ]
    for result in guard_results:
        warnings.extend(str(item) for item in result.get("warnings", []))
    return list(dict.fromkeys(warnings))


def _safe_filename(filename_redacted: str | None) -> str:
    if not filename_redacted or "<filename_redacted>" not in filename_redacted:
        return "<filename_redacted>"
    return filename_redacted
