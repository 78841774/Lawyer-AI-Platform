import subprocess
from pathlib import Path
from typing import Any

from local_sandbox.schemas import GitSafetyGuard, MaterialSafetyGuard, ProviderModeGuard

ALLOWED_MODES = {"mock", "local", "local_only", "disabled"}
DANGEROUS_MODES = {"live", "deepseek", "deepseek_live", "production", "remote", "external"}
ALLOWED_ROOTS = ("~/Lawyer-AI-Local-Cases", "~/AIHome-Law-Local-Sandbox")
BLOCKED_PATH_MARKERS = (
    ".env",
    "local.db",
    "sandbox_cases",
    "real_cases",
    "case_workspaces",
    "storage/runtime",
    "__pycache__",
    "__MACOSX",
    ".DS_Store",
)


def check_provider_mode_guard(provider_mode: str, ocr_mode: str, legal_search_mode: str) -> dict[str, Any]:
    modes = {
        "provider_mode": provider_mode,
        "ocr_mode": ocr_mode,
        "legal_search_mode": legal_search_mode,
    }
    warnings = [
        "Live provider is blocked in v3.9 local sandbox.",
        "DeepSeek live provider is blocked in v3.9 local sandbox.",
        "External provider is blocked in v3.9 local sandbox.",
    ]
    dangerous_values = [
        value
        for value in modes.values()
        if _normalize_mode(value) in DANGEROUS_MODES
    ]
    unsupported_values = [
        value
        for value in modes.values()
        if _normalize_mode(value) not in ALLOWED_MODES and _normalize_mode(value) not in DANGEROUS_MODES
    ]
    allowed = not dangerous_values and not unsupported_values
    if unsupported_values:
        warnings.append("Unsupported provider mode is blocked in v3.9 local sandbox.")
    return ProviderModeGuard(
        provider_mode=provider_mode,
        ocr_mode=ocr_mode,
        legal_search_mode=legal_search_mode,
        allowed=allowed,
        warnings=warnings
    ).model_dump()


def check_material_safety_guard(local_case_root: str | None) -> dict[str, Any]:
    warnings = [
        "Material guard did not read file content.",
        "Real case material is not allowed in Git.",
        "Local case root must be outside repository and ignored by Git.",
        "v3.9 only validates sandbox boundary.",
    ]
    path_allowed = bool(local_case_root) and _is_allowed_local_root(local_case_root) and not _contains_blocked_marker(local_case_root)
    if not local_case_root:
        warnings.append("Local case root is empty; dry-run cannot continue.")
    if local_case_root and not _is_allowed_local_root(local_case_root):
        warnings.append("Local case root must use an approved local-only sandbox prefix.")
    if local_case_root and _contains_blocked_marker(local_case_root):
        warnings.append("Repository-internal or blocked real case material path detected.")
    return MaterialSafetyGuard(
        local_case_root="<local_case_root_redacted>" if local_case_root else None,
        local_case_root_redacted="<local_case_root_redacted>" if local_case_root else None,
        path_allowed=path_allowed,
        allowed=path_allowed,
        warnings=warnings
    ).model_dump()


def check_git_safety_guard() -> dict[str, Any]:
    warnings = [
        "Git safety guard only reports sensitive tracked or staged paths.",
        "No user files are deleted or modified by this guard.",
    ]
    try:
        status_output = subprocess.run(
            ["git", "status", "--short"],
            cwd=_repo_root(),
            check=True,
            capture_output=True,
            text=True,
        ).stdout
        tracked_output = subprocess.run(
            ["git", "ls-files"],
            cwd=_repo_root(),
            check=True,
            capture_output=True,
            text=True,
        ).stdout
        git_status_checked = True
    except (OSError, subprocess.CalledProcessError) as error:
        return GitSafetyGuard(
            git_status_checked=False,
            forbidden_paths_detected=[],
            staged_sensitive_files_detected=[],
            allowed=False,
            warnings=[*warnings, f"Git safety guard failed: {error}"]
        ).model_dump()

    staged_sensitive = _find_staged_sensitive_paths(status_output)
    tracked_sensitive = _find_sensitive_paths(tracked_output.splitlines())
    forbidden = sorted(set(staged_sensitive + tracked_sensitive))
    allowed = not forbidden
    if forbidden:
        warnings.append("Sensitive staged or tracked paths detected.")
    return GitSafetyGuard(
        git_status_checked=git_status_checked,
        forbidden_paths_detected=forbidden,
        staged_sensitive_files_detected=staged_sensitive,
        allowed=allowed,
        warnings=warnings
    ).model_dump()


def get_all_guards() -> dict[str, Any]:
    return {
        "provider_mode_guard": check_provider_mode_guard("mock", "mock", "mock"),
        "material_safety_guard": check_material_safety_guard("~/Lawyer-AI-Local-Cases/demo_case"),
        "git_safety_guard": check_git_safety_guard(),
    }


def _normalize_mode(value: str | None) -> str:
    return (value or "").strip().lower()


def _is_allowed_local_root(value: str) -> bool:
    normalized = value.strip()
    return any(normalized == root or normalized.startswith(f"{root}/") for root in ALLOWED_ROOTS)


def _contains_blocked_marker(value: str) -> bool:
    normalized = value.replace("\\", "/")
    if normalized.endswith(".env.example"):
        return False
    return any(marker in normalized for marker in BLOCKED_PATH_MARKERS)


def _find_staged_sensitive_paths(status_output: str) -> list[str]:
    detected: list[str] = []
    for line in status_output.splitlines():
        if len(line) < 4:
            continue
        index_status = line[0]
        path = _normalize_status_path(line[3:])
        if index_status not in {" ", "?"} and _contains_blocked_marker(path):
            detected.append(path)
    return sorted(set(detected))


def _find_sensitive_paths(paths: list[str]) -> list[str]:
    return sorted({path for path in paths if _contains_blocked_marker(path)})


def _normalize_status_path(value: str) -> str:
    path = value.strip()
    if " -> " in path:
        path = path.split(" -> ", 1)[1]
    return path.strip('"')


def _repo_root() -> Path:
    return Path(__file__).resolve().parents[3]
