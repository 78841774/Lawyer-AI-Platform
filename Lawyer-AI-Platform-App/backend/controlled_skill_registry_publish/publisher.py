import copy
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from experience_package_build.builder import (
    ExperiencePackageBuildError,
    get_experience_package_candidate,
    mark_candidate_published
)

BACKEND_ROOT = Path(__file__).resolve().parents[1]
REGISTRY_PATH = BACKEND_ROOT / "controlled_skill_registry_publish" / "registry.json"

_RUNTIME_SKILLS: dict[str, dict[str, Any]] = {}


class ControlledSkillRegistryPublishError(ValueError):
    """Raised when a controlled local Skill Registry publish is not allowed."""


def utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def load_registry() -> dict[str, Any]:
    try:
        data = json.loads(REGISTRY_PATH.read_text(encoding="utf-8"))
    except FileNotFoundError as error:
        raise ControlledSkillRegistryPublishError("controlled skill registry not found") from error
    except json.JSONDecodeError as error:
        raise ControlledSkillRegistryPublishError("controlled skill registry invalid") from error
    if not isinstance(data, dict):
        raise ControlledSkillRegistryPublishError("controlled skill registry payload invalid")
    return data


def seed_skills() -> list[dict[str, Any]]:
    skills = load_registry().get("published_skills", [])
    if not isinstance(skills, list):
        raise ControlledSkillRegistryPublishError("controlled skill registry published_skills must be a list")
    return [copy.deepcopy(skill) for skill in skills if isinstance(skill, dict)]


def list_controlled_published_skills() -> list[dict[str, Any]]:
    merged = {skill["skill_id"]: skill for skill in seed_skills()}
    merged.update({key: copy.deepcopy(value) for key, value in _RUNTIME_SKILLS.items()})
    return list(merged.values())


def get_controlled_published_skill(skill_id: str) -> dict[str, Any]:
    if skill_id in _RUNTIME_SKILLS:
        return copy.deepcopy(_RUNTIME_SKILLS[skill_id])
    for skill in seed_skills():
        if skill.get("skill_id") == skill_id:
            return skill
    raise ControlledSkillRegistryPublishError("controlled skill registry record not found")


def skill_id_for_candidate(candidate: dict[str, Any]) -> str:
    case_cause_code = str(candidate.get("case_cause_code") or "unknown").replace("-", "_")
    return f"skill_{case_cause_code}_v1_0_0"


def assert_candidate_publishable(candidate: dict[str, Any]) -> None:
    review = candidate.get("review", {})
    safety = candidate.get("safety", {})
    if candidate.get("status") != "candidate":
        raise ControlledSkillRegistryPublishError("experience package must be candidate")
    if not isinstance(review, dict) or review.get("requires_human_review") is not True:
        raise ControlledSkillRegistryPublishError("human review is required")
    if review.get("review_status") != "approved":
        raise ControlledSkillRegistryPublishError("experience package review must be approved")
    if not isinstance(safety, dict) or safety.get("can_publish_to_skill_registry") is not True:
        raise ControlledSkillRegistryPublishError("experience package cannot publish to skill registry")
    if safety.get("auto_publish_enabled") is True:
        raise ControlledSkillRegistryPublishError("auto publish must be disabled")
    if candidate.get("skill_registry_published") is True:
        raise ControlledSkillRegistryPublishError("experience package already published")
    if candidate.get("llm_called") is True:
        raise ControlledSkillRegistryPublishError("experience package called LLM")
    if candidate.get("real_case_material_used") is True:
        raise ControlledSkillRegistryPublishError("experience package used real case material")


def publish_experience_package_to_skill_registry(
    experience_package_id: str,
    workspace_scope: str = "local_demo_workspace"
) -> dict[str, Any]:
    try:
        candidate = get_experience_package_candidate(experience_package_id)
    except ExperiencePackageBuildError as error:
        raise ControlledSkillRegistryPublishError(str(error)) from error
    assert_candidate_publishable(candidate)
    skill_id = skill_id_for_candidate(candidate)
    if any(skill.get("skill_id") == skill_id for skill in list_controlled_published_skills()):
        raise ControlledSkillRegistryPublishError("controlled skill registry record already exists")

    skill = {
        "skill_id": skill_id,
        "source_experience_package_id": experience_package_id,
        "source_run_id": candidate["source_run_id"],
        "source_package_id": candidate["source_package_id"],
        "case_cause_code": candidate["case_cause_code"],
        "status": "published_local",
        "version": "1.0.0",
        "publish_mode": "controlled_local_publish",
        "workspace_scope": workspace_scope or "local_demo_workspace",
        "llm_called": False,
        "real_case_material_used": False,
        "published_at": utc_now(),
        "review": {
            "requires_human_review": True,
            "review_status": "approved",
            "reviewed_by": candidate["review"].get("reviewed_by")
        },
        "inheritance_chain": candidate.get("inheritance_chain", []),
        "taxonomy_path": candidate.get("taxonomy_path", []),
        "safety": {
            "auto_publish_enabled": False,
            "controlled_publish": True,
            "rollback_supported": True,
            "deprecate_supported": True,
            "child_package_cannot_disable_safety_rules": True
        },
        "runtime": {
            "workspace_runtime_enabled": False,
            "skill_aware_case_processing_enabled": False,
            "requires_manual_enablement": True
        },
        "events": []
    }
    _RUNTIME_SKILLS[skill_id] = copy.deepcopy(skill)
    mark_candidate_published(experience_package_id, skill_id)
    return skill


def append_skill_event(skill_id: str, status: str, event_type: str, reason: str | None = None) -> dict[str, Any]:
    skill = get_controlled_published_skill(skill_id)
    skill["status"] = status
    events = skill.get("events", [])
    if not isinstance(events, list):
        events = []
    events.append({
        "event": event_type,
        "reason": reason or "",
        "created_at": utc_now()
    })
    skill["events"] = events
    _RUNTIME_SKILLS[skill_id] = copy.deepcopy(skill)
    return skill


def deprecate_controlled_skill(skill_id: str, reason: str | None = None) -> dict[str, Any]:
    return append_skill_event(skill_id, "deprecated", "deprecated", reason)


def rollback_controlled_skill(skill_id: str, reason: str | None = None) -> dict[str, Any]:
    return append_skill_event(skill_id, "rolled_back", "rollback", reason)
