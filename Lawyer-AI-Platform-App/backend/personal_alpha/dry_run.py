from typing import Any
from uuid import uuid4

from internal_alpha.dry_run import run_internal_alpha_dry_run
from internal_alpha.schemas import InternalAlphaDryRunRequest
from personal_alpha.audit import append_personal_alpha_audit_log
from personal_alpha.manifest import preview_case_manifest
from personal_alpha.material_inventory import build_material_inventory_preview
from personal_alpha.schemas import (
    MaterialInventoryRequest,
    PersonalAlphaDryRunRequest,
    PersonalAlphaDryRunResult,
    PersonalCaseManifestPreviewRequest,
    utc_now,
)

DANGEROUS_MODES = {"live", "deepseek", "deepseek_live", "production", "remote", "external"}


def run_personal_alpha_dry_run(request: PersonalAlphaDryRunRequest) -> dict[str, Any]:
    created_at = utc_now()
    dry_run_id = f"personal_alpha_dry_run_{uuid4().hex[:12]}"
    audit_log_id = f"personal_alpha_audit_{uuid4().hex[:12]}"

    manifest_preview = preview_case_manifest(
        PersonalCaseManifestPreviewRequest(
            case_id=request.case_id,
            workspace_id=request.workspace_id,
            case_title_redacted="Personal Alpha redacted case",
            local_case_root=request.local_case_root,
            case_cause_code=request.case_cause_code,
            jurisdiction=request.jurisdiction,
            dry_run_only=request.dry_run_only,
            manual_review_confirmed=request.manual_review_confirmed,
        )
    )
    material_inventory = build_material_inventory_preview(
        MaterialInventoryRequest(
            case_id=request.case_id,
            workspace_id=request.workspace_id,
            local_case_root=request.local_case_root,
            include_file_names=False,
            dry_run_only=request.dry_run_only,
        )
    )
    internal_alpha_result = run_internal_alpha_dry_run(
        InternalAlphaDryRunRequest(
            case_id=request.case_id,
            workspace_id=request.workspace_id,
            local_case_root=request.local_case_root,
            provider_mode=request.provider_mode,
            ocr_mode=request.ocr_mode,
            legal_search_mode=request.legal_search_mode,
            dry_run_only=request.dry_run_only,
            manual_review_confirmed=request.manual_review_confirmed,
        )
    )
    local_sandbox_result = internal_alpha_result.get("local_sandbox_dry_run_result", {})
    warnings = _collect_warnings(manifest_preview, material_inventory, internal_alpha_result)
    warnings.extend(_mode_warnings(request))

    if not request.dry_run_only:
        warnings.append("dry_run_only=false is blocked; v4.1 supports dry-run only.")
    if not request.manual_review_confirmed:
        warnings.append("Manual review confirmation is required before Personal Alpha continuation.")

    allowed_to_continue = (
        bool(manifest_preview.get("allowed_to_continue"))
        and bool(internal_alpha_result.get("allowed_to_continue"))
        and not _has_dangerous_mode(request)
        and request.dry_run_only
        and request.manual_review_confirmed
    )
    result_label = "completed_personal_alpha_dry_run" if allowed_to_continue else "blocked_by_personal_alpha_guard"

    append_personal_alpha_audit_log(
        {
            "audit_log_id": audit_log_id,
            "event_type": "personal_alpha_dry_run",
            "case_id": request.case_id,
            "workspace_id": request.workspace_id,
            "personal_alpha_dry_run_id": dry_run_id,
            "result": result_label,
            "warnings": list(dict.fromkeys(warnings)),
            "created_at": created_at,
        }
    )
    return PersonalAlphaDryRunResult(
        personal_alpha_dry_run_id=dry_run_id,
        manifest_preview=manifest_preview,
        material_inventory=material_inventory,
        internal_alpha_dry_run_result=internal_alpha_result,
        local_sandbox_dry_run_result=local_sandbox_result if isinstance(local_sandbox_result, dict) else {},
        mock_ocr_preview=_mock_ocr_preview(),
        mock_legal_search_preview=_mock_legal_search_preview(request),
        mock_source_trace_preview=_mock_source_trace_preview(),
        mock_report_draft_preview=_mock_report_draft_preview(),
        allowed_to_continue=allowed_to_continue,
        manual_review_required=True,
        audit_log_id=audit_log_id,
        warnings=list(dict.fromkeys(warnings)),
        created_at=created_at,
    ).model_dump()


def _collect_warnings(*payloads: dict[str, Any]) -> list[str]:
    warnings = [
        "Personal Alpha local dry-run only.",
        "No real material content was read.",
        "No real filename is returned.",
        "No real OCR provider was called.",
        "No real legal database was queried.",
        "No real LLM or DeepSeek live provider was called.",
        "Not legal advice.",
        "Manual lawyer review required.",
    ]
    for payload in payloads:
        warnings.extend(str(item) for item in payload.get("warnings", []))
    return list(dict.fromkeys(warnings))


def _mode_warnings(request: PersonalAlphaDryRunRequest) -> list[str]:
    warnings: list[str] = []
    modes = {
        "provider_mode": request.provider_mode,
        "ocr_mode": request.ocr_mode,
        "legal_search_mode": request.legal_search_mode,
        "llm_mode": request.llm_mode,
    }
    for name, value in modes.items():
        normalized = (value or "").strip().lower()
        if normalized == "deepseek_live":
            warnings.append("DeepSeek live provider is blocked in v4.1 Personal Alpha.")
        elif normalized in DANGEROUS_MODES:
            warnings.append(f"Live provider is blocked for {name} in v4.1 Personal Alpha.")
    return warnings


def _has_dangerous_mode(request: PersonalAlphaDryRunRequest) -> bool:
    return any(
        (value or "").strip().lower() in DANGEROUS_MODES
        for value in [request.provider_mode, request.ocr_mode, request.legal_search_mode, request.llm_mode]
    )


def _mock_ocr_preview() -> dict[str, Any]:
    return {
        "status": "mock_preview",
        "provider": "mock_ocr",
        "content_read": False,
        "text_available": False,
        "mock_only": True,
        "warnings": ["No real OCR call.", "No material content read.", "OCR text is not generated in v4.1."],
    }


def _mock_legal_search_preview(request: PersonalAlphaDryRunRequest) -> dict[str, Any]:
    return {
        "status": "mock_preview",
        "provider": "mock_legal_search",
        "case_cause_code": request.case_cause_code,
        "jurisdiction": request.jurisdiction,
        "mock_only": True,
        "warnings": ["No real legal database query.", "Mock legal search preview only."],
    }


def _mock_source_trace_preview() -> dict[str, Any]:
    return {
        "status": "mock_preview",
        "trace_id": "personal_alpha_source_trace_preview",
        "nodes": [],
        "edges": [],
        "mock_only": True,
        "warnings": ["Source trace preview only.", "No real material content or OCR text persisted."],
    }


def _mock_report_draft_preview() -> dict[str, Any]:
    return {
        "title": "Mock Personal Alpha Report Draft Preview",
        "status": "mock_preview",
        "legal_opinion_finalized": False,
        "requires_human_review": True,
        "mock_only": True,
        "warnings": [
            "No real LLM call.",
            "No real case material read.",
            "Not legal advice.",
            "Manual lawyer review required.",
        ],
    }
