import subprocess
from pathlib import Path
from typing import Any

from controlled_material_processing.schemas import (
    ControlledMaterialGuardResult,
    ControlledMaterialReadRequest,
    ControlledProviderGateResult,
)

ALLOWED_MODES = {"mock", "local", "local_only", "disabled", "controlled_local"}
DANGEROUS_MODES = {"live", "deepseek_live", "deepseek", "production", "remote", "external"}
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


def check_explicit_read_confirmation_gate(request: ControlledMaterialReadRequest) -> dict[str, Any]:
    warnings = ["Explicit read confirmation is required before controlled material processing."]
    return ControlledMaterialGuardResult(
        guard_name="explicit_read_confirmation_gate",
        allowed=request.explicit_read_confirmation,
        status="passed" if request.explicit_read_confirmation else "blocked",
        warnings=warnings,
    ).model_dump()


def check_manual_review_gate(request: ControlledMaterialReadRequest) -> dict[str, Any]:
    warnings = ["Manual lawyer review confirmation is required."]
    return ControlledMaterialGuardResult(
        guard_name="manual_review_gate",
        allowed=request.manual_review_confirmed,
        status="passed" if request.manual_review_confirmed else "blocked",
        warnings=warnings,
    ).model_dump()


def check_controlled_provider_gate(request: ControlledMaterialReadRequest) -> dict[str, Any]:
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
        "Live provider is blocked in v4.2 controlled local processing.",
        "DeepSeek live provider is blocked in v4.2 controlled local processing.",
        "External provider is blocked in v4.2 controlled local processing.",
    ]
    if any(_normalize(value) not in ALLOWED_MODES and _normalize(value) not in DANGEROUS_MODES for value in modes.values()):
        warnings.append("Unsupported provider mode is blocked in v4.2 controlled local processing.")
    return ControlledProviderGateResult(
        provider_mode=request.provider_mode,
        ocr_mode=request.ocr_mode,
        llm_mode=request.llm_mode,
        legal_search_mode=request.legal_search_mode,
        allowed=not blocked_modes,
        blocked_modes=blocked_modes,
        warnings=warnings,
    ).model_dump()


def check_material_content_read_guard(request: ControlledMaterialReadRequest) -> dict[str, Any]:
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


def _repo_root() -> Path:
    return Path(__file__).resolve().parents[3]
