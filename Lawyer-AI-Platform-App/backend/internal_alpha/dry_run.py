from typing import Any
from uuid import uuid4

from internal_alpha.audit import append_internal_alpha_audit_log
from internal_alpha.readiness import get_deployment_readiness_checklist
from internal_alpha.schemas import InternalAlphaDryRunRequest, InternalAlphaDryRunResult, utc_now
from local_sandbox.dry_run import run_local_sandbox_dry_run
from local_sandbox.schemas import LocalSandboxDryRunRequest


def run_internal_alpha_dry_run(request: InternalAlphaDryRunRequest) -> dict[str, Any]:
    created_at = utc_now()
    alpha_dry_run_id = f"internal_alpha_dry_run_{uuid4().hex[:12]}"
    audit_log_id = f"internal_alpha_audit_{uuid4().hex[:12]}"

    local_result = run_local_sandbox_dry_run(
        LocalSandboxDryRunRequest(
            case_id=request.case_id,
            workspace_id=request.workspace_id,
            local_case_root=request.local_case_root,
            provider_mode=request.provider_mode,
            ocr_mode=request.ocr_mode,
            legal_search_mode=request.legal_search_mode,
            dry_run_only=request.dry_run_only,
        )
    )
    readiness = get_deployment_readiness_checklist()
    warnings = _collect_warnings(local_result, readiness)

    if not request.dry_run_only:
        warnings.append("dry_run_only=false is blocked; v4.0 supports dry-run only.")
    if not request.manual_review_confirmed:
        warnings.append("Manual review confirmation is required before Internal Alpha continuation.")

    required_passed = bool(readiness.get("required_passed"))
    allowed_to_continue = (
        bool(local_result.get("allowed_to_continue"))
        and required_passed
        and request.dry_run_only
        and request.manual_review_confirmed
    )
    result_label = "completed_internal_alpha_dry_run" if allowed_to_continue else "blocked_by_internal_alpha_guard"

    append_internal_alpha_audit_log(
        {
            "audit_log_id": audit_log_id,
            "event_type": "internal_alpha_dry_run",
            "case_id": request.case_id,
            "workspace_id": request.workspace_id,
            "alpha_dry_run_id": alpha_dry_run_id,
            "local_sandbox_dry_run_id": local_result.get("dry_run_id"),
            "provider_mode": request.provider_mode,
            "ocr_mode": request.ocr_mode,
            "legal_search_mode": request.legal_search_mode,
            "result": result_label,
            "warnings": warnings,
            "created_at": created_at,
        }
    )
    return InternalAlphaDryRunResult(
        alpha_dry_run_id=alpha_dry_run_id,
        local_sandbox_dry_run_result=local_result,
        readiness_summary={
            "required_passed": readiness.get("required_passed"),
            "manual_verification_required": readiness.get("manual_verification_required"),
            "items": readiness.get("items", []),
        },
        allowed_to_continue=allowed_to_continue,
        manual_review_required=True,
        audit_log_id=audit_log_id,
        warnings=warnings,
        created_at=created_at,
    ).model_dump()


def _collect_warnings(local_result: dict[str, Any], readiness: dict[str, Any]) -> list[str]:
    warnings: list[str] = [
        "Internal Alpha dry-run only.",
        "No real case material was read.",
        "No real OCR provider was called.",
        "No real legal database was queried.",
        "No real LLM or DeepSeek live provider was called.",
        "No Workspace Runtime or Skill Registry publish was enabled.",
    ]
    warnings.extend(str(item) for item in local_result.get("warnings", []))
    warnings.extend(str(item) for item in readiness.get("warnings", []))
    return list(dict.fromkeys(warnings))
