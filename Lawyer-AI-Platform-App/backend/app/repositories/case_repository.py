from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.case import Case


class CaseRepository:
    def __init__(self, db: Session) -> None:
        self.db = db

    def next_case_id(self) -> str:
        index = self.db.query(Case).count() + 1
        while self.get_by_case_id(f"case_{index:03d}") is not None:
            index += 1
        return f"case_{index:03d}"

    def create(
        self,
        *,
        case_id: str,
        title: str,
        case_type: str,
        status: str,
        objective: str | None,
        workspace_id: str,
        owner_user_id: str
    ) -> Case:
        case = Case(
            case_id=case_id,
            title=title,
            case_type=case_type,
            status=status,
            objective=objective,
            workspace_id=workspace_id,
            owner_user_id=owner_user_id
        )
        self.db.add(case)
        self.db.commit()
        self.db.refresh(case)
        return case

    def get_by_case_id(self, case_id: str) -> Case | None:
        return self.db.execute(
            select(Case).where(Case.case_id == case_id)
        ).scalar_one_or_none()

    def list_all(self) -> list[Case]:
        return list(
            self.db.execute(
                select(Case).order_by(Case.created_at.asc(), Case.id.asc())
            ).scalars()
        )

    def list_by_workspace_id(self, workspace_id: str) -> list[Case]:
        return list(
            self.db.execute(
                select(Case)
                .where(Case.workspace_id == workspace_id)
                .order_by(Case.created_at.asc(), Case.id.asc())
            ).scalars()
        )

    def list_by_workspace_ids(self, workspace_ids: list[str]) -> list[Case]:
        if not workspace_ids:
            return []
        return list(
            self.db.execute(
                select(Case)
                .where(Case.workspace_id.in_(workspace_ids))
                .order_by(Case.created_at.asc(), Case.id.asc())
            ).scalars()
        )

    def count_all(self) -> int:
        return self.db.query(Case).count()
