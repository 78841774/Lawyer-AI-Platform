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
        objective: str | None
    ) -> Case:
        resolved_case_id = case_id or self.repository.next_case_id()
        if self.repository.get_by_case_id(resolved_case_id) is not None:
            raise ValueError("case_id already exists")

        return self.repository.create(
            case_id=resolved_case_id,
            title=title,
            case_type=case_type,
            status=status,
            objective=objective
        )

    def get_case(self, case_id: str) -> Case | None:
        return self.repository.get_by_case_id(case_id)
