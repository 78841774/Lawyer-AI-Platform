import json
from pathlib import Path
from typing import Any

BACKEND_ROOT = Path(__file__).resolve().parents[1]
PACKAGES_REGISTRY_PATH = BACKEND_ROOT / "versioned_skill_training_packages" / "registry.json"
TAXONOMY_REGISTRY_PATH = BACKEND_ROOT / "case_cause_taxonomy" / "registry.json"
RUNS_REGISTRY_PATH = BACKEND_ROOT / "versioned_skill_training_runs" / "registry.json"
MOCK_TIMESTAMP = "2026-06-04T00:00:00Z"


class MockTrainingRunError(ValueError):
    """Raised when a mock training run cannot be prepared from local registries."""


def load_json_file(path: Path) -> dict[str, Any]:
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError as error:
        raise MockTrainingRunError(f"missing registry: {path}") from error
    except json.JSONDecodeError as error:
        raise MockTrainingRunError(f"invalid registry json: {path}") from error
    if not isinstance(data, dict):
        raise MockTrainingRunError(f"registry payload must be an object: {path}")
    return data


def registry_packages() -> list[dict[str, Any]]:
    packages = load_json_file(PACKAGES_REGISTRY_PATH).get("packages", [])
    if not isinstance(packages, list):
        raise MockTrainingRunError("versioned training package registry packages must be a list")
    return [package for package in packages if isinstance(package, dict)]


def taxonomy_entries() -> list[dict[str, Any]]:
    entries = load_json_file(TAXONOMY_REGISTRY_PATH).get("case_causes", [])
    if not isinstance(entries, list):
        raise MockTrainingRunError("case cause taxonomy registry case_causes must be a list")
    return [entry for entry in entries if isinstance(entry, dict)]


def registry_runs() -> list[dict[str, Any]]:
    runs = load_json_file(RUNS_REGISTRY_PATH).get("runs", [])
    if not isinstance(runs, list):
        raise MockTrainingRunError("versioned skill training run registry runs must be a list")
    return [run for run in runs if isinstance(run, dict)]


def find_package(package_id: str) -> dict[str, Any]:
    for package in registry_packages():
        if package.get("training_package_id") == package_id:
            return package
    raise MockTrainingRunError(f"versioned training package not found: {package_id}")


def find_taxonomy_path(case_cause_code: str, fallback: list[str]) -> list[str]:
    for entry in taxonomy_entries():
        if entry.get("case_cause_code") == case_cause_code:
            path = entry.get("path", [])
            if isinstance(path, list) and all(isinstance(item, str) for item in path):
                return path
    return fallback


def normalize_run_id(package_id: str) -> str:
    if package_id == "sales_contract_payment_dispute@v1.0.0":
        return "training_run_payment_dispute_mock_001"
    return "training_run_" + package_id.replace("@", "_").replace(".", "_").replace("-", "_") + "_mock_001"


def find_seed_run_by_package(package_id: str) -> dict[str, Any] | None:
    for run in registry_runs():
        if run.get("package_id") == package_id:
            return run
    return None


def create_mock_training_run(package_id: str) -> dict[str, Any]:
    package = find_package(package_id)
    seed_run = find_seed_run_by_package(package_id)
    case_cause_code = package.get("case_cause_code")
    if not isinstance(case_cause_code, str) or not case_cause_code:
        raise MockTrainingRunError(f"package missing case_cause_code: {package_id}")

    package_path = package.get("case_cause_path", [])
    fallback_path = package_path if isinstance(package_path, list) else []
    taxonomy_path = find_taxonomy_path(case_cause_code, [item for item in fallback_path if isinstance(item, str)])
    inheritance_chain = package.get("inheritance_order", [])
    if not isinstance(inheritance_chain, list):
        inheritance_chain = [package_id]

    return {
        "run_id": seed_run.get("run_id") if seed_run else normalize_run_id(package_id),
        "package_id": package_id,
        "case_cause_code": case_cause_code,
        "status": "completed_mock",
        "runner": "mock_training_runner",
        "llm_provider": "mock",
        "llm_called": False,
        "started_at": seed_run.get("started_at", MOCK_TIMESTAMP) if seed_run else MOCK_TIMESTAMP,
        "completed_at": seed_run.get("completed_at", MOCK_TIMESTAMP) if seed_run else MOCK_TIMESTAMP,
        "inheritance_chain": [item for item in inheritance_chain if isinstance(item, str)] or [package_id],
        "taxonomy_path": taxonomy_path,
        "inputs": {
            "source": "versioned_training_package",
            "real_case_material_used": False,
            "legacy_asset_modified": False
        },
        "outputs": {
            "skill_candidate_created": False,
            "experience_package_created": False,
            "skill_registry_published": False
        },
        "mock_evaluation": {
            "accuracy": 0.0,
            "consistency": 0.0,
            "completeness": 0.0,
            "legal_relevance": 0.0,
            "report_quality": 0.0,
            "notes": "Mock training run only. No LLM call. No real case material used."
        },
        "safety": {
            "requires_human_review": True,
            "auto_train_enabled": False,
            "auto_publish_enabled": False,
            "child_package_cannot_disable_safety_rules": True
        }
    }
