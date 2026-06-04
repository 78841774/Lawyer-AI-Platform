from typing import Any
from uuid import uuid4

from controlled_material_processing.audit import append_controlled_material_audit_log
from controlled_material_processing.guards import DANGEROUS_MODES, run_all_controlled_material_guards
from controlled_material_processing.schemas import (
    ControlledMaterialReadRequest,
    ControlledMaterialReadResult,
    ControlledMaterialStatus,
    ControlledReportDraftRequest,
    ControlledReportDraftResult,
    utc_now,
)


def get_controlled_material_status() -> dict[str, Any]:
    return ControlledMaterialStatus(
        warnings=[
            "v4.2 is local-only controlled processing.",
            "Real material content is not read in this stage.",
            "No real OCR, LLM, legal database, or DeepSeek live provider is called.",
            "Manual lawyer review and explicit read confirmation are required.",
        ]
    ).model_dump()


def run_controlled_material_read(request: ControlledMaterialReadRequest) -> dict[str, Any]:
    created_at = utc_now()
    controlled_read_id = f"controlled_read_{uuid4().hex[:12]}"
    audit_log_id = f"controlled_material_audit_{uuid4().hex[:12]}"
    guard_results = run_all_controlled_material_guards(request)
    allowed_to_continue = all(bool(result.get("allowed")) for result in guard_results)
    warnings = _collect_warnings(guard_results)
    result_label = "controlled_read_gate_ready" if allowed_to_continue else "blocked_by_controlled_material_guard"
    source_refs = _controlled_source_refs(request)

    append_controlled_material_audit_log(
        {
            "audit_log_id": audit_log_id,
            "event_type": "controlled_material_read_confirmed",
            "case_id": request.case_id,
            "workspace_id": request.workspace_id,
            "controlled_read_id": controlled_read_id,
            "material_id": request.material_id,
            "filename_redacted": _safe_filename(request.filename_redacted),
            "result": result_label,
            "warnings": warnings,
            "created_at": created_at,
        }
    )
    return ControlledMaterialReadResult(
        controlled_read_id=controlled_read_id,
        case_id=request.case_id,
        workspace_id=request.workspace_id,
        material_id=request.material_id,
        filename_redacted=_safe_filename(request.filename_redacted),
        content_read=False,
        controlled_read_ready=allowed_to_continue,
        requires_next_stage_real_read=True,
        extracted_text_stored=False,
        git_storage_allowed=False,
        allowed_to_continue=allowed_to_continue,
        guard_results=guard_results,
        source_refs=source_refs,
        warnings=warnings,
        audit_log_id=audit_log_id,
        created_at=created_at,
    ).model_dump()


def generate_controlled_report_draft(request: ControlledReportDraftRequest) -> dict[str, Any]:
    created_at = utc_now()
    report_draft_id = f"controlled_report_draft_{uuid4().hex[:12]}"
    audit_log_id = f"controlled_material_audit_{uuid4().hex[:12]}"
    warnings = [
        "Mock controlled report draft only.",
        "No real material content read.",
        "No real LLM call.",
        "Not a final legal opinion.",
        "Manual lawyer review required.",
    ]
    blocked = False
    if not request.manual_review_confirmed:
        warnings.append("Manual lawyer review confirmation is required.")
        blocked = True
    if _normalize(request.llm_mode) in DANGEROUS_MODES:
        warnings.append("Live provider is blocked in v4.2 controlled local processing.")
        warnings.append("DeepSeek live provider is blocked in v4.2 controlled local processing.")
        blocked = True

    status = "mock_draft" if not blocked else "blocked_by_controlled_material_guard"
    append_controlled_material_audit_log(
        {
            "audit_log_id": audit_log_id,
            "event_type": "controlled_report_draft",
            "case_id": request.case_id,
            "workspace_id": request.workspace_id,
            "controlled_read_id": request.controlled_read_id,
            "material_id": None,
            "filename_redacted": "<filename_redacted>",
            "result": status,
            "warnings": warnings,
            "created_at": created_at,
        }
    )
    return ControlledReportDraftResult(
        report_draft_id=report_draft_id,
        case_id=request.case_id,
        workspace_id=request.workspace_id,
        controlled_read_id=request.controlled_read_id,
        status=status,
        legal_opinion_finalized=False,
        requires_human_review=True,
        final_legal_opinion_enabled=False,
        llm_called=False,
        content_read=False,
        mock_only=True,
        source_refs=[
            {
                "source_ref_id": "source_ref_controlled_report_draft_001",
                "source_type": "controlled_report_draft",
                "controlled_read_id": request.controlled_read_id,
                "quote": "Mock controlled report draft source placeholder. No real content read.",
                "provider": "controlled_local",
                "provider_mode": "mock",
                "mock_only": True,
            }
        ],
        warnings=list(dict.fromkeys(warnings)),
        audit_log_id=audit_log_id,
        created_at=created_at,
    ).model_dump()


def _controlled_source_refs(request: ControlledMaterialReadRequest) -> list[dict[str, Any]]:
    return [
        {
            "source_ref_id": "source_ref_controlled_material_001",
            "source_type": "controlled_material",
            "material_id": request.material_id,
            "filename": _safe_filename(request.filename_redacted),
            "relative_path": "<local_case_root_redacted>",
            "quote": "Controlled material source ref placeholder. No real content read.",
            "provider": "controlled_local",
            "provider_mode": "mock",
            "mock_only": True,
        }
    ]


def _collect_warnings(guard_results: list[dict[str, Any]]) -> list[str]:
    warnings = [
        "Controlled material read gate only.",
        "No real material content was read.",
        "No OCR text was stored.",
        "No real OCR, LLM, legal database, or DeepSeek live provider was called.",
        "No material content or extracted text may be stored in Git.",
    ]
    for result in guard_results:
        warnings.extend(str(item) for item in result.get("warnings", []))
    return list(dict.fromkeys(warnings))


def _safe_filename(filename_redacted: str | None) -> str:
    if not filename_redacted or "<filename_redacted>" not in filename_redacted:
        return "<filename_redacted>"
    return filename_redacted


def _normalize(value: str | None) -> str:
    return (value or "").strip().lower()
