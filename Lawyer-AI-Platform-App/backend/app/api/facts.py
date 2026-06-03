from typing import Any

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.models.fact import Fact
from app.repositories.case_repository import CaseRepository
from app.repositories.fact_repository import FactRepository
from app.repositories.material_repository import MaterialRepository
from app.repositories.skill_repository import SkillRepository
from app.repositories.workspace_skill_repository import WorkspaceSkillRepository
from app.services.fact_service import FactService
from app.services.skill_runtime_service import SkillRuntimeService

router = APIRouter(prefix="/cases/{case_id}/facts", tags=["facts"])


def get_fact_service(db: Session) -> FactService:
    return FactService(
        fact_repository=FactRepository(db),
        material_repository=MaterialRepository(db),
        case_repository=CaseRepository(db),
        skill_runtime_service=SkillRuntimeService(
            skill_repository=SkillRepository(db),
            workspace_skill_repository=WorkspaceSkillRepository(db)
        )
    )


def serialize_fact(fact: Fact) -> dict[str, Any]:
    return {
        "fact_id": fact.fact_id,
        "case_id": fact.case_id,
        "material_id": fact.material_id,
        "content": fact.content,
        "fact_type": fact.fact_type,
        "confidence": fact.confidence,
        "source_text": fact.source_text,
        "status": fact.status,
        "created_at": fact.created_at
    }


def is_runtime_error(error: ValueError) -> bool:
    message = str(error)
    return (
        message
        in {
            "skill not found",
            "skill not published",
            "package not found",
            "package not published"
        }
        or message.startswith("package file")
    )


@router.post("/extract")
def extract_facts(
    case_id: str,
    db: Session = Depends(get_db)
) -> dict[str, Any]:
    service = get_fact_service(db)
    try:
        result = service.extract_facts_with_runtime(case_id)
    except ValueError as error:
        if str(error) == "case not found":
            raise HTTPException(status_code=404, detail=str(error)) from error
        if is_runtime_error(error):
            raise HTTPException(status_code=400, detail=str(error)) from error
        raise HTTPException(status_code=500, detail="fact extraction failed") from error
    response = {
        "case_id": case_id,
        "facts": [serialize_fact(fact) for fact in result.facts]
    }
    if result.skill_used is not None:
        response["skill_used"] = result.skill_used
    if result.package_used is not None:
        response["package_used"] = result.package_used
    return response


@router.get("")
def list_facts(
    case_id: str,
    db: Session = Depends(get_db)
) -> dict[str, Any]:
    service = get_fact_service(db)
    try:
        facts = service.list_facts(case_id)
    except ValueError as error:
        raise HTTPException(status_code=404, detail=str(error)) from error
    return {
        "case_id": case_id,
        "facts": [serialize_fact(fact) for fact in facts]
    }
