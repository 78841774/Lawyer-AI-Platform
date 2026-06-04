import re
import subprocess
from typing import Any

from personal_alpha_workspace.schemas import (
    PersonalAlphaWorkspaceGuardResult,
    PersonalAlphaWorkspaceRequest,
)

ALLOWED_PROVIDER_MODES = {"mock", "disabled", "local", "local_only", "controlled_local"}
DANGEROUS_PROVIDER_MODES = {"live", "real", "production", "remote", "external", "deepseek_live", "deepseek"}
ALLOWED_WORKFLOW_MODES = {
    "status_only",
    "end_to_end_mock",
    "material_to_final_lock_mock",
    "resume_existing_workspace",
    "audit_timeline_only",
}
SOFT_CONFIRMATION_MODES = {"status_only", "audit_timeline_only"}
RUNTIME_STORAGE_PATH = "storage/runtime/personal_alpha_workspace"
SENSITIVE_PATH_MARKERS = (
    ".env",
    "local.db",
    ".db",
    "sandbox_cases",
    "real_cases",
    "case_workspaces",
    "Lawyer-AI-Local-Cases",
    "AIHome-Law-Local-Sandbox",
    "storage/runtime",
)
RAW_CONTENT_PATTERNS = (
    r"sk-[A-Za-z0-9_-]{12,}",
    r"api[_-]?key",
    r"(?<!\d)1[3-9]\d{9}(?!\d)",
    r"(?<!\d)\d{6}(?:19|20)\d{2}\d{2}\d{2}\d{3}[\dXx](?!\d)",
    r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}",
    r"[（(]\d{4}[）)][\u4e00-\u9fa5A-Za-z0-9第初终再执民商行刑破知号字\-]{4,40}号",
    r"\.(pdf|docx|xlsx|zip|png|jpg|jpeg|txt|md|json)$",
    r"[/\\]",
)


def check_explicit_workspace_confirmation_gate(request: PersonalAlphaWorkspaceRequest) -> dict[str, Any]:
    soft_mode = _normalize(request.workflow_mode) in SOFT_CONFIRMATION_MODES
    warnings = ["Explicit workspace confirmation is required before an end-to-end personal alpha workspace run."]
    if soft_mode and not request.explicit_workspace_confirmation:
        warnings.append("status_only and audit_timeline_only may continue without explicit workspace confirmation.")
    return _guard(
        "explicit_workspace_confirmation_gate",
        request.explicit_workspace_confirmation or soft_mode,
        warnings,
        {"workflow_mode": request.workflow_mode, "explicit_workspace_confirmation": request.explicit_workspace_confirmation},
    )


def check_manual_review_gate(request: PersonalAlphaWorkspaceRequest) -> dict[str, Any]:
    soft_mode = _normalize(request.workflow_mode) == "status_only"
    warnings = ["Manual lawyer review confirmation is required before an end-to-end personal alpha workspace run."]
    if soft_mode and not request.manual_review_confirmed:
        warnings.append("status_only may continue without manual review confirmation.")
    return _guard(
        "manual_review_gate",
        request.manual_review_confirmed or soft_mode,
        warnings,
        {"workflow_mode": request.workflow_mode, "manual_review_confirmed": request.manual_review_confirmed},
    )


def check_workspace_provider_gate(request: PersonalAlphaWorkspaceRequest) -> dict[str, Any]:
    modes = {"llm_mode": request.llm_mode, "provider_mode": request.provider_mode}
    blocked_modes = [
        f"{field_name}={value}"
        for field_name, value in modes.items()
        if _normalize(value) in DANGEROUS_PROVIDER_MODES or _normalize(value) not in ALLOWED_PROVIDER_MODES
    ]
    warnings = [
        "Real LLM provider is blocked in v5.0.",
        "DeepSeek live provider is blocked in v5.0.",
        "External workspace provider is blocked in v5.0.",
    ]
    return _guard("workspace_provider_gate", not blocked_modes, warnings, {"blocked_modes": blocked_modes, **modes})


def check_workflow_mode_gate(request: PersonalAlphaWorkspaceRequest) -> dict[str, Any]:
    workflow_mode = _normalize(request.workflow_mode)
    return _guard(
        "workflow_mode_gate",
        workflow_mode in ALLOWED_WORKFLOW_MODES,
        ["workflow_mode must be an allowed personal alpha workspace mode."],
        {"workflow_mode": request.workflow_mode, "allowed_workflow_modes": sorted(ALLOWED_WORKFLOW_MODES)},
    )


def check_no_raw_content_guard(request: PersonalAlphaWorkspaceRequest) -> dict[str, Any]:
    values = {
        "case_id": request.case_id,
        "workspace_id": request.workspace_id,
        "workflow_mode": request.workflow_mode,
        "material_preview_id": request.material_preview_id,
        "ocr_preview_id": request.ocr_preview_id,
        "legal_search_preview_id": request.legal_search_preview_id,
        "draft_id": request.draft_id,
        "review_id": request.review_id,
        "revision_id": request.revision_id,
        "final_lock_id": request.final_lock_id,
    }
    flagged = []
    for field_name, field_value in values.items():
        text = str(field_value or "")
        if _looks_like_raw_content_or_path(text):
            flagged.append(f"{field_name} contains unsafe value")
    warnings = [
        "No raw material text may be included in personal alpha workspace requests.",
        "No raw OCR text may be included in personal alpha workspace requests.",
        "No raw legal search results may be included in personal alpha workspace requests.",
        "API keys, real paths, real filenames, case numbers, phone numbers, and ID numbers are blocked.",
    ]
    return _guard("no_raw_content_guard", not flagged, warnings, {"flagged_fields": sorted(set(flagged))})


def check_workspace_runtime_storage_guard() -> dict[str, Any]:
    warnings = [
        "Workspace snapshot may only use storage/runtime/personal_alpha_workspace.",
        "Personal alpha workspace runtime storage must be ignored by Git.",
        "Workspace snapshots must not be written to docs, backend, frontend, registry, or tracked paths.",
    ]
    try:
        check = subprocess.run(
            ["git", "check-ignore", "-q", RUNTIME_STORAGE_PATH],
            cwd=_repo_root(),
            check=False,
            capture_output=True,
            text=True,
        )
    except OSError as error:
        return _guard("workspace_runtime_storage_guard", False, [*warnings, f"Runtime storage ignore check failed: {error}"], {"runtime_storage_path": RUNTIME_STORAGE_PATH})
    return _guard("workspace_runtime_storage_guard", check.returncode == 0, warnings, {"runtime_storage_path": RUNTIME_STORAGE_PATH})


def check_workspace_git_storage_guard() -> dict[str, Any]:
    warnings = [
        "Personal alpha workspace runtime files must not enter Git.",
        "Raw material, raw OCR text, and raw legal search results must not enter Git.",
        "API keys and real case materials must not enter Git.",
    ]
    try:
        status_output = subprocess.run(["git", "status", "--short"], cwd=_repo_root(), check=True, capture_output=True, text=True).stdout
    except (OSError, subprocess.CalledProcessError) as error:
        return _guard("workspace_git_storage_guard", False, [*warnings, f"Git storage guard failed: {error}"], {})
    staged_sensitive = _staged_sensitive_paths(status_output)
    if staged_sensitive:
        warnings.append(f"Sensitive staged paths detected: {', '.join(staged_sensitive)}")
    return _guard("workspace_git_storage_guard", not staged_sensitive, warnings, {"staged_sensitive_paths": staged_sensitive})


def run_all_personal_alpha_workspace_guards(request: PersonalAlphaWorkspaceRequest) -> list[dict[str, Any]]:
    return [
        check_explicit_workspace_confirmation_gate(request),
        check_manual_review_gate(request),
        check_workspace_provider_gate(request),
        check_workflow_mode_gate(request),
        check_no_raw_content_guard(request),
        check_workspace_runtime_storage_guard(),
        check_workspace_git_storage_guard(),
    ]


def _guard(guard_name: str, allowed: bool, warnings: list[str], metadata: dict[str, Any]) -> dict[str, Any]:
    return PersonalAlphaWorkspaceGuardResult(
        guard_name=guard_name,
        allowed=allowed,
        status="passed" if allowed else "blocked",
        warnings=warnings,
        metadata=metadata,
    ).model_dump()


def _looks_like_raw_content_or_path(value: str) -> bool:
    lowered = value.lower()
    if any(marker.lower() in lowered for marker in SENSITIVE_PATH_MARKERS):
        return True
    return any(re.search(pattern, value, flags=re.IGNORECASE) for pattern in RAW_CONTENT_PATTERNS)


def _normalize(value: str | None) -> str:
    return (value or "").strip().lower()


def _staged_sensitive_paths(status_output: str) -> list[str]:
    detected: list[str] = []
    for line in status_output.splitlines():
        if len(line) < 4:
            continue
        index_status = line[0]
        path = line[3:].strip().strip('"')
        if " -> " in path:
            path = path.split(" -> ", 1)[1]
        if index_status not in {" ", "?"} and _contains_sensitive_marker(path):
            detected.append(path)
    return sorted(set(detected))


def _contains_sensitive_marker(path: str) -> bool:
    normalized = path.replace("\\", "/")
    if normalized.endswith(".env.example"):
        return False
    return any(marker in normalized for marker in SENSITIVE_PATH_MARKERS)


def _repo_root() -> str:
    return "/Users/wazhen/Lawyer-AI-Platform"
