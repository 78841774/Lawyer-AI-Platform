from dataclasses import asdict
from typing import Any

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.repositories.experience_package_repository import ExperiencePackageRepository
from app.repositories.skill_registry_repository import SkillRegistryRepository
from app.repositories.skill_repository import SkillRepository
from app.services.skill_registry_service import SkillRegistryService

router = APIRouter(prefix="/skill-registry", tags=["skill-registry"])


def get_skill_registry_service(db: Session) -> SkillRegistryService:
    return SkillRegistryService(
        skill_registry_repository=SkillRegistryRepository(
            skill_repository=SkillRepository(db),
            experience_package_repository=ExperiencePackageRepository(db)
        )
    )


@router.get("")
def list_skill_registry(
    db: Session = Depends(get_db)
) -> dict[str, Any]:
    service = get_skill_registry_service(db)
    return {
        "skills": [
            asdict(entry)
            for entry in service.list_registry()
        ]
    }


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
    db: Session = Depends(get_db)
) -> dict[str, object]:
    service = get_skill_registry_service(db)
    try:
        return service.deprecate(skill_id)
    except ValueError as error:
        if str(error) == "skill not found":
            raise HTTPException(status_code=404, detail=str(error)) from error
        raise HTTPException(status_code=500, detail="skill deprecation failed") from error

