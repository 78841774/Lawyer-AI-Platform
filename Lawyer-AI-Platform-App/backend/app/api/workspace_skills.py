from typing import Any

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.models.case_skill_binding import CaseSkillBinding
from app.models.experience_package import ExperiencePackage
from app.models.skill import Skill
from app.repositories.case_repository import CaseRepository
from app.repositories.skill_repository import SkillRepository
from app.repositories.workspace_skill_repository import WorkspaceSkillRepository
from app.services.skill_runtime_service import SkillRuntimeService
from app.services.workspace_skill_service import WorkspaceSkillService

router = APIRouter(tags=["workspace-skills"])


def get_workspace_skill_service(db: Session) -> WorkspaceSkillService:
    return WorkspaceSkillService(
        workspace_skill_repository=WorkspaceSkillRepository(db),
        case_repository=CaseRepository(db),
        skill_repository=SkillRepository(db)
    )


def get_skill_runtime_service(db: Session) -> SkillRuntimeService:
    return SkillRuntimeService(
        skill_repository=SkillRepository(db),
        workspace_skill_repository=WorkspaceSkillRepository(db)
    )


def serialize_workspace_skill(
    skill: Skill,
    package: ExperiencePackage
) -> dict[str, Any]:
    return {
        "skill_id": skill.skill_id,
        "skill_name": skill.skill_name,
        "domain": skill.domain,
        "version": skill.version,
        "package_id": package.package_id,
        "package_path": package.package_path,
        "status": skill.status
    }


def serialize_binding(binding: CaseSkillBinding) -> dict[str, Any]:
    return {
        "case_id": binding.case_id,
        "skill_id": binding.skill_id,
        "package_id": binding.package_id,
        "status": binding.status,
        "message": "Skill applied to case workspace"
    }


@router.get("/workspace/skills")
def list_workspace_skills(
    db: Session = Depends(get_db)
) -> dict[str, Any]:
    service = get_workspace_skill_service(db)
    return {
        "skills": [
            serialize_workspace_skill(skill, package)
            for skill, package in service.list_workspace_skills()
        ]
    }


@router.get("/workspace/skills/{skill_id}/runtime")
def get_workspace_skill_runtime(
    skill_id: str,
    db: Session = Depends(get_db)
) -> dict[str, object]:
    service = get_skill_runtime_service(db)
    try:
        return service.get_runtime_summary(skill_id)
    except ValueError as error:
        if str(error) == "skill not found":
            raise HTTPException(status_code=404, detail=str(error)) from error
        if str(error) == "skill not published":
            raise HTTPException(status_code=400, detail=str(error)) from error
        if str(error) == "package not published":
            raise HTTPException(status_code=400, detail=str(error)) from error
        if str(error).startswith("package"):
            raise HTTPException(status_code=400, detail=str(error)) from error
        raise HTTPException(status_code=500, detail="skill runtime load failed") from error


@router.get("/workspace/skills/{skill_id}")
def get_workspace_skill(
    skill_id: str,
    db: Session = Depends(get_db)
) -> dict[str, object]:
    service = get_workspace_skill_service(db)
    try:
        skill, package = service.get_workspace_skill(skill_id)
    except ValueError as error:
        if str(error) == "skill not found":
            raise HTTPException(status_code=404, detail=str(error)) from error
        if str(error) == "skill not published":
            raise HTTPException(status_code=400, detail=str(error)) from error
        raise HTTPException(status_code=500, detail="workspace skill query failed") from error
    return service.build_skill_detail(skill=skill, package=package)


@router.post("/cases/{case_id}/skills/{skill_id}/apply")
def apply_skill_to_case(
    case_id: str,
    skill_id: str,
    db: Session = Depends(get_db)
) -> dict[str, Any]:
    service = get_workspace_skill_service(db)
    try:
        binding = service.apply_skill_to_case(case_id=case_id, skill_id=skill_id)
    except ValueError as error:
        if str(error) in {"case not found", "skill not found"}:
            raise HTTPException(status_code=404, detail=str(error)) from error
        if str(error) == "skill not published":
            raise HTTPException(status_code=400, detail=str(error)) from error
        raise HTTPException(status_code=500, detail="skill apply failed") from error
    return serialize_binding(binding)


@router.get("/cases/{case_id}/skills")
def list_case_skills(
    case_id: str,
    db: Session = Depends(get_db)
) -> dict[str, Any]:
    service = get_workspace_skill_service(db)
    try:
        skills = service.list_case_skills(case_id)
    except ValueError as error:
        if str(error) == "case not found":
            raise HTTPException(status_code=404, detail=str(error)) from error
        raise HTTPException(status_code=500, detail="case skills query failed") from error
    return {
        "case_id": case_id,
        "skills": skills
    }
