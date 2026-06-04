import json
from pathlib import Path
from typing import Any

from fastapi import APIRouter, HTTPException

router = APIRouter(tags=["versioned-skill-training-packages"])

BACKEND_ROOT = Path(__file__).resolve().parents[2]
PACKAGES_ROOT = BACKEND_ROOT / "versioned_skill_training_packages"
REGISTRY_PATH = PACKAGES_ROOT / "registry.json"


def load_json_file(path: Path) -> dict[str, Any]:
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError as error:
        raise HTTPException(status_code=404, detail="versioned training package not found") from error
    except json.JSONDecodeError as error:
        raise HTTPException(status_code=500, detail="versioned training package registry invalid") from error
    if not isinstance(data, dict):
        raise HTTPException(status_code=500, detail="versioned training package payload invalid")
    return data


def load_registry() -> dict[str, Any]:
    return load_json_file(REGISTRY_PATH)


def find_package_entry(package_id: str) -> dict[str, Any]:
    registry = load_registry()
    packages = registry.get("packages", [])
    if not isinstance(packages, list):
        raise HTTPException(status_code=500, detail="versioned training package registry invalid")
    for package in packages:
        if isinstance(package, dict) and package.get("training_package_id") == package_id:
            return package
    raise HTTPException(status_code=404, detail="versioned training package not found")


def safe_package_metadata_path(package: dict[str, Any]) -> Path:
    raw_path = package.get("path")
    if not isinstance(raw_path, str) or not raw_path:
        raise HTTPException(status_code=500, detail="versioned training package path invalid")
    candidate = (PACKAGES_ROOT / raw_path).resolve()
    packages_root = PACKAGES_ROOT.resolve()
    if packages_root != candidate and packages_root not in candidate.parents:
        raise HTTPException(status_code=400, detail="invalid versioned training package path")
    if candidate.name != "metadata.json":
        raise HTTPException(status_code=500, detail="versioned training package metadata path invalid")
    return candidate


def package_dir(package: dict[str, Any]) -> Path:
    return safe_package_metadata_path(package).parent


def read_readme_summary(directory: Path) -> str:
    readme_path = directory / "README.md"
    if not readme_path.exists():
        return ""
    text = readme_path.read_text(encoding="utf-8")
    return text[:4000]


def list_package_files(directory: Path) -> list[dict[str, Any]]:
    files: list[dict[str, Any]] = []
    for path in sorted(directory.rglob("*")):
        if not path.is_file():
            continue
        relative_path = path.relative_to(directory).as_posix()
        if relative_path.startswith(".") or "/." in relative_path:
            continue
        files.append(
            {
                "path": relative_path,
                "size": path.stat().st_size
            }
        )
    return files


@router.get("/versioned-skill-training-packages")
def list_versioned_skill_training_packages() -> dict[str, Any]:
    registry = load_registry()
    return {
        "schema_version": registry.get("schema_version"),
        "status": registry.get("status"),
        "registry_status": registry.get("registry_status"),
        "packages": registry.get("packages", [])
    }


@router.get("/versioned-skill-training-packages/{package_id}")
def get_versioned_skill_training_package(package_id: str) -> dict[str, Any]:
    package = find_package_entry(package_id)
    metadata_path = safe_package_metadata_path(package)
    metadata = load_json_file(metadata_path)
    directory = metadata_path.parent
    return {
        "package": package,
        "metadata": metadata,
        "readme": read_readme_summary(directory)
    }


@router.get("/versioned-skill-training-packages/{package_id}/files")
def get_versioned_skill_training_package_files(package_id: str) -> dict[str, Any]:
    package = find_package_entry(package_id)
    directory = package_dir(package)
    return {
        "training_package_id": package_id,
        "files": list_package_files(directory)
    }
