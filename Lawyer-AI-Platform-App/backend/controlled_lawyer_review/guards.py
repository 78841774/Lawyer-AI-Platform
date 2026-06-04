import re
import subprocess
from typing import Any

from controlled_lawyer_review.schemas import (
    ControlledLawyerReviewActionRequest,
    ControlledLawyerReviewGuardResult,
    ControlledLawyerReviewSubmitRequest,
)

ALLOWED_MODES = {"mock", "disabled", "local", "local_only", "controlled_local", "mock_review"}
DANGEROUS_MODES = {"live", "real", "production", "remote", "external", "deepseek_live", "deepseek"}
RUNTIME_STORAGE_PATH = "storage/runtime/controlled_lawyer_reviews"
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


def check_explicit_review_confirmation_gate(request: ControlledLawyerReviewSubmitRequest | ControlledLawyerReviewActionRequest) -> dict[str, Any]:
    return _guard(
        "explicit_review_confirmation_gate",
        request.explicit_review_confirmation,
        ["Explicit lawyer review confirmation is required."],
        {},
    )


def check_explicit_assembly_confirmation_gate(request: ControlledLawyerReviewSubmitRequest) -> dict[str, Any]:
    return _guard(
        "explicit_assembly_confirmation_gate",
        request.explicit_assembly_confirmation,
        ["Explicit v4.6 report draft assembly confirmation is required."],
        {},
    )


def check_manual_review_gate(request: ControlledLawyerReviewSubmitRequest | ControlledLawyerReviewActionRequest) -> dict[str, Any]:
    return _guard(
        "manual_review_gate",
        request.manual_review_confirmed,
        ["Manual lawyer review confirmation is required."],
        {},
    )


def check_review_provider_gate(request: ControlledLawyerReviewSubmitRequest | ControlledLawyerReviewActionRequest) -> dict[str, Any]:
    modes = {"llm_mode": request.llm_mode, "provider_mode": request.provider_mode}
    if isinstance(request, ControlledLawyerReviewSubmitRequest):
        modes["review_mode"] = request.review_mode
    blocked_modes = [
        f"{name}={value}"
        for name, value in modes.items()
        if _normalize(value) in DANGEROUS_MODES or _normalize(value) not in ALLOWED_MODES
    ]
    warnings = [
        "Real LLM provider is blocked in v4.7.",
        "DeepSeek live provider is blocked in v4.7.",
        "External review provider is blocked in v4.7.",
    ]
    return _guard("review_provider_gate", not blocked_modes, warnings, {"blocked_modes": blocked_modes, **modes})


def check_mock_report_draft_gate(request: ControlledLawyerReviewSubmitRequest) -> dict[str, Any]:
    allowed = request.draft_status == "mock_draft" and request.draft_id.startswith("controlled_report_draft")
    return _guard(
        "mock_report_draft_gate",
        allowed,
        ["Only v4.6 mock controlled report drafts may enter v4.7 lawyer review."],
        {"draft_id": request.draft_id, "draft_status": request.draft_status},
    )


def check_no_raw_content_guard(request: ControlledLawyerReviewSubmitRequest | ControlledLawyerReviewActionRequest, review_id: str = "") -> dict[str, Any]:
    values: dict[str, Any] = {
        "llm_mode": request.llm_mode,
        "provider_mode": request.provider_mode,
    }
    if isinstance(request, ControlledLawyerReviewSubmitRequest):
        values.update(
            {
                "draft_id": request.draft_id,
                "case_id": request.case_id,
                "workspace_id": request.workspace_id,
                "submitted_by": request.submitted_by,
                "review_mode": request.review_mode,
                "draft_status": request.draft_status,
            }
        )
    else:
        values.update({"review_id": review_id, "reviewer_id": request.reviewer_id, "review_notes": request.review_notes})
    flagged = []
    for field_name, field_value in values.items():
        text = str(field_value or "")
        if _looks_like_raw_content_or_path(text):
            flagged.append(f"{field_name} contains unsafe value")
    warnings = [
        "No raw material text may be included in review workflow requests.",
        "No raw OCR text may be included in review workflow requests.",
        "No raw legal search results may be included in review workflow requests.",
        "API keys, real paths, real filenames, case numbers, phone numbers, and ID numbers are blocked.",
    ]
    return _guard("no_raw_content_guard", not flagged, warnings, {"flagged_fields": sorted(set(flagged))})


def check_review_runtime_storage_guard() -> dict[str, Any]:
    warnings = [
        "Review records may only use storage/runtime/controlled_lawyer_reviews.",
        "Controlled lawyer review runtime storage must be ignored by Git.",
        "Review records must not be written to docs, backend, frontend, registry, or tracked paths.",
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
        return _guard("review_runtime_storage_guard", False, [*warnings, f"Runtime storage ignore check failed: {error}"], {"runtime_storage_path": RUNTIME_STORAGE_PATH})
    return _guard("review_runtime_storage_guard", check.returncode == 0, warnings, {"runtime_storage_path": RUNTIME_STORAGE_PATH})


def check_review_git_storage_guard() -> dict[str, Any]:
    warnings = [
        "Review runtime files must not enter Git.",
        "Raw material, raw OCR text, and raw legal search results must not enter Git.",
        "API keys and real case materials must not enter Git.",
    ]
    try:
        status_output = subprocess.run(["git", "status", "--short"], cwd=_repo_root(), check=True, capture_output=True, text=True).stdout
    except (OSError, subprocess.CalledProcessError) as error:
        return _guard("review_git_storage_guard", False, [*warnings, f"Git storage guard failed: {error}"], {})
    staged_sensitive = _staged_sensitive_paths(status_output)
    if staged_sensitive:
        warnings.append(f"Sensitive staged paths detected: {', '.join(staged_sensitive)}")
    return _guard("review_git_storage_guard", not staged_sensitive, warnings, {"staged_sensitive_paths": staged_sensitive})


def run_submit_guards(request: ControlledLawyerReviewSubmitRequest) -> list[dict[str, Any]]:
    return [
        check_explicit_review_confirmation_gate(request),
        check_explicit_assembly_confirmation_gate(request),
        check_manual_review_gate(request),
        check_review_provider_gate(request),
        check_mock_report_draft_gate(request),
        check_no_raw_content_guard(request),
        check_review_runtime_storage_guard(),
        check_review_git_storage_guard(),
    ]


def run_action_guards(request: ControlledLawyerReviewActionRequest, review_id: str) -> list[dict[str, Any]]:
    return [
        check_explicit_review_confirmation_gate(request),
        check_manual_review_gate(request),
        check_review_provider_gate(request),
        check_no_raw_content_guard(request, review_id),
        check_review_runtime_storage_guard(),
        check_review_git_storage_guard(),
    ]


def _guard(guard_name: str, allowed: bool, warnings: list[str], metadata: dict[str, Any]) -> dict[str, Any]:
    return ControlledLawyerReviewGuardResult(
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

