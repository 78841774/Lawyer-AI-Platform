from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.report import Report


class ReportRepository:
    def __init__(self, db: Session) -> None:
        self.db = db

    def next_report_id(self) -> str:
        index = self.db.query(Report).count() + 1
        while self.get_by_report_id(f"report_{index:03d}") is not None:
            index += 1
        return f"report_{index:03d}"

    def next_version(self, case_id: str) -> int:
        return len(self.list_by_case_id(case_id)) + 1

    def create(
        self,
        *,
        report_id: str,
        case_id: str,
        report_type: str,
        title: str,
        content: str,
        status: str,
        version: int,
        storage_path: str,
        source_refs: str
    ) -> Report:
        report = Report(
            report_id=report_id,
            case_id=case_id,
            report_type=report_type,
            title=title,
            content=content,
            status=status,
            version=version,
            storage_path=storage_path,
            source_refs=source_refs
        )
        self.db.add(report)
        self.db.commit()
        self.db.refresh(report)
        return report

    def get_by_report_id(self, report_id: str) -> Report | None:
        return self.db.execute(
            select(Report).where(Report.report_id == report_id)
        ).scalar_one_or_none()

    def list_by_case_id(self, case_id: str) -> list[Report]:
        return list(
            self.db.execute(
                select(Report)
                .where(Report.case_id == case_id)
                .order_by(Report.created_at.asc(), Report.id.asc())
            ).scalars()
        )
