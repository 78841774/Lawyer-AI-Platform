from typing import Any

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.models.user import User
from app.repositories.identity_repository import IdentityRepository
from app.services.identity_service import IdentityService

router = APIRouter(prefix="/users", tags=["users"])


def serialize_user(user: User) -> dict[str, Any]:
    return {
        "user_id": user.user_id,
        "email": user.email,
        "display_name": user.display_name,
        "role": user.role,
        "status": user.status,
        "created_at": user.created_at,
        "updated_at": user.updated_at
    }


@router.get("/me")
def get_me(db: Session = Depends(get_db)) -> dict[str, Any]:
    service = IdentityService(IdentityRepository(db))
    try:
        return serialize_user(service.get_current_user())
    except ValueError as error:
        raise HTTPException(status_code=404, detail=str(error)) from error
    except PermissionError as error:
        raise HTTPException(status_code=403, detail=str(error)) from error
