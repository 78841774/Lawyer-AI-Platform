from app.models.case import Case
from app.repositories.case_repository import CaseRepository


class CaseService:
    def __init__(self, repository: CaseRepository) -> None:
        self.repository = repository

    def create_case(
        self,
        *,
        case_id: str | None,
        title: str,
        case_type: str,
        status: str,
        objective: str | None,
        workspace_id: str,
        owner_user_id: str
    ) -> Case:
        resolved_case_id = case_id or self.repository.next_case_id()
        if self.repository.get_by_case_id(resolved_case_id) is not None:
            raise ValueError("case_id already exists")

        return self.repository.create(
            case_id=resolved_case_id,
            title=title,
            case_type=case_type,
            status=status,
            objective=objective,
            workspace_id=workspace_id,
            owner_user_id=owner_user_id
        )

    def get_case(self, case_id: str) -> Case | None:
        return self.repository.get_by_case_id(case_id)

    def list_cases(self) -> list[Case]:
        return self.repository.list_all()

    def list_cases_for_workspace(self, workspace_id: str) -> list[Case]:
        return self.repository.list_by_workspace_id(workspace_id)

    def list_cases_for_workspaces(self, workspace_ids: list[str]) -> list[Case]:
        return self.repository.list_by_workspace_ids(workspace_ids)
