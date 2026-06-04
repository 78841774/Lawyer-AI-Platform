from dataclasses import asdict
from typing import Any

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.repositories.experience_package_repository import ExperiencePackageRepository
from app.repositories.skill_registry_repository import SkillRegistryRepository
from app.repositories.skill_repository import SkillRepository
from app.services.skill_registry_service import SkillRegistryService
from controlled_skill_registry_publish.publisher import (
    ControlledSkillRegistryPublishError,
    deprecate_controlled_skill,
    get_controlled_published_skill,
    list_controlled_published_skills,
    publish_experience_package_to_skill_registry,
    rollback_controlled_skill
)

router = APIRouter(prefix="/skill-registry", tags=["skill-registry"])


class PublishExperiencePackageRequest(BaseModel):
    experience_package_id: str
    workspace_scope: str = "local_demo_workspace"


class SkillLifecycleRequest(BaseModel):
    reason: str | None = None


def get_skill_registry_service(db: Session) -> SkillRegistryService:
    return SkillRegistryService(
        skill_registry_repository=SkillRegistryRepository(
            skill_repository=SkillRepository(db),
            experience_package_repository=ExperiencePackageRepository(db)
        )
    )


def handle_controlled_publish_error(error: ControlledSkillRegistryPublishError) -> HTTPException:
    message = str(error)
    if "not found" in message:
        return HTTPException(status_code=404, detail=message)
    return HTTPException(status_code=400, detail=message)


@router.get("")
def list_skill_registry(
    db: Session = Depends(get_db)
) -> dict[str, Any]:
    service = get_skill_registry_service(db)
    return {
        "skills": list_controlled_published_skills() + [
            asdict(entry)
            for entry in service.list_registry()
        ]
    }


@router.post("/publish")
def publish_experience_package(
    payload: PublishExperiencePackageRequest
) -> dict[str, Any]:
    try:
        return publish_experience_package_to_skill_registry(payload.experience_package_id, payload.workspace_scope)
    except ControlledSkillRegistryPublishError as error:
        raise handle_controlled_publish_error(error) from error


@router.get("/domains")
def list_skill_registry_domains(
    db: Session = Depends(get_db)
) -> dict[str, Any]:
    service = get_skill_registry_service(db)
    return {
        "domains": [
            asdict(domain)
            for domain in service.list_domains()
        ]
    }


@router.get("/{skill_id}")
def get_skill_registry_detail(
    skill_id: str,
    db: Session = Depends(get_db)
) -> dict[str, object]:
    try:
        return get_controlled_published_skill(skill_id)
    except ControlledSkillRegistryPublishError:
        pass
    service = get_skill_registry_service(db)
    try:
        return service.get_registry_detail(skill_id)
    except ValueError as error:
        if str(error) == "skill not found":
            raise HTTPException(status_code=404, detail=str(error)) from error
        raise HTTPException(status_code=500, detail="skill registry query failed") from error


@router.post("/{skill_id}/publish")
def publish_skill(
    skill_id: str,
    db: Session = Depends(get_db)
) -> dict[str, object]:
    service = get_skill_registry_service(db)
    try:
        return service.publish(skill_id)
    except ValueError as error:
        if str(error) == "skill not found":
            raise HTTPException(status_code=404, detail=str(error)) from error
        if str(error) in {
            "skill deprecated",
            "skill not validated",
            "package not built"
        }:
            raise HTTPException(status_code=400, detail=str(error)) from error
        raise HTTPException(status_code=500, detail="skill publish failed") from error


@router.post("/{skill_id}/deprecate")
def deprecate_skill(
    skill_id: str,
    payload: SkillLifecycleRequest | None = None,
    db: Session = Depends(get_db)
) -> dict[str, object]:
    try:
        return deprecate_controlled_skill(skill_id, payload.reason if payload else None)
    except ControlledSkillRegistryPublishError:
        pass
    service = get_skill_registry_service(db)
    try:
        return service.deprecate(skill_id)
    except ValueError as error:
        if str(error) == "skill not found":
            raise HTTPException(status_code=404, detail=str(error)) from error
        raise HTTPException(status_code=500, detail="skill deprecation failed") from error


@router.post("/{skill_id}/rollback")
def rollback_skill(
    skill_id: str,
    payload: SkillLifecycleRequest | None = None
) -> dict[str, object]:
    try:
        return rollback_controlled_skill(skill_id, payload.reason if payload else None)
    except ControlledSkillRegistryPublishError as error:
        raise handle_controlled_publish_error(error) from error
