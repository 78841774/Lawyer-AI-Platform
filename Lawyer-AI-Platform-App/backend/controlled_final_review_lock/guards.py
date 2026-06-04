import re
import subprocess
from typing import Any

from controlled_final_review_lock.schemas import (
    ControlledFinalReviewLockGuardResult,
    ControlledFinalReviewLockRequest,
)

ALLOWED_MODES = {"mock", "disabled", "local", "local_only", "controlled_local"}
DANGEROUS_MODES = {"live", "real", "production", "remote", "external", "deepseek_live", "deepseek"}
ALLOWED_LOCK_MODES = {
    "mock_final_review_candidate",
    "lock_after_revision",
    "lock_after_approval",
    "lock_for_archive_preview",
}
RUNTIME_STORAGE_PATH = "storage/runtime/controlled_final_review_locks"
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


def check_draft_id_gate(request: ControlledFinalReviewLockRequest) -> dict[str, Any]:
    return _guard(
        "draft_id_gate",
        bool(request.draft_id.strip()),
        ["draft_id is required before final review lock."],
        {"draft_id_present": bool(request.draft_id.strip())},
    )


def check_review_id_gate(request: ControlledFinalReviewLockRequest) -> dict[str, Any]:
    return _guard(
        "review_id_gate",
        bool(request.review_id.strip()),
        ["review_id is required before final review lock."],
        {"review_id_present": bool(request.review_id.strip())},
    )


def check_revision_id_gate(request: ControlledFinalReviewLockRequest) -> dict[str, Any]:
    return _guard(
        "revision_id_gate",
        bool(request.revision_id.strip()),
        ["revision_id is required before final review lock."],
        {"revision_id_present": bool(request.revision_id.strip())},
    )


def check_explicit_final_lock_confirmation_gate(request: ControlledFinalReviewLockRequest) -> dict[str, Any]:
    return _guard(
        "explicit_final_lock_confirmation_gate",
        request.explicit_final_lock_confirmation,
        ["Explicit final lock confirmation is required."],
        {},
    )


def check_manual_final_review_gate(request: ControlledFinalReviewLockRequest) -> dict[str, Any]:
    return _guard(
        "manual_final_review_gate",
        request.manual_final_review_confirmed,
        ["Manual lawyer final review confirmation is required."],
        {},
    )


def check_final_checklist_gate(request: ControlledFinalReviewLockRequest) -> dict[str, Any]:
    return _guard(
        "final_checklist_gate",
        request.final_checklist_confirmed,
        ["Final review checklist must be confirmed before lock."],
        {},
    )


def check_lock_mode_gate(request: ControlledFinalReviewLockRequest) -> dict[str, Any]:
    lock_mode = _normalize(request.lock_mode)
    return _guard(
        "lock_mode_gate",
        lock_mode in ALLOWED_LOCK_MODES,
        ["lock_mode must be an allowed controlled final review lock mode."],
        {"lock_mode": request.lock_mode, "allowed_lock_modes": sorted(ALLOWED_LOCK_MODES)},
    )


def check_final_lock_provider_gate(request: ControlledFinalReviewLockRequest) -> dict[str, Any]:
    modes = {"llm_mode": request.llm_mode, "provider_mode": request.provider_mode}
    blocked_modes = [
        f"{name}={value}"
        for name, value in modes.items()
        if _normalize(value) in DANGEROUS_MODES or _normalize(value) not in ALLOWED_MODES
    ]
    warnings = [
        "Real LLM provider is blocked in v4.9.",
        "DeepSeek live provider is blocked in v4.9.",
        "External final review provider is blocked in v4.9.",
    ]
    return _guard("final_lock_provider_gate", not blocked_modes, warnings, {"blocked_modes": blocked_modes, **modes})


def check_no_raw_content_guard(request: ControlledFinalReviewLockRequest) -> dict[str, Any]:
    values = {
        "case_id": request.case_id,
        "workspace_id": request.workspace_id,
        "draft_id": request.draft_id,
        "review_id": request.review_id,
        "revision_id": request.revision_id,
        "final_review_notes": request.final_review_notes,
        "lock_mode": request.lock_mode,
    }
    flagged = []
    for field_name, field_value in values.items():
        text = str(field_value or "")
        if _looks_like_raw_content_or_path(text):
            flagged.append(f"{field_name} contains unsafe value")
    warnings = [
        "No raw material text may be included in controlled final review lock requests.",
        "No raw OCR text may be included in controlled final review lock requests.",
        "No raw legal search results may be included in controlled final review lock requests.",
        "API keys, real paths, real filenames, case numbers, phone numbers, and ID numbers are blocked.",
    ]
    return _guard("no_raw_content_guard", not flagged, warnings, {"flagged_fields": sorted(set(flagged))})


def check_final_lock_runtime_storage_guard() -> dict[str, Any]:
    warnings = [
        "Final lock snapshot may only use storage/runtime/controlled_final_review_locks.",
        "Controlled final review lock runtime storage must be ignored by Git.",
        "Final lock snapshots must not be written to docs, backend, frontend, registry, or tracked paths.",
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
        return _guard("final_lock_runtime_storage_guard", False, [*warnings, f"Runtime storage ignore check failed: {error}"], {"runtime_storage_path": RUNTIME_STORAGE_PATH})
    return _guard("final_lock_runtime_storage_guard", check.returncode == 0, warnings, {"runtime_storage_path": RUNTIME_STORAGE_PATH})


def check_final_lock_git_storage_guard() -> dict[str, Any]:
    warnings = [
        "Final lock runtime files must not enter Git.",
        "Raw material, raw OCR text, and raw legal search results must not enter Git.",
        "API keys and real case materials must not enter Git.",
    ]
    try:
        status_output = subprocess.run(["git", "status", "--short"], cwd=_repo_root(), check=True, capture_output=True, text=True).stdout
    except (OSError, subprocess.CalledProcessError) as error:
        return _guard("final_lock_git_storage_guard", False, [*warnings, f"Git storage guard failed: {error}"], {})
    staged_sensitive = _staged_sensitive_paths(status_output)
    if staged_sensitive:
        warnings.append(f"Sensitive staged paths detected: {', '.join(staged_sensitive)}")
    return _guard("final_lock_git_storage_guard", not staged_sensitive, warnings, {"staged_sensitive_paths": staged_sensitive})


def run_all_controlled_final_review_lock_guards(request: ControlledFinalReviewLockRequest) -> list[dict[str, Any]]:
    return [
        check_draft_id_gate(request),
        check_review_id_gate(request),
        check_revision_id_gate(request),
        check_explicit_final_lock_confirmation_gate(request),
        check_manual_final_review_gate(request),
        check_final_checklist_gate(request),
        check_lock_mode_gate(request),
        check_final_lock_provider_gate(request),
        check_no_raw_content_guard(request),
        check_final_lock_runtime_storage_guard(),
        check_final_lock_git_storage_guard(),
    ]


def _guard(guard_name: str, allowed: bool, warnings: list[str], metadata: dict[str, Any]) -> dict[str, Any]:
    return ControlledFinalReviewLockGuardResult(
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
