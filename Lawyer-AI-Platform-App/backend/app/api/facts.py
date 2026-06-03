from typing import Any

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.models.fact import Fact
from app.repositories.case_repository import CaseRepository
from app.repositories.fact_repository import FactRepository
from app.repositories.material_repository import MaterialRepository
from app.services.fact_service import FactService

router = APIRouter(prefix="/cases/{case_id}/facts", tags=["facts"])


def get_fact_service(db: Session) -> FactService:
    return FactService(
        fact_repository=FactRepository(db),
        material_repository=MaterialRepository(db),
        case_repository=CaseRepository(db)
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


@router.post("/extract")
def extract_facts(
    case_id: str,
    db: Session = Depends(get_db)
) -> dict[str, Any]:
    service = get_fact_service(db)
    try:
        facts = service.extract_facts(case_id)
    except ValueError as error:
        raise HTTPException(status_code=404, detail=str(error)) from error
    return {
        "case_id": case_id,
        "facts": [serialize_fact(fact) for fact in facts]
    }


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
