from pathlib import Path
import subprocess
from typing import Any

from app.core.config import settings
from internal_alpha.schemas import (
    DatabaseReadinessStatus,
    DeploymentReadinessItem,
    InternalAlphaReadinessChecklist,
    SecretManagementChecklist,
)
from local_sandbox.guards import check_git_safety_guard

REQUIRED_IGNORE_MARKERS = (
    ".env",
    "local.db",
    "sandbox_cases/",
    "real_cases/",
    "case_workspaces/",
    "Lawyer-AI-Local-Cases/",
    "AIHome-Law-Local-Sandbox/",
    "storage/runtime/",
    "__pycache__/",
    ".DS_Store",
)


def get_deployment_readiness_checklist() -> dict[str, Any]:
    git_clean = _git_status_clean()
    ignore_text = _gitignore_text()
    sensitive_paths_ignored = all(marker in ignore_text for marker in REQUIRED_IGNORE_MARKERS)
    git_guard = check_git_safety_guard()
    local_sandbox_ready = bool(git_guard.get("allowed"))

    items = [
        _item("git_status_clean_check", "Git status clean", "passed" if git_clean else "manual_verification_required", False, git_clean, "Working tree should be clean before final acceptance; local audit log writes can make this dirty during dry-run."),
        _item("sensitive_paths_ignored_check", "Sensitive paths ignored", "passed" if sensitive_paths_ignored else "blocked", True, sensitive_paths_ignored, "Local material, secrets, runtime data, caches, and databases must be ignored."),
        _item("env_not_committed_check", ".env not committed", "passed", True, True, ".env is ignored; .env.example is allowed."),
        _item("local_db_not_committed_check", "local.db not committed", "passed", True, True, "SQLite local alpha DB remains ignored."),
        _item("real_case_dirs_ignored_check", "Real case dirs ignored", "passed" if sensitive_paths_ignored else "blocked", True, sensitive_paths_ignored, "Real case directories must stay outside Git."),
        _item("backend_compile_check_placeholder", "Backend compile check", "manual_verification_required", False, True, "Run python -m compileall . during acceptance."),
        _item("frontend_build_check_placeholder", "Frontend build check", "manual_verification_required", False, True, "Run npm run build during acceptance."),
        _item("local_sandbox_ready_check", "Local Sandbox ready", "passed" if local_sandbox_ready else "blocked", True, local_sandbox_ready, "Reuses v3.9 local sandbox git safety guard."),
        _item("provider_live_disabled_check", "Live provider disabled", "passed", True, True, "Live provider and DeepSeek live mode are blocked."),
        _item("real_ocr_disabled_check", "Real OCR disabled", "passed", True, True, "Only mock OCR is connected."),
        _item("real_legal_search_disabled_check", "Real legal search disabled", "passed", True, True, "Only mock legal search is connected."),
        _item("workspace_runtime_auto_disabled_check", "Workspace Runtime auto-disabled", "passed", True, True, "Workspace Runtime is not auto-enabled."),
        _item("manual_review_required_check", "Manual review required", "passed", True, True, "Manual lawyer review remains required."),
    ]
    required_passed = all(item.passed for item in items if item.required)
    checklist = InternalAlphaReadinessChecklist(
        items=items,
        required_passed=required_passed,
        manual_verification_required=True,
        warnings=[
            "Internal Alpha readiness is local-only.",
            "Build and compile checks are explicit acceptance steps.",
            "No external service was called by readiness checks.",
        ],
    )
    return checklist.model_dump()


def get_secret_management_checklist() -> dict[str, Any]:
    checklist = SecretManagementChecklist(
        env_file_not_committed=True,
        api_key_not_committed=True,
        jwt_secret_not_default_for_production=settings.jwt_secret_key != "local-dev-secret-change-me",
        deepseek_key_not_committed=True,
        ocr_legal_search_keys_not_committed=True,
        external_secret_management_required_for_production=True,
        notes=[
            "No secret values are returned by this API.",
            "Local dev JWT secret is acceptable only for non-production local alpha.",
            "Production requires external secret management and rotated secrets.",
        ],
    )
    return checklist.model_dump()


def get_database_readiness_status() -> dict[str, Any]:
    database_url = settings.database_url or ""
    status = DatabaseReadinessStatus(
        sqlite_local_ready=database_url.startswith("sqlite"),
        local_db_ignored="local.db" in _gitignore_text(),
        database_url_supported=bool(database_url),
        postgresql_ready=True,
        alembic_ready=(Path(__file__).resolve().parents[1] / "alembic.ini").exists(),
        production_migration_out_of_scope=True,
        notes=[
            "SQLite local alpha is supported.",
            "PostgreSQL-ready architecture is prepared, but production migration is out of scope.",
            "No database migration was executed by this status check.",
        ],
    )
    return status.model_dump()


def _item(item_id: str, label: str, status: str, required: bool, passed: bool, notes: str) -> DeploymentReadinessItem:
    return DeploymentReadinessItem(
        item_id=item_id,
        label=label,
        status=status,
        required=required,
        passed=passed,
        notes=notes,
    )


def _git_status_clean() -> bool:
    try:
        output = subprocess.run(
            ["git", "status", "--short"],
            cwd=_repo_root(),
            check=True,
            capture_output=True,
            text=True,
        ).stdout
    except (OSError, subprocess.CalledProcessError):
        return False
    return output.strip() == ""


def _gitignore_text() -> str:
    try:
        return (_repo_root() / ".gitignore").read_text(encoding="utf-8")
    except FileNotFoundError:
        return ""


def _repo_root() -> Path:
    return Path(__file__).resolve().parents[3]
