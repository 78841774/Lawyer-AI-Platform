import subprocess
from pathlib import Path
from typing import Any

from controlled_ocr_pipeline.schemas import ControlledOCRGuardResult, ControlledOCRPreviewRequest

ALLOWED_MODES = {"mock", "disabled", "local", "local_only", "controlled_local"}
DANGEROUS_MODES = {"live", "real", "deepseek_live", "deepseek", "production", "remote", "external"}
ALLOWED_FILE_EXTENSIONS = {".pdf", ".png", ".jpg", ".jpeg", ".txt"}
BLOCKED_FILE_EXTENSIONS = {".doc", ".docx", ".heic", ".xlsx", ".zip", ".rar", ".7z", ".eml", ".msg"}
MAX_FILE_SIZE_BYTES = 5000000
RUNTIME_STORAGE_PATH = "storage/runtime/controlled_ocr_previews"
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


def check_explicit_ocr_confirmation_gate(request: ControlledOCRPreviewRequest) -> dict[str, Any]:
    warnings = ["Explicit OCR confirmation is required before controlled OCR preview."]
    return ControlledOCRGuardResult(
        guard_name="explicit_ocr_confirmation_gate",
        allowed=request.explicit_ocr_confirmation,
        status="passed" if request.explicit_ocr_confirmation else "blocked",
        warnings=warnings,
    ).model_dump()


def check_manual_review_gate(request: ControlledOCRPreviewRequest) -> dict[str, Any]:
    warnings = ["Manual lawyer review confirmation is required."]
    return ControlledOCRGuardResult(
        guard_name="manual_review_gate",
        allowed=request.manual_review_confirmed,
        status="passed" if request.manual_review_confirmed else "blocked",
        warnings=warnings,
    ).model_dump()


def check_ocr_provider_gate(request: ControlledOCRPreviewRequest) -> dict[str, Any]:
    modes = {"ocr_mode": request.ocr_mode, "provider_mode": request.provider_mode}
    blocked_modes = [
        f"{name}={value}"
        for name, value in modes.items()
        if _normalize(value) in DANGEROUS_MODES or _normalize(value) not in ALLOWED_MODES
    ]
    warnings = [
        "Real OCR provider is blocked in v4.4.",
        "External OCR provider is blocked in v4.4.",
        "DeepSeek live provider is blocked in v4.4.",
    ]
    if any(_normalize(value) not in ALLOWED_MODES and _normalize(value) not in DANGEROUS_MODES for value in modes.values()):
        warnings.append("Unsupported OCR provider mode is blocked in v4.4.")
    return ControlledOCRGuardResult(
        guard_name="ocr_provider_gate",
        allowed=not blocked_modes,
        status="passed" if not blocked_modes else "blocked",
        warnings=warnings,
        metadata={"blocked_modes": blocked_modes, **modes},
    ).model_dump()


def check_ocr_local_file_path_guard(request: ControlledOCRPreviewRequest) -> dict[str, Any]:
    file_path = _resolve_local_file_path(request.local_file_path)
    warnings = [
        "Local OCR file path must exist and must be a file.",
        "Local OCR file path is always returned as <local_file_path_redacted>.",
        "Git repository internal files and runtime storage paths are blocked.",
    ]
    metadata = {"local_file_path_redacted": "<local_file_path_redacted>"}
    if file_path is None:
        return _guard("ocr_local_file_path_guard", False, [*warnings, "local_file_path is required."], metadata)
    metadata["file_extension"] = file_path.suffix.lower()
    if not file_path.exists():
        return _guard("ocr_local_file_path_guard", False, [*warnings, "Local OCR file does not exist."], metadata)
    if file_path.is_dir():
        return _guard("ocr_local_file_path_guard", False, [*warnings, "Local OCR file path must not be a directory."], metadata)
    blocked = _is_repo_internal(file_path) or _contains_sensitive_material_dir(file_path) or _is_runtime_storage_path(file_path)
    if blocked:
        warnings.append("Local OCR file path is blocked because it is inside the repository, runtime storage, or a blocked material directory.")
    return _guard("ocr_local_file_path_guard", not blocked, warnings, metadata)


def check_ocr_file_extension_guard(file_path: str | Path | None) -> dict[str, Any]:
    resolved = _resolve_local_file_path(file_path)
    extension = resolved.suffix.lower() if resolved else ""
    warnings = ["Only .pdf, .png, .jpg, .jpeg, and .txt are allowed for v4.4 controlled OCR preview."]
    if extension in {".pdf", ".png", ".jpg", ".jpeg"}:
        warnings.append("PDF and image files use mock OCR only; binary content is not read in v4.4.")
    if extension in BLOCKED_FILE_EXTENSIONS:
        warnings.append("Word, HEIC, spreadsheet, archive, and email files are blocked in v4.4.")
    if not extension:
        warnings.append("File extension is required.")
    return _guard("ocr_file_extension_guard", extension in ALLOWED_FILE_EXTENSIONS, warnings, {"file_extension": extension})


def check_ocr_file_size_guard(file_path: str | Path | None) -> dict[str, Any]:
    resolved = _resolve_local_file_path(file_path)
    warnings = [f"OCR preview file size must be at or below {MAX_FILE_SIZE_BYTES} bytes."]
    if resolved is None or not resolved.exists() or resolved.is_dir():
        return _guard(
            "ocr_file_size_guard",
            False,
            [*warnings, "File does not exist or is not a regular file."],
            {"max_file_size_bytes": MAX_FILE_SIZE_BYTES, "file_size_bytes": 0},
        )
    size = resolved.stat().st_size
    if size > MAX_FILE_SIZE_BYTES:
        warnings.append("File exceeds v4.4 controlled OCR preview size limit.")
    return _guard(
        "ocr_file_size_guard",
        size <= MAX_FILE_SIZE_BYTES,
        warnings,
        {"max_file_size_bytes": MAX_FILE_SIZE_BYTES, "file_size_bytes": size},
    )


def check_ocr_path_outside_repo_guard(file_path: str | Path | None) -> dict[str, Any]:
    resolved = _resolve_local_file_path(file_path)
    warnings = ["Controlled OCR preview files must be outside the Git repository."]
    inside_repo = bool(resolved and _is_repo_internal(resolved))
    return _guard(
        "ocr_path_outside_repo_guard",
        bool(resolved) and not inside_repo,
        warnings if resolved else [*warnings, "local_file_path is required."],
        {"local_file_path_redacted": "<local_file_path_redacted>"},
    )


def check_ocr_runtime_storage_guard() -> dict[str, Any]:
    warnings = [
        "Redacted OCR preview may only be stored in storage/runtime/controlled_ocr_previews.",
        "Controlled OCR runtime storage must be ignored by Git.",
        "Raw OCR text must not be stored in runtime storage.",
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
        return _guard("ocr_runtime_storage_guard", False, [*warnings, f"Runtime storage ignore check failed: {error}"], {"runtime_storage_path": RUNTIME_STORAGE_PATH})
    return _guard("ocr_runtime_storage_guard", check.returncode == 0, warnings, {"runtime_storage_path": RUNTIME_STORAGE_PATH})


def check_ocr_git_storage_guard() -> dict[str, Any]:
    warnings = [
        "OCR text must not enter Git.",
        "Real case materials must not enter Git.",
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
        return _guard("ocr_git_storage_guard", False, [*warnings, f"Git storage guard failed: {error}"], {})
    staged_sensitive = _staged_sensitive_paths(status_output)
    if staged_sensitive:
        warnings.append(f"Sensitive staged paths detected: {', '.join(staged_sensitive)}")
    return _guard("ocr_git_storage_guard", not staged_sensitive, warnings, {"staged_sensitive_paths": staged_sensitive})


def run_all_controlled_ocr_guards(request: ControlledOCRPreviewRequest) -> list[dict[str, Any]]:
    return [
        check_explicit_ocr_confirmation_gate(request),
        check_manual_review_gate(request),
        check_ocr_provider_gate(request),
        check_ocr_local_file_path_guard(request),
        check_ocr_file_extension_guard(request.local_file_path),
        check_ocr_file_size_guard(request.local_file_path),
        check_ocr_path_outside_repo_guard(request.local_file_path),
        check_ocr_runtime_storage_guard(),
        check_ocr_git_storage_guard(),
    ]


def _guard(guard_name: str, allowed: bool, warnings: list[str], metadata: dict[str, Any]) -> dict[str, Any]:
    return ControlledOCRGuardResult(
        guard_name=guard_name,
        allowed=allowed,
        status="passed" if allowed else "blocked",
        warnings=warnings,
        metadata=metadata,
    ).model_dump()


def _normalize(value: str | None) -> str:
    return (value or "").strip().lower()


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
    return bool(set(file_path.parts) & blocked_names)


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


def _repo_root() -> Path:
    return Path(__file__).resolve().parents[3]
