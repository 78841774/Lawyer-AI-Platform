from typing import Any

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.models.case import Case
from app.repositories.case_repository import CaseRepository
from app.repositories.identity_repository import IdentityRepository
from app.services.case_service import CaseService
from app.services.identity_service import (
    IdentityService,
    LOCAL_WORKSPACE_ID
)

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
        "workspace_id": case.workspace_id,
        "owner_user_id": case.owner_user_id,
        "created_at": case.created_at,
        "updated_at": case.updated_at
    }


@router.get("")
def list_cases(db: Session = Depends(get_db)) -> list[dict[str, Any]]:
    service = CaseService(CaseRepository(db))
    return [serialize_case(case) for case in service.list_cases()]


@router.post("")
def create_case(
    payload: CaseCreate | None = None,
    db: Session = Depends(get_db)
) -> dict[str, Any]:
    case_payload = payload or CaseCreate()
    identity_service = IdentityService(IdentityRepository(db))
    service = CaseService(CaseRepository(db))

    try:
        user = identity_service.get_current_user()
        workspace = identity_service.get_current_user_workspace(LOCAL_WORKSPACE_ID)
        case = service.create_case(
            case_id=case_payload.case_id,
            title=case_payload.title,
            case_type=case_payload.case_type,
            status=case_payload.status,
            objective=case_payload.objective,
            workspace_id=workspace.workspace_id,
            owner_user_id=user.user_id
        )
    except ValueError as error:
        detail = str(error)
        status_code = 409 if "case_id already exists" in detail else 404
        raise HTTPException(status_code=status_code, detail=detail) from error
    except PermissionError as error:
        raise HTTPException(status_code=403, detail=str(error)) from error
    except LookupError as error:
        raise HTTPException(status_code=404, detail=str(error)) from error
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
