from app.models.case import Case
from app.models.report import Report
from app.repositories.case_repository import CaseRepository
from app.repositories.fact_repository import FactRepository
from app.repositories.legal_analysis_repository import LegalAnalysisRepository
from app.repositories.material_repository import MaterialRepository
from app.repositories.report_repository import ReportRepository


class WorkspaceService:
    def __init__(
        self,
        *,
        case_repository: CaseRepository,
        material_repository: MaterialRepository,
        fact_repository: FactRepository,
        legal_analysis_repository: LegalAnalysisRepository,
        report_repository: ReportRepository
    ) -> None:
        self.case_repository = case_repository
        self.material_repository = material_repository
        self.fact_repository = fact_repository
        self.legal_analysis_repository = legal_analysis_repository
        self.report_repository = report_repository

    def list_cases(self) -> list[Case]:
        return self.case_repository.list_all()

    def list_reports(self) -> list[Report]:
        return self.report_repository.list_all()

    def get_report(self, report_id: str) -> Report | None:
        return self.report_repository.get_by_report_id(report_id)

    def dashboard_stats(self) -> dict[str, int]:
        return {
            "cases": self.case_repository.count_all(),
            "materials": self.material_repository.count_all(),
            "facts": self.fact_repository.count_all(),
            "analyses": self.legal_analysis_repository.count_all(),
            "reports": self.report_repository.count_all()
        }
