from datetime import datetime, timedelta, timezone
from uuid import uuid4

from fastapi import HTTPException
from jose import ExpiredSignatureError, JWTError, jwt

from app.core.config import settings
from app.models.user import User
from app.repositories.identity_repository import IdentityRepository


def create_access_token(
    user_id: str,
    expires_delta: timedelta | None = None
) -> tuple[str, datetime]:
    expires_at = datetime.now(timezone.utc) + (
        expires_delta or timedelta(minutes=settings.jwt_expiration_minutes)
    )
    payload = {
        "sub": user_id,
        "exp": expires_at,
        "jti": str(uuid4())
    }
    token = jwt.encode(
        payload,
        settings.jwt_secret_key,
        algorithm=settings.jwt_algorithm
    )
    return token, expires_at


def decode_access_token(token: str) -> dict[str, object]:
    try:
        return jwt.decode(
            token,
            settings.jwt_secret_key,
            algorithms=[settings.jwt_algorithm]
        )
    except ExpiredSignatureError as error:
        raise HTTPException(status_code=401, detail="jwt token expired") from error
    except JWTError as error:
        raise HTTPException(status_code=401, detail="invalid jwt token") from error


def get_current_user_from_jwt(
    token: str,
    repository: IdentityRepository
) -> tuple[User, dict[str, object], datetime | None]:
    payload = decode_access_token(token)
    user_id = payload.get("sub")
    if not isinstance(user_id, str) or not user_id:
        raise HTTPException(status_code=401, detail="jwt subject missing")

    user = repository.get_user(user_id)
    if user is None or user.status != "active":
        raise HTTPException(status_code=401, detail="jwt user is not active")

    expires_at = _payload_exp_to_datetime(payload.get("exp"))
    return user, payload, expires_at


def _payload_exp_to_datetime(exp: object) -> datetime | None:
    if isinstance(exp, int | float):
        return datetime.fromtimestamp(exp, timezone.utc)
    return None
