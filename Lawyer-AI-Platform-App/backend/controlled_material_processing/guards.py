import subprocess
from pathlib import Path
from typing import Any

from controlled_material_processing.schemas import (
    ControlledLocalFileGuardResult,
    ControlledMaterialGuardResult,
    ControlledMaterialReadRequest,
    ControlledProviderGateResult,
)

ALLOWED_MODES = {"mock", "local", "local_only", "disabled", "controlled_local"}
DANGEROUS_MODES = {"live", "deepseek_live", "deepseek", "production", "remote", "external"}
ALLOWED_FILE_EXTENSIONS = {".txt", ".md", ".json"}
BLOCKED_FILE_EXTENSIONS = {".pdf", ".doc", ".docx", ".jpg", ".jpeg", ".png", ".heic", ".xlsx", ".zip", ".rar", ".7z", ".eml", ".msg"}
MAX_FILE_SIZE_BYTES = 200000
RUNTIME_STORAGE_PATH = "storage/runtime/controlled_material_previews"
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


def check_explicit_read_confirmation_gate(request: ControlledMaterialReadRequest | Any) -> dict[str, Any]:
    warnings = ["Explicit read confirmation is required before controlled material processing."]
    return ControlledMaterialGuardResult(
        guard_name="explicit_read_confirmation_gate",
        allowed=request.explicit_read_confirmation,
        status="passed" if request.explicit_read_confirmation else "blocked",
        warnings=warnings,
    ).model_dump()


def check_manual_review_gate(request: ControlledMaterialReadRequest | Any) -> dict[str, Any]:
    warnings = ["Manual lawyer review confirmation is required."]
    return ControlledMaterialGuardResult(
        guard_name="manual_review_gate",
        allowed=request.manual_review_confirmed,
        status="passed" if request.manual_review_confirmed else "blocked",
        warnings=warnings,
    ).model_dump()


def check_controlled_provider_gate(request: ControlledMaterialReadRequest | Any) -> dict[str, Any]:
    modes = {
        "provider_mode": request.provider_mode,
        "ocr_mode": request.ocr_mode,
        "llm_mode": request.llm_mode,
        "legal_search_mode": request.legal_search_mode,
    }
    blocked_modes = [
        f"{name}={value}"
        for name, value in modes.items()
        if _normalize(value) in DANGEROUS_MODES or _normalize(value) not in ALLOWED_MODES
    ]
    warnings = [
        "Live provider is blocked in controlled local processing.",
        "DeepSeek live provider is blocked in controlled local processing.",
        "External provider is blocked in controlled local processing.",
    ]
    if any(_normalize(value) not in ALLOWED_MODES and _normalize(value) not in DANGEROUS_MODES for value in modes.values()):
        warnings.append("Unsupported provider mode is blocked in controlled local processing.")
    return ControlledProviderGateResult(
        provider_mode=request.provider_mode,
        ocr_mode=request.ocr_mode,
        llm_mode=request.llm_mode,
        legal_search_mode=request.legal_search_mode,
        allowed=not blocked_modes,
        blocked_modes=blocked_modes,
        warnings=warnings,
    ).model_dump()


def check_material_content_read_guard(request: ControlledMaterialReadRequest | Any) -> dict[str, Any]:
    return ControlledMaterialGuardResult(
        guard_name="material_content_read_guard",
        allowed=True,
        status="controlled_gate_ready",
        warnings=[
            "v4.2 prepares controlled read gates only.",
            "Real material content is not read in this stage.",
            "Next stage must implement actual local file reading with stricter safeguards.",
        ],
    ).model_dump()


def check_local_file_path_guard(request: Any) -> dict[str, Any]:
    file_path = _resolve_local_file_path(getattr(request, "local_file_path", None))
    warnings = [
        "Local file path must exist and must be a file.",
        "Local file path is always returned as <local_file_path_redacted>.",
        "Git repository internal files and runtime storage paths are blocked.",
    ]
    metadata = {"local_file_path_redacted": "<local_file_path_redacted>"}
    if file_path is None:
        return ControlledLocalFileGuardResult(
            guard_name="local_file_path_guard",
            allowed=False,
            status="blocked",
            warnings=[*warnings, "local_file_path is required."],
            metadata=metadata,
        ).model_dump()
    metadata["file_extension"] = file_path.suffix.lower()
    if not file_path.exists():
        return ControlledLocalFileGuardResult(
            guard_name="local_file_path_guard",
            allowed=False,
            status="blocked",
            warnings=[*warnings, "Local file does not exist."],
            metadata=metadata,
        ).model_dump()
    if file_path.is_dir():
        return ControlledLocalFileGuardResult(
            guard_name="local_file_path_guard",
            allowed=False,
            status="blocked",
            warnings=[*warnings, "Local file path must not be a directory."],
            metadata=metadata,
        ).model_dump()
    blocked = _is_repo_internal(file_path) or _contains_sensitive_material_dir(file_path) or _is_runtime_storage_path(file_path)
    if blocked:
        warnings.append("Local file path is blocked because it is inside the repository, runtime storage, or a blocked material directory.")
    return ControlledLocalFileGuardResult(
        guard_name="local_file_path_guard",
        allowed=not blocked,
        status="passed" if not blocked else "blocked",
        warnings=warnings,
        metadata=metadata,
    ).model_dump()


def check_file_extension_guard(file_path: str | Path | None) -> dict[str, Any]:
    resolved = _resolve_local_file_path(file_path)
    extension = resolved.suffix.lower() if resolved else ""
    allowed = extension in ALLOWED_FILE_EXTENSIONS
    warnings = ["Only .txt, .md, and .json are allowed for v4.3 local read preview."]
    if extension in BLOCKED_FILE_EXTENSIONS:
        warnings.append("PDF, Word, image, spreadsheet, archive, and email files are blocked in v4.3.")
    if not extension:
        warnings.append("File extension is required.")
    return ControlledLocalFileGuardResult(
        guard_name="file_extension_guard",
        allowed=allowed,
        status="passed" if allowed else "blocked",
        warnings=warnings,
        metadata={"file_extension": extension},
    ).model_dump()


def check_file_size_guard(file_path: str | Path | None) -> dict[str, Any]:
    resolved = _resolve_local_file_path(file_path)
    warnings = [f"File size must be at or below {MAX_FILE_SIZE_BYTES} bytes."]
    if resolved is None or not resolved.exists() or resolved.is_dir():
        return ControlledLocalFileGuardResult(
            guard_name="file_size_guard",
            allowed=False,
            status="blocked",
            warnings=[*warnings, "File does not exist or is not a regular file."],
            metadata={"max_file_size_bytes": MAX_FILE_SIZE_BYTES, "file_size_bytes": 0},
        ).model_dump()
    size = resolved.stat().st_size
    allowed = size <= MAX_FILE_SIZE_BYTES
    if not allowed:
        warnings.append("File exceeds v4.3 local read preview size limit.")
    return ControlledLocalFileGuardResult(
        guard_name="file_size_guard",
        allowed=allowed,
        status="passed" if allowed else "blocked",
        warnings=warnings,
        metadata={"max_file_size_bytes": MAX_FILE_SIZE_BYTES, "file_size_bytes": size},
    ).model_dump()


def check_path_outside_repo_guard(file_path: str | Path | None) -> dict[str, Any]:
    resolved = _resolve_local_file_path(file_path)
    warnings = ["Local read preview files must be outside the Git repository."]
    inside_repo = bool(resolved and _is_repo_internal(resolved))
    return ControlledLocalFileGuardResult(
        guard_name="path_outside_repo_guard",
        allowed=bool(resolved) and not inside_repo,
        status="passed" if resolved and not inside_repo else "blocked",
        warnings=warnings if resolved else [*warnings, "local_file_path is required."],
        metadata={"local_file_path_redacted": "<local_file_path_redacted>"},
    ).model_dump()


def check_runtime_storage_guard() -> dict[str, Any]:
    warnings = [
        "Redacted preview may only be stored in storage/runtime/controlled_material_previews.",
        "Runtime storage must be ignored by Git.",
        "Raw text must not be stored in runtime storage.",
    ]
    storage_path = _repo_root() / RUNTIME_STORAGE_PATH
    try:
        check = subprocess.run(
            ["git", "check-ignore", "-q", str(storage_path.relative_to(_repo_root()))],
            cwd=_repo_root(),
            check=False,
            capture_output=True,
            text=True,
        )
    except OSError as error:
        return ControlledLocalFileGuardResult(
            guard_name="runtime_storage_guard",
            allowed=False,
            status="blocked",
            warnings=[*warnings, f"Runtime storage ignore check failed: {error}"],
            metadata={"runtime_storage_path": RUNTIME_STORAGE_PATH},
        ).model_dump()
    return ControlledLocalFileGuardResult(
        guard_name="runtime_storage_guard",
        allowed=check.returncode == 0,
        status="passed" if check.returncode == 0 else "blocked",
        warnings=warnings,
        metadata={"runtime_storage_path": RUNTIME_STORAGE_PATH},
    ).model_dump()


def check_git_storage_guard() -> dict[str, Any]:
    warnings = [
        "Material content must not enter Git.",
        "OCR text must not enter Git.",
        "Full real paths must not enter Git.",
        "Real filenames must not enter audit logs.",
    ]
    try:
        status_output = subprocess.run(
            ["git", "status", "--short"],
            cwd=_repo_root(),
            check=True,
            capture_output=True,
            text=True,
        ).stdout
    except (OSError, subprocess.CalledProcessError) as error:
        return ControlledMaterialGuardResult(
            guard_name="git_storage_guard",
            allowed=False,
            status="blocked",
            warnings=[*warnings, f"Git storage guard failed: {error}"],
        ).model_dump()

    staged_sensitive = _staged_sensitive_paths(status_output)
    if staged_sensitive:
        warnings.append(f"Sensitive staged paths detected: {', '.join(staged_sensitive)}")
    return ControlledMaterialGuardResult(
        guard_name="git_storage_guard",
        allowed=not staged_sensitive,
        status="passed" if not staged_sensitive else "blocked",
        warnings=warnings,
    ).model_dump()


def run_all_controlled_material_guards(request: ControlledMaterialReadRequest) -> list[dict[str, Any]]:
    return [
        check_explicit_read_confirmation_gate(request),
        check_manual_review_gate(request),
        check_controlled_provider_gate(request),
        check_material_content_read_guard(request),
        check_git_storage_guard(),
    ]


def run_all_controlled_local_read_guards(request: Any) -> list[dict[str, Any]]:
    return [
        check_explicit_read_confirmation_gate(request),
        check_manual_review_gate(request),
        check_controlled_provider_gate(request),
        check_local_file_path_guard(request),
        check_file_extension_guard(getattr(request, "local_file_path", None)),
        check_file_size_guard(getattr(request, "local_file_path", None)),
        check_path_outside_repo_guard(getattr(request, "local_file_path", None)),
        check_runtime_storage_guard(),
        check_git_storage_guard(),
    ]


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


def _resolve_local_file_path(file_path: str | Path | None) -> Path | None:
    if file_path is None or not str(file_path).strip():
        return None
    return Path(str(file_path)).expanduser().resolve()


def _is_repo_internal(file_path: Path) -> bool:
    try:
        file_path.relative_to(_repo_root())
        return True
    except ValueError:
        return False


def _is_runtime_storage_path(file_path: Path) -> bool:
    runtime_path = (_repo_root() / "storage/runtime").resolve()
    try:
        file_path.relative_to(runtime_path)
        return True
    except ValueError:
        return False


def _contains_sensitive_material_dir(file_path: Path) -> bool:
    blocked_names = {"sandbox_cases", "real_cases", "case_workspaces"}
    parts = set(file_path.parts)
    return bool(parts & blocked_names)


def _repo_root() -> Path:
    return Path(__file__).resolve().parents[3]
