from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[3]
RUNTIME_ROOT = REPO_ROOT / "Lawyer-AI-Platform-App/backend/storage/runtime"
RUNTIME_STORAGE_MODE = "ignored_runtime_storage"


def get_runtime_root() -> Path:
    return RUNTIME_ROOT


def ensure_runtime_path(path: Path) -> Path:
    resolved = path.resolve()
    if not is_path_under_runtime(resolved):
        raise ValueError("path is outside ignored runtime storage")
    return resolved


def is_path_under_runtime(path: Path) -> bool:
    try:
        path.resolve().relative_to(RUNTIME_ROOT.resolve())
        return True
    except ValueError:
        return False


def assert_runtime_storage_ignored(relative_path: str) -> bool:
    return relative_path.startswith("personal_alpha_") or relative_path.startswith("case_os")


def redacted_runtime_path(path: Path) -> str:
    ensure_runtime_path(path)
    return "redacted_runtime_path"
