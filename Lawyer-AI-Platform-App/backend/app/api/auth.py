from typing import Any

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.core.auth import AuthContext, get_auth_context, hash_token
from app.core.config import settings
from app.core.database import get_db
from app.core.jwt_auth import create_access_token
from app.repositories.identity_repository import IdentityRepository

router = APIRouter(prefix="/auth", tags=["auth"])


class LoginRequest(BaseModel):
    user_id: str
    dev_token: str


@router.get("/status")
def auth_status(context: AuthContext = Depends(get_auth_context)) -> dict[str, Any]:
    return {
        "authenticated": True,
        "user_id": context.user.user_id,
        "auth_mode": context.auth_mode,
        "expires_at": context.expires_at.isoformat() if context.expires_at else None
    }


@router.post("/login")
def login(
    payload: LoginRequest,
    db: Session = Depends(get_db)
) -> dict[str, Any]:
    repository = IdentityRepository(db)
    user = repository.get_user(payload.user_id)
    if user is None or user.status != "active":
        raise HTTPException(status_code=401, detail="user is not active")

    auth_token = repository.get_auth_token_by_hash(hash_token(payload.dev_token))
    if (
        auth_token is None
        or auth_token.status != "active"
        or auth_token.user_id != user.user_id
    ):
        raise HTTPException(status_code=401, detail="invalid dev token")

    access_token, expires_at = create_access_token(user.user_id)
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "expires_in": settings.jwt_expiration_minutes * 60,
        "user_id": user.user_id,
        "expires_at": expires_at.isoformat()
    }


@router.get("/dev-token")
def dev_token() -> dict[str, Any]:
    if settings.app_env.lower().strip() != "local":
        raise HTTPException(status_code=403, detail="dev token endpoint is local only")

    token = settings.local_dev_token
    return {
        "token_name": "Local Dev Token",
        "example_headers": {
            "Authorization": f"Bearer {token}",
            "X-Dev-Token": token
        }
    }
