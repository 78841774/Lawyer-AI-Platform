from hashlib import sha256

from app.core.config import settings
from app.models.user import User
from app.models.workspace import Workspace
from app.repositories.identity_repository import IdentityRepository

LOCAL_USER_ID = "user_local_001"
LOCAL_USER_EMAIL = "local@example.com"
LOCAL_USER_DISPLAY_NAME = "Local Demo User"
LOCAL_WORKSPACE_ID = "workspace_local_001"
LOCAL_WORKSPACE_NAME = "Local Demo Workspace"
LOCAL_TOKEN_ID = "token_local_001"
LOCAL_TOKEN_NAME = "Local Dev Token"


def hash_local_token(token: str) -> str:
    return sha256(token.encode("utf-8")).hexdigest()


class IdentityService:
    def __init__(self, repository: IdentityRepository) -> None:
        self.repository = repository

    def get_current_user(self) -> User:
        user = self.repository.get_user(LOCAL_USER_ID)
        if user is None:
            raise ValueError("local demo user not found")
        if user.status != "active":
            raise PermissionError("local demo user is not active")
        return user

    def list_current_user_workspaces(self) -> list[Workspace]:
        user = self.get_current_user()
        return self.list_user_workspaces(user)

    def get_current_user_workspace(self, workspace_id: str) -> Workspace:
        user = self.get_current_user()
        return self.get_user_workspace(user, workspace_id)

    def list_user_workspaces(self, user: User) -> list[Workspace]:
        if user.status != "active":
            raise PermissionError("user is not active")
        return self.repository.list_active_workspaces_for_user(user.user_id)

    def get_first_active_workspace(self, user: User) -> Workspace | None:
        workspaces = self.list_user_workspaces(user)
        return workspaces[0] if workspaces else None

    def get_user_workspace(self, user: User, workspace_id: str) -> Workspace:
        if user.status != "active":
            raise PermissionError("user is not active")
        workspace = self.repository.get_workspace(workspace_id)
        if workspace is None:
            raise LookupError("workspace not found")
        if workspace.status != "active":
            raise PermissionError("workspace is not active")
        member = self.repository.get_member(workspace.workspace_id, user.user_id)
        if member is None or member.status != "active":
            raise PermissionError("workspace is not available to current user")
        return workspace


def ensure_local_demo_identity(repository: IdentityRepository) -> None:
    user = repository.get_user(LOCAL_USER_ID)
    if user is None:
        user = repository.create_user(
            user_id=LOCAL_USER_ID,
            email=LOCAL_USER_EMAIL,
            display_name=LOCAL_USER_DISPLAY_NAME,
            role="admin",
            status="active"
        )
    user.email = LOCAL_USER_EMAIL
    user.display_name = LOCAL_USER_DISPLAY_NAME
    user.role = "admin"
    user.status = "active"

    workspace = repository.get_workspace(LOCAL_WORKSPACE_ID)
    if workspace is None:
        workspace = repository.create_workspace(
            workspace_id=LOCAL_WORKSPACE_ID,
            name=LOCAL_WORKSPACE_NAME,
            owner_user_id=LOCAL_USER_ID,
            status="active"
        )
    workspace.name = LOCAL_WORKSPACE_NAME
    workspace.owner_user_id = LOCAL_USER_ID
    workspace.status = "active"

    member = repository.get_member(LOCAL_WORKSPACE_ID, LOCAL_USER_ID)
    if member is None:
        member = repository.create_member(
            workspace_id=LOCAL_WORKSPACE_ID,
            user_id=LOCAL_USER_ID,
            role="admin",
            status="active"
        )
    member.role = "admin"
    member.status = "active"

    token = repository.get_auth_token_by_id(LOCAL_TOKEN_ID)
    if token is None:
        token = repository.create_auth_token(
            token_id=LOCAL_TOKEN_ID,
            user_id=LOCAL_USER_ID,
            token_hash=hash_local_token(settings.local_dev_token),
            token_name=LOCAL_TOKEN_NAME,
            status="active"
        )
    token.user_id = LOCAL_USER_ID
    token.token_hash = hash_local_token(settings.local_dev_token)
    token.token_name = LOCAL_TOKEN_NAME
    token.status = "active"
