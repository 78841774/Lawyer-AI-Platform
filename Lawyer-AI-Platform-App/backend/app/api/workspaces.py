from typing import Any

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.api.cases import CaseCreate, serialize_case
from app.core.auth import AuthContext, get_auth_context
from app.core.database import get_db
from app.models.workspace import Workspace
from app.repositories.case_repository import CaseRepository
from app.repositories.identity_repository import IdentityRepository
from app.services.case_service import CaseService
from app.services.identity_service import IdentityService

router = APIRouter(prefix="/workspaces", tags=["workspaces"])


def serialize_workspace(workspace: Workspace) -> dict[str, Any]:
    return {
        "workspace_id": workspace.workspace_id,
        "name": workspace.name,
        "owner_user_id": workspace.owner_user_id,
        "status": workspace.status,
        "created_at": workspace.created_at,
        "updated_at": workspace.updated_at
    }


def get_identity_service(db: Session) -> IdentityService:
    return IdentityService(IdentityRepository(db))


def raise_identity_error(error: Exception) -> None:
    if isinstance(error, LookupError):
        raise HTTPException(status_code=404, detail=str(error)) from error
    if isinstance(error, ValueError):
        raise HTTPException(status_code=404, detail=str(error)) from error
    if isinstance(error, PermissionError):
        raise HTTPException(status_code=403, detail=str(error)) from error
    raise HTTPException(status_code=500, detail=str(error)) from error


@router.get("")
def list_workspaces(
    context: AuthContext = Depends(get_auth_context),
    db: Session = Depends(get_db)
) -> list[dict[str, Any]]:
    service = get_identity_service(db)
    try:
        return [
            serialize_workspace(workspace)
            for workspace in service.list_user_workspaces(context.user)
        ]
    except (ValueError, PermissionError) as error:
        raise_identity_error(error)


@router.get("/{workspace_id}")
def get_workspace(
    workspace_id: str,
    context: AuthContext = Depends(get_auth_context),
    db: Session = Depends(get_db)
) -> dict[str, Any]:
    service = get_identity_service(db)
    try:
        return serialize_workspace(service.get_user_workspace(context.user, workspace_id))
    except (LookupError, PermissionError, ValueError) as error:
        raise_identity_error(error)


@router.get("/{workspace_id}/cases")
def list_workspace_cases(
    workspace_id: str,
    context: AuthContext = Depends(get_auth_context),
    db: Session = Depends(get_db)
) -> list[dict[str, Any]]:
    identity_service = get_identity_service(db)
    try:
        identity_service.get_user_workspace(context.user, workspace_id)
    except (LookupError, PermissionError, ValueError) as error:
        raise_identity_error(error)

    case_service = CaseService(CaseRepository(db))
    return [
        serialize_case(case)
        for case in case_service.list_cases_for_workspace(workspace_id)
    ]


@router.post("/{workspace_id}/cases")
def create_workspace_case(
    workspace_id: str,
    payload: CaseCreate | None = None,
    context: AuthContext = Depends(get_auth_context),
    db: Session = Depends(get_db)
) -> dict[str, Any]:
    identity_service = get_identity_service(db)
    try:
        workspace = identity_service.get_user_workspace(context.user, workspace_id)
    except (LookupError, PermissionError, ValueError) as error:
        raise_identity_error(error)

    case_payload = payload or CaseCreate()
    case_service = CaseService(CaseRepository(db))
    try:
        case = case_service.create_case(
            case_id=case_payload.case_id,
            title=case_payload.title,
            case_type=case_payload.case_type,
            status=case_payload.status,
            objective=case_payload.objective,
            workspace_id=workspace.workspace_id,
            owner_user_id=context.user.user_id
        )
    except ValueError as error:
        raise HTTPException(status_code=409, detail=str(error)) from error
    return serialize_case(case)
