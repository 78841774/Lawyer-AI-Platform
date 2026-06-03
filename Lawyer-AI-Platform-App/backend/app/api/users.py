from typing import Any

from fastapi import APIRouter, Depends

from app.core.auth import AuthContext, get_auth_context
from app.models.user import User

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
def get_me(context: AuthContext = Depends(get_auth_context)) -> dict[str, Any]:
    return serialize_user(context.user)
