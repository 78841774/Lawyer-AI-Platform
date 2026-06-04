import copy
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from versioned_skill_training_runs.runner import (
    MockTrainingRunError,
    create_mock_training_run,
    normalize_run_id,
    registry_packages,
    registry_runs
)

BACKEND_ROOT = Path(__file__).resolve().parents[1]
REGISTRY_PATH = BACKEND_ROOT / "experience_package_build" / "registry.json"
MOCK_TIMESTAMP = "2026-06-04T00:00:00Z"
ALLOWED_REVIEW_STATUS = {"pending", "approved", "rejected", "needs_revision"}

_RUNTIME_CANDIDATES: dict[str, dict[str, Any]] = {}


class ExperiencePackageBuildError(ValueError):
    """Raised when a mock Experience Package Candidate cannot be created."""


def utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def load_registry() -> dict[str, Any]:
    try:
        data = json.loads(REGISTRY_PATH.read_text(encoding="utf-8"))
    except FileNotFoundError as error:
        raise ExperiencePackageBuildError("experience package candidate registry not found") from error
    except json.JSONDecodeError as error:
        raise ExperiencePackageBuildError("experience package candidate registry invalid") from error
    if not isinstance(data, dict):
        raise ExperiencePackageBuildError("experience package candidate registry payload invalid")
    return data


def seed_candidates() -> list[dict[str, Any]]:
    candidates = load_registry().get("experience_packages", [])
    if not isinstance(candidates, list):
        raise ExperiencePackageBuildError("experience package candidate registry items must be a list")
    return [copy.deepcopy(candidate) for candidate in candidates if isinstance(candidate, dict)]


def list_experience_package_candidates() -> list[dict[str, Any]]:
    merged = {candidate["experience_package_id"]: candidate for candidate in seed_candidates()}
    merged.update({key: copy.deepcopy(value) for key, value in _RUNTIME_CANDIDATES.items()})
    return list(merged.values())


def get_experience_package_candidate(experience_package_id: str) -> dict[str, Any]:
    if experience_package_id in _RUNTIME_CANDIDATES:
        return copy.deepcopy(_RUNTIME_CANDIDATES[experience_package_id])
    for candidate in seed_candidates():
        if candidate.get("experience_package_id") == experience_package_id:
            return candidate
    raise ExperiencePackageBuildError("experience package candidate not found")


def find_training_run(run_id: str) -> dict[str, Any]:
    for run in registry_runs():
        if run.get("run_id") == run_id:
            return copy.deepcopy(run)
    for package in registry_packages():
        package_id = package.get("training_package_id")
        if isinstance(package_id, str) and normalize_run_id(package_id) == run_id:
            return create_mock_training_run(package_id)
    raise ExperiencePackageBuildError("training run not found")


def assert_safe_training_run(run: dict[str, Any]) -> None:
    if run.get("status") != "completed_mock":
        raise ExperiencePackageBuildError("training run must be completed_mock")
    if run.get("llm_called") is True:
        raise ExperiencePackageBuildError("training run called LLM")
    inputs = run.get("inputs", {})
    outputs = run.get("outputs", {})
    if isinstance(inputs, dict) and inputs.get("real_case_material_used") is True:
        raise ExperiencePackageBuildError("training run used real case material")
    if isinstance(outputs, dict) and outputs.get("skill_registry_published") is True:
        raise ExperiencePackageBuildError("training run already published skill registry")


def candidate_id_for_run(run: dict[str, Any]) -> str:
    case_cause_code = run.get("case_cause_code")
    if case_cause_code == "payment_dispute":
        return "experience_package_payment_dispute_candidate_001"
    safe_code = str(case_cause_code or "unknown").replace("-", "_")
    return f"experience_package_{safe_code}_candidate_001"


def create_experience_package_candidate(run_id: str) -> dict[str, Any]:
    run = find_training_run(run_id)
    assert_safe_training_run(run)
    candidate = {
        "experience_package_id": candidate_id_for_run(run),
        "source_run_id": run["run_id"],
        "source_package_id": run["package_id"],
        "case_cause_code": run["case_cause_code"],
        "status": "candidate",
        "build_mode": "mock_candidate_build",
        "llm_called": False,
        "real_case_material_used": False,
        "skill_registry_published": False,
        "published_skill_id": None,
        "created_at": run.get("completed_at", MOCK_TIMESTAMP),
        "inheritance_chain": run.get("inheritance_chain", []),
        "taxonomy_path": run.get("taxonomy_path", []),
        "package_contents": {
            "runtime_rules_included": True,
            "prompt_templates_included": True,
            "report_templates_included": True,
            "evaluation_rubrics_included": True,
            "reference_assets_included": True,
            "real_case_material_included": False
        },
        "review": {
            "requires_human_review": True,
            "review_status": "pending",
            "reviewed_by": None,
            "reviewed_at": None
        },
        "safety": {
            "auto_publish_enabled": False,
            "can_publish_to_skill_registry": False,
            "child_package_cannot_disable_safety_rules": True
        }
    }
    _RUNTIME_CANDIDATES[candidate["experience_package_id"]] = copy.deepcopy(candidate)
    return candidate


def review_experience_package_candidate(
    experience_package_id: str,
    review_status: str,
    reviewed_by: str | None = None
) -> dict[str, Any]:
    if review_status not in ALLOWED_REVIEW_STATUS:
        raise ExperiencePackageBuildError("review_status invalid")
    candidate = get_experience_package_candidate(experience_package_id)
    candidate["review"]["requires_human_review"] = True
    candidate["review"]["review_status"] = review_status
    candidate["review"]["reviewed_by"] = reviewed_by
    candidate["review"]["reviewed_at"] = utc_now() if review_status != "pending" else None
    candidate["safety"]["auto_publish_enabled"] = False
    candidate["safety"]["can_publish_to_skill_registry"] = review_status == "approved"
    candidate["safety"]["child_package_cannot_disable_safety_rules"] = True
    candidate["skill_registry_published"] = False
    candidate["llm_called"] = False
    candidate["real_case_material_used"] = False
    _RUNTIME_CANDIDATES[experience_package_id] = copy.deepcopy(candidate)
    return candidate


def mark_candidate_published(experience_package_id: str, skill_id: str) -> dict[str, Any]:
    candidate = get_experience_package_candidate(experience_package_id)
    candidate["skill_registry_published"] = True
    candidate["published_skill_id"] = skill_id
    candidate["llm_called"] = False
    candidate["real_case_material_used"] = False
    candidate["safety"]["auto_publish_enabled"] = False
    _RUNTIME_CANDIDATES[experience_package_id] = copy.deepcopy(candidate)
    return candidate
