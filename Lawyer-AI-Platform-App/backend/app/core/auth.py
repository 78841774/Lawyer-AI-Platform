from dataclasses import dataclass
from datetime import datetime
from hashlib import sha256

from fastapi import Depends, HTTPException, Request
from sqlalchemy.orm import Session

from app.core.config import settings
from app.core.database import get_db
from app.models.user import User
from app.repositories.identity_repository import IdentityRepository
from app.services.identity_service import LOCAL_USER_ID


@dataclass(frozen=True)
class AuthContext:
    user: User
    auth_mode: str
    token_id: str | None = None


def hash_token(token: str) -> str:
    return sha256(token.encode("utf-8")).hexdigest()


def get_auth_context(
    request: Request,
    db: Session = Depends(get_db)
) -> AuthContext:
    repository = IdentityRepository(db)
    token = _extract_token(request)

    if token:
        token_hash = hash_token(token)
        auth_token = repository.get_auth_token_by_hash(token_hash)
        if auth_token is None or auth_token.status != "active":
            raise HTTPException(status_code=401, detail="invalid auth token")

        user = repository.get_user(auth_token.user_id)
        if user is None or user.status != "active":
            raise HTTPException(status_code=401, detail="token user is not active")

        auth_token.last_used_at = datetime.utcnow()
        db.commit()
        return AuthContext(
            user=user,
            auth_mode="dev_token",
            token_id=auth_token.token_id
        )

    if settings.app_env.lower().strip() == "local":
        user = repository.get_user(LOCAL_USER_ID)
        if user is None or user.status != "active":
            raise HTTPException(status_code=401, detail="local fallback user is not active")
        return AuthContext(user=user, auth_mode="local_fallback")

    raise HTTPException(status_code=401, detail="auth token required")


def get_current_user(context: AuthContext = Depends(get_auth_context)) -> User:
    return context.user


def _extract_token(request: Request) -> str | None:
    authorization = request.headers.get("Authorization", "").strip()
    if authorization.lower().startswith("bearer "):
        token = authorization[7:].strip()
        if token:
            return token

    dev_token = request.headers.get("X-Dev-Token", "").strip()
    if dev_token:
        return dev_token

    return None
