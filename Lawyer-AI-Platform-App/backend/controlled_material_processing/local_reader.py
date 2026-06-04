from pathlib import Path
from typing import Any
from uuid import uuid4

from controlled_material_processing.audit import append_controlled_material_audit_log
from controlled_material_processing.guards import MAX_FILE_SIZE_BYTES, run_all_controlled_local_read_guards
from controlled_material_processing.redaction import build_redacted_preview
from controlled_material_processing.runtime_storage import store_redacted_preview
from controlled_material_processing.schemas import ControlledLocalReadPreviewRequest, ControlledLocalReadPreviewResult, utc_now


def read_local_text_file_preview(request: ControlledLocalReadPreviewRequest) -> dict[str, Any]:
    created_at = utc_now()
    preview_id = f"controlled_preview_{uuid4().hex[:12]}"
    audit_log_id = f"controlled_material_audit_{uuid4().hex[:12]}"
    guard_results = run_all_controlled_local_read_guards(request)
    allowed_to_continue = all(bool(result.get("allowed")) for result in guard_results)
    warnings = _collect_warnings(guard_results)
    file_path = Path(request.local_file_path).expanduser().resolve()
    file_extension = file_path.suffix.lower()
    file_size = file_path.stat().st_size if file_path.exists() and file_path.is_file() else 0

    if not request.preview_only:
        allowed_to_continue = False
        warnings.append("preview_only must remain true for v4.3 local read preview.")

    if not allowed_to_continue:
        append_controlled_material_audit_log(
            {
                "audit_log_id": audit_log_id,
                "event_type": "controlled_local_read_preview",
                "case_id": request.case_id,
                "workspace_id": request.workspace_id,
                "preview_id": preview_id,
                "material_id": request.material_id,
                "filename_redacted": _safe_filename(request.filename_redacted),
                "result": "blocked_by_controlled_local_read_guard",
                "warnings": warnings,
                "created_at": created_at,
            }
        )
        return ControlledLocalReadPreviewResult(
            preview_id=preview_id,
            case_id=request.case_id,
            workspace_id=request.workspace_id,
            material_id=request.material_id,
            filename_redacted=_safe_filename(request.filename_redacted),
            file_extension=file_extension,
            file_size_bytes=file_size,
            content_read=False,
            raw_content_stored=False,
            redacted_preview_created=False,
            redacted_preview="",
            redacted_preview_storage_path="storage/runtime/controlled_material_previews",
            source_refs=[],
            guard_results=guard_results,
            audit_log_id=audit_log_id,
            allowed_to_continue=False,
            warnings=list(dict.fromkeys(warnings)),
            created_at=created_at,
        ).model_dump()

    raw_text = file_path.read_bytes()[:MAX_FILE_SIZE_BYTES].decode("utf-8", errors="replace")
    redaction_result = build_redacted_preview(raw_text)
    storage_result = store_redacted_preview(preview_id, redaction_result["redacted_preview"])
    source_refs = _source_refs(preview_id, request)
    warnings.extend(redaction_result.get("warnings", []))
    warnings.extend(storage_result.get("warnings", []))

    append_controlled_material_audit_log(
        {
            "audit_log_id": audit_log_id,
            "event_type": "controlled_local_read_preview",
            "case_id": request.case_id,
            "workspace_id": request.workspace_id,
            "preview_id": preview_id,
            "material_id": request.material_id,
            "filename_redacted": _safe_filename(request.filename_redacted),
            "result": "redacted_preview_created",
            "warnings": warnings,
            "created_at": created_at,
        }
    )
    return ControlledLocalReadPreviewResult(
        preview_id=preview_id,
        case_id=request.case_id,
        workspace_id=request.workspace_id,
        material_id=request.material_id,
        filename_redacted=_safe_filename(request.filename_redacted),
        file_extension=file_extension,
        file_size_bytes=file_size,
        content_read=True,
        raw_content_stored=False,
        redacted_preview_created=True,
        redacted_preview=redaction_result["redacted_preview"],
        redacted_preview_storage_path=storage_result["storage_path"],
        source_refs=source_refs,
        guard_results=guard_results,
        audit_log_id=audit_log_id,
        allowed_to_continue=True,
        warnings=list(dict.fromkeys(warnings)),
        created_at=created_at,
    ).model_dump()


def _source_refs(preview_id: str, request: ControlledLocalReadPreviewRequest) -> list[dict[str, Any]]:
    return [
        {
            "source_ref_id": "source_ref_controlled_local_preview_001",
            "source_type": "controlled_local_read_preview",
            "preview_id": preview_id,
            "material_id": request.material_id,
            "filename": _safe_filename(request.filename_redacted),
            "relative_path": "<local_file_path_redacted>",
            "quote": "Redacted preview source placeholder. Raw text is not returned.",
            "provider": "controlled_local",
            "provider_mode": "disabled",
            "mock_or_redacted_only": True,
        }
    ]


def _collect_warnings(guard_results: list[dict[str, Any]]) -> list[str]:
    warnings = [
        "v4.3 local read preview only.",
        "Only .txt, .md, and .json files are eligible.",
        "Raw text is only used in memory to build a redacted preview.",
        "Raw text is not returned, logged, or stored in Git.",
        "No OCR, LLM, legal database, or DeepSeek live provider was called.",
    ]
    for result in guard_results:
        warnings.extend(str(item) for item in result.get("warnings", []))
    return list(dict.fromkeys(warnings))


def _safe_filename(filename_redacted: str | None) -> str:
    if not filename_redacted or "<filename_redacted>" not in filename_redacted:
        return "<filename_redacted>"
    return filename_redacted
