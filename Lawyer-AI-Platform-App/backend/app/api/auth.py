from typing import Any

from fastapi import APIRouter, Depends, HTTPException

from app.core.auth import AuthContext, get_auth_context
from app.core.config import settings

router = APIRouter(prefix="/auth", tags=["auth"])


@router.get("/status")
def auth_status(context: AuthContext = Depends(get_auth_context)) -> dict[str, Any]:
    return {
        "authenticated": True,
        "user_id": context.user.user_id,
        "auth_mode": context.auth_mode
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
