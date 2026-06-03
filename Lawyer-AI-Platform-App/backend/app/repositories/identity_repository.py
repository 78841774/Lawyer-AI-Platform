from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.user import User
from app.models.workspace import Workspace, WorkspaceMember


class IdentityRepository:
    def __init__(self, db: Session) -> None:
        self.db = db

    def get_user(self, user_id: str) -> User | None:
        return self.db.execute(
            select(User).where(User.user_id == user_id)
        ).scalar_one_or_none()

    def create_user(
        self,
        *,
        user_id: str,
        email: str,
        display_name: str,
        role: str,
        status: str
    ) -> User:
        user = User(
            user_id=user_id,
            email=email,
            display_name=display_name,
            role=role,
            status=status
        )
        self.db.add(user)
        self.db.flush()
        return user

    def get_workspace(self, workspace_id: str) -> Workspace | None:
        return self.db.execute(
            select(Workspace).where(Workspace.workspace_id == workspace_id)
        ).scalar_one_or_none()

    def create_workspace(
        self,
        *,
        workspace_id: str,
        name: str,
        owner_user_id: str,
        status: str
    ) -> Workspace:
        workspace = Workspace(
            workspace_id=workspace_id,
            name=name,
            owner_user_id=owner_user_id,
            status=status
        )
        self.db.add(workspace)
        self.db.flush()
        return workspace

    def get_member(self, workspace_id: str, user_id: str) -> WorkspaceMember | None:
        return self.db.execute(
            select(WorkspaceMember).where(
                WorkspaceMember.workspace_id == workspace_id,
                WorkspaceMember.user_id == user_id
            )
        ).scalar_one_or_none()

    def create_member(
        self,
        *,
        workspace_id: str,
        user_id: str,
        role: str,
        status: str
    ) -> WorkspaceMember:
        member = WorkspaceMember(
            workspace_id=workspace_id,
            user_id=user_id,
            role=role,
            status=status
        )
        self.db.add(member)
        self.db.flush()
        return member

    def list_active_workspaces_for_user(self, user_id: str) -> list[Workspace]:
        return list(
            self.db.execute(
                select(Workspace)
                .join(
                    WorkspaceMember,
                    WorkspaceMember.workspace_id == Workspace.workspace_id
                )
                .where(
                    WorkspaceMember.user_id == user_id,
                    WorkspaceMember.status == "active",
                    Workspace.status == "active"
                )
                .order_by(Workspace.created_at.asc(), Workspace.id.asc())
            ).scalars()
        )
