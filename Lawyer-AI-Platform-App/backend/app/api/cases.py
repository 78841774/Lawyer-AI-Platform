from typing import Any

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.models.case import Case
from app.repositories.case_repository import CaseRepository
from app.services.case_service import CaseService

router = APIRouter(prefix="/cases", tags=["cases"])


class CaseCreate(BaseModel):
    case_id: str | None = None
    title: str = "MVP Demo Case"
    case_type: str = "contract_dispute"
    status: str = "draft"
    parties: list[dict[str, Any]] = Field(default_factory=list)
    objective: str | None = None


def serialize_case(case: Case) -> dict[str, Any]:
    return {
        "case_id": case.case_id,
        "title": case.title,
        "case_type": case.case_type,
        "status": case.status,
        "objective": case.objective,
        "created_at": case.created_at,
        "updated_at": case.updated_at
    }


@router.post("")
def create_case(
    payload: CaseCreate | None = None,
    db: Session = Depends(get_db)
) -> dict[str, Any]:
    case_payload = payload or CaseCreate()
    service = CaseService(CaseRepository(db))

    try:
        case = service.create_case(
            case_id=case_payload.case_id,
            title=case_payload.title,
            case_type=case_payload.case_type,
            status=case_payload.status,
            objective=case_payload.objective
        )
    except ValueError as error:
        raise HTTPException(status_code=409, detail=str(error)) from error
    return serialize_case(case)


@router.get("/{case_id}")
def get_case(
    case_id: str,
    db: Session = Depends(get_db)
) -> dict[str, Any]:
    service = CaseService(CaseRepository(db))
    case = service.get_case(case_id)
    if case is None:
        raise HTTPException(status_code=404, detail="case not found")
    return serialize_case(case)
