import re
import subprocess
from typing import Any

from controlled_legal_search_pipeline.schemas import ControlledLegalSearchGuardResult, ControlledLegalSearchPreviewRequest

ALLOWED_MODES = {"mock", "disabled", "local", "local_only", "controlled_local"}
DANGEROUS_MODES = {"live", "real", "production", "remote", "external", "deepseek_live", "deepseek"}
RUNTIME_STORAGE_PATH = "storage/runtime/controlled_legal_search_previews"
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


def redact_legal_query(query_text: str) -> str:
    redacted = query_text or ""
    patterns = [
        (r"(?<!\d)1[3-9]\d{9}(?!\d)", "<PHONE_REDACTED>"),
        (r"(?<!\d)\d{6}(?:19|20)\d{2}\d{2}\d{2}\d{3}[\dXx](?!\d)", "<ID_NUMBER_REDACTED>"),
        (r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}", "<EMAIL_REDACTED>"),
        (r"[（(]\d{4}[）)][\u4e00-\u9fa5A-Za-z0-9第初终再执民商行刑破知号字\-]{4,40}号", "<CASE_NUMBER_REDACTED>"),
        (r"(?<!\d)\d{8,}(?!\d)", "<LONG_NUMBER_REDACTED>"),
    ]
    for pattern, replacement in patterns:
        redacted = re.sub(pattern, replacement, redacted)
    return redacted[:8000]


def check_explicit_legal_search_confirmation_gate(request: ControlledLegalSearchPreviewRequest) -> dict[str, Any]:
    return _guard(
        "explicit_legal_search_confirmation_gate",
        request.explicit_legal_search_confirmation,
        ["Explicit legal search confirmation is required before controlled legal search preview."],
        {},
    )


def check_manual_review_gate(request: ControlledLegalSearchPreviewRequest | Any) -> dict[str, Any]:
    return _guard(
        "manual_review_gate",
        bool(request.manual_review_confirmed),
        ["Manual lawyer review confirmation is required."],
        {},
    )


def check_legal_search_provider_gate(request: ControlledLegalSearchPreviewRequest | Any) -> dict[str, Any]:
    modes = {"legal_search_mode": request.legal_search_mode, "provider_mode": request.provider_mode}
    blocked_modes = [
        f"{name}={value}"
        for name, value in modes.items()
        if _normalize(value) in DANGEROUS_MODES or _normalize(value) not in ALLOWED_MODES
    ]
    warnings = [
        "Real legal search provider is blocked in v4.5.",
        "External legal database provider is blocked in v4.5.",
        "DeepSeek live provider is blocked in v4.5.",
    ]
    return _guard("legal_search_provider_gate", not blocked_modes, warnings, {"blocked_modes": blocked_modes, **modes})


def check_query_redaction_guard(request: ControlledLegalSearchPreviewRequest) -> dict[str, Any]:
    redacted = request.query_text_redacted.strip() or redact_legal_query(request.query_text)
    return _guard(
        "query_redaction_guard",
        bool(redacted),
        [
            "Query redaction is best-effort and requires manual lawyer review.",
            "Raw query must not enter registry, audit logs, or Git.",
            "Customer name risk must be reviewed manually.",
        ],
        {"query_text_redacted": redacted},
    )


def check_legal_search_runtime_storage_guard() -> dict[str, Any]:
    warnings = [
        "Redacted legal search preview may only be stored in storage/runtime/controlled_legal_search_previews.",
        "Controlled legal search runtime storage must be ignored by Git.",
        "Raw query and raw legal search results must not be stored.",
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
        return _guard("legal_search_runtime_storage_guard", False, [*warnings, f"Runtime storage ignore check failed: {error}"], {"runtime_storage_path": RUNTIME_STORAGE_PATH})
    return _guard("legal_search_runtime_storage_guard", check.returncode == 0, warnings, {"runtime_storage_path": RUNTIME_STORAGE_PATH})


def check_legal_search_git_storage_guard() -> dict[str, Any]:
    warnings = [
        "Raw query must not enter Git.",
        "Real legal search results must not enter Git.",
        "API keys must not enter Git.",
        "Real case materials must not enter Git.",
    ]
    try:
        status_output = subprocess.run(["git", "status", "--short"], cwd=_repo_root(), check=True, capture_output=True, text=True).stdout
    except (OSError, subprocess.CalledProcessError) as error:
        return _guard("legal_search_git_storage_guard", False, [*warnings, f"Git storage guard failed: {error}"], {})
    staged_sensitive = _staged_sensitive_paths(status_output)
    if staged_sensitive:
        warnings.append(f"Sensitive staged paths detected: {', '.join(staged_sensitive)}")
    return _guard("legal_search_git_storage_guard", not staged_sensitive, warnings, {"staged_sensitive_paths": staged_sensitive})


def run_all_controlled_legal_search_guards(request: ControlledLegalSearchPreviewRequest) -> list[dict[str, Any]]:
    return [
        check_explicit_legal_search_confirmation_gate(request),
        check_manual_review_gate(request),
        check_legal_search_provider_gate(request),
        check_query_redaction_guard(request),
        check_legal_search_runtime_storage_guard(),
        check_legal_search_git_storage_guard(),
    ]


def _guard(guard_name: str, allowed: bool, warnings: list[str], metadata: dict[str, Any]) -> dict[str, Any]:
    return ControlledLegalSearchGuardResult(
        guard_name=guard_name,
        allowed=allowed,
        status="passed" if allowed else "blocked",
        warnings=warnings,
        metadata=metadata,
    ).model_dump()


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
