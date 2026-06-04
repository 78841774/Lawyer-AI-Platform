from typing import Any
from uuid import uuid4

from local_sandbox.audit_log import append_audit_log
from local_sandbox.guards import (
    check_git_safety_guard,
    check_material_safety_guard,
    check_provider_mode_guard,
)
from local_sandbox.schemas import LocalSandboxAuditLog, LocalSandboxDryRunRequest, LocalSandboxDryRunResult, utc_now


def run_local_sandbox_dry_run(request: LocalSandboxDryRunRequest) -> dict[str, Any]:
    created_at = utc_now()
    dry_run_id = f"local_sandbox_dry_run_{uuid4().hex[:12]}"
    audit_log_id = f"local_sandbox_audit_{uuid4().hex[:12]}"

    if not request.dry_run_only:
        guard_results = {
            "provider_mode_guard": check_provider_mode_guard(request.provider_mode, request.ocr_mode, request.legal_search_mode),
            "material_safety_guard": check_material_safety_guard(request.local_case_root),
            "git_safety_guard": check_git_safety_guard(),
        }
        warnings = _collect_warnings(guard_results)
        warnings.append("dry_run_only=false is blocked; v3.9 supports dry-run only.")
        allowed_to_continue = False
    else:
        guard_results = {
            "provider_mode_guard": check_provider_mode_guard(request.provider_mode, request.ocr_mode, request.legal_search_mode),
            "material_safety_guard": check_material_safety_guard(request.local_case_root),
            "git_safety_guard": check_git_safety_guard(),
        }
        warnings = _collect_warnings(guard_results)
        allowed_to_continue = all(
            bool(result.get("allowed"))
            for result in guard_results.values()
            if isinstance(result, dict)
        )

    status = "completed_dry_run" if allowed_to_continue else "blocked_by_guard"
    audit_log = LocalSandboxAuditLog(
        audit_log_id=audit_log_id,
        event_type="local_sandbox_dry_run",
        case_id=request.case_id,
        workspace_id=request.workspace_id,
        dry_run_id=dry_run_id,
        provider_mode=request.provider_mode,
        ocr_mode=request.ocr_mode,
        legal_search_mode=request.legal_search_mode,
        result=status,
        warnings=warnings,
        created_at=created_at
    ).model_dump()
    append_audit_log(audit_log)

    result = LocalSandboxDryRunResult(
        dry_run_id=dry_run_id,
        case_id=request.case_id,
        workspace_id=request.workspace_id,
        status=status,
        allowed_to_continue=allowed_to_continue,
        guard_results=guard_results,
        audit_log_id=audit_log_id,
        warnings=warnings,
        dry_run_only=True,
        created_at=created_at
    )
    return result.model_dump()


def _collect_warnings(guard_results: dict[str, Any]) -> list[str]:
    warnings: list[str] = [
        "No real case material was read.",
        "No real OCR provider was called.",
        "No real legal database was queried.",
        "No real LLM or DeepSeek live provider was called.",
        "No Workspace Runtime or Skill Registry publish was enabled.",
    ]
    for result in guard_results.values():
        if isinstance(result, dict):
            warnings.extend(str(item) for item in result.get("warnings", []))
    return list(dict.fromkeys(warnings))
