from typing import Any

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from controlled_skill_registry_publish.publisher import (
    ControlledSkillRegistryPublishError,
    deprecate_controlled_skill,
    get_controlled_published_skill,
    list_controlled_published_skills,
    publish_experience_package_to_skill_registry,
    rollback_controlled_skill
)

router = APIRouter(tags=["controlled-skill-registry-publish"])


class PublishExperiencePackageRequest(BaseModel):
    experience_package_id: str
    workspace_scope: str = "local_demo_workspace"


class SkillLifecycleRequest(BaseModel):
    reason: str | None = None


def handle_publish_error(error: ControlledSkillRegistryPublishError) -> HTTPException:
    message = str(error)
    if "not found" in message:
        return HTTPException(status_code=404, detail=message)
    return HTTPException(status_code=400, detail=message)


@router.get("/controlled-skill-registry")
def list_controlled_skills_endpoint() -> dict[str, Any]:
    return {"skills": list_controlled_published_skills()}


@router.get("/controlled-skill-registry/{skill_id}")
def get_controlled_skill_endpoint(skill_id: str) -> dict[str, Any]:
    try:
        return get_controlled_published_skill(skill_id)
    except ControlledSkillRegistryPublishError as error:
        raise handle_publish_error(error) from error


@router.post("/controlled-skill-registry/publish")
def publish_controlled_skill_endpoint(payload: PublishExperiencePackageRequest) -> dict[str, Any]:
    try:
        return publish_experience_package_to_skill_registry(payload.experience_package_id, payload.workspace_scope)
    except ControlledSkillRegistryPublishError as error:
        raise handle_publish_error(error) from error


@router.post("/controlled-skill-registry/{skill_id}/deprecate")
def deprecate_controlled_skill_endpoint(skill_id: str, payload: SkillLifecycleRequest) -> dict[str, Any]:
    try:
        return deprecate_controlled_skill(skill_id, payload.reason)
    except ControlledSkillRegistryPublishError as error:
        raise handle_publish_error(error) from error


@router.post("/controlled-skill-registry/{skill_id}/rollback")
def rollback_controlled_skill_endpoint(skill_id: str, payload: SkillLifecycleRequest) -> dict[str, Any]:
    try:
        return rollback_controlled_skill(skill_id, payload.reason)
    except ControlledSkillRegistryPublishError as error:
        raise handle_publish_error(error) from error
