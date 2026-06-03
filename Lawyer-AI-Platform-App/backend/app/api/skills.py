import json
from typing import Any

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.models.skill import Skill
from app.repositories.case_repository import CaseRepository
from app.repositories.fact_repository import FactRepository
from app.repositories.legal_analysis_repository import LegalAnalysisRepository
from app.repositories.report_repository import ReportRepository
from app.repositories.skill_repository import SkillRepository
from app.services.skill_service import SkillService

router = APIRouter(tags=["skills"])


def get_skill_service(db: Session) -> SkillService:
    return SkillService(
        skill_repository=SkillRepository(db),
        case_repository=CaseRepository(db),
        fact_repository=FactRepository(db),
        legal_analysis_repository=LegalAnalysisRepository(db),
        report_repository=ReportRepository(db)
    )


def serialize_skill(skill: Skill) -> dict[str, Any]:
    return {
        "skill_id": skill.skill_id,
        "case_id": skill.case_id,
        "skill_name": skill.skill_name,
        "domain": skill.domain,
        "version": skill.version,
        "status": skill.status,
        "fact_patterns": json.loads(skill.fact_patterns),
        "reasoning_patterns": json.loads(skill.reasoning_patterns),
        "prompts": json.loads(skill.prompts),
        "templates": json.loads(skill.templates),
        "evaluation_score": skill.evaluation_score,
        "package_path": skill.package_path,
        "created_at": skill.created_at
    }


def serialize_skill_summary(skill: Skill) -> dict[str, Any]:
    return {
        "skill_id": skill.skill_id,
        "case_id": skill.case_id,
        "skill_name": skill.skill_name,
        "domain": skill.domain,
        "version": skill.version,
        "status": skill.status,
        "evaluation_score": skill.evaluation_score,
        "package_path": skill.package_path
    }


@router.post("/cases/{case_id}/skills/build")
def build_case_skill(
    case_id: str,
    db: Session = Depends(get_db)
) -> dict[str, Any]:
    service = get_skill_service(db)
    try:
        skill = service.build_skill(case_id)
    except ValueError as error:
        if str(error) == "case not found":
            raise HTTPException(status_code=404, detail=str(error)) from error
        if str(error) == "facts required":
            raise HTTPException(status_code=400, detail="case has no facts") from error
        if str(error) == "analysis required":
            raise HTTPException(status_code=400, detail="case has no legal analysis") from error
        if str(error) == "reports required":
            raise HTTPException(status_code=400, detail="case has no reports") from error
        raise HTTPException(status_code=500, detail="skill build failed") from error
    except Exception as error:
        raise HTTPException(status_code=500, detail="skill build failed") from error
    return serialize_skill_summary(skill)


@router.get("/skills")
def list_skills(db: Session = Depends(get_db)) -> dict[str, Any]:
    service = get_skill_service(db)
    return {
        "skills": [serialize_skill_summary(skill) for skill in service.list_skills()]
    }


@router.get("/skills/{skill_id}")
def get_skill(
    skill_id: str,
    db: Session = Depends(get_db)
) -> dict[str, Any]:
    service = get_skill_service(db)
    skill = service.get_skill(skill_id)
    if skill is None:
        raise HTTPException(status_code=404, detail="skill not found")
    return serialize_skill(skill)

