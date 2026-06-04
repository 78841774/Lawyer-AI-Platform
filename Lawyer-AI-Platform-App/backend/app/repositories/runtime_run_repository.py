from datetime import datetime
from uuid import uuid4

from sqlalchemy import select, update
from sqlalchemy.orm import Session

from app.models.runtime_run import AnalysisRun, ExtractionRun, ReportRun


class RuntimeRunRepository:
    def __init__(self, db: Session) -> None:
        self.db = db

    def next_run_id(self, prefix: str) -> str:
        return f"{prefix}_{datetime.utcnow().strftime('%Y%m%d%H%M%S')}_{uuid4().hex[:8]}"

    def create_extraction_run(
        self,
        *,
        case_id: str,
        workspace_id: str | None,
        triggered_by_user_id: str | None
    ) -> ExtractionRun:
        self._mark_not_latest(ExtractionRun, case_id)
        run = ExtractionRun(
            run_id=self.next_run_id("extract"),
            case_id=case_id,
            workspace_id=workspace_id,
            triggered_by_user_id=triggered_by_user_id,
            status="running",
            is_latest=True
        )
        self.db.add(run)
        self.db.commit()
        self.db.refresh(run)
        return run

    def complete_extraction_run(
        self,
        run: ExtractionRun,
        *,
        llm_provider: str | None,
        llm_status: str | None,
        skill_id: str | None,
        package_id: str | None,
        materials_count: int,
        facts_created_count: int,
        facts_reused_count: int,
        facts_skipped_count: int,
        source_material_ids: str,
        source_refs: str
    ) -> ExtractionRun:
        run.status = "completed"
        run.llm_provider = llm_provider
        run.llm_status = llm_status
        run.skill_id = skill_id
        run.package_id = package_id
        run.materials_count = materials_count
        run.facts_created_count = facts_created_count
        run.facts_reused_count = facts_reused_count
        run.facts_skipped_count = facts_skipped_count
        run.source_material_ids = source_material_ids
        run.source_refs = source_refs
        run.completed_at = datetime.utcnow()
        self.db.commit()
        self.db.refresh(run)
        return run

    def create_analysis_run(
        self,
        *,
        case_id: str,
        workspace_id: str | None,
        triggered_by_user_id: str | None
    ) -> AnalysisRun:
        self._mark_not_latest(AnalysisRun, case_id)
        run = AnalysisRun(
            run_id=self.next_run_id("analysis"),
            case_id=case_id,
            workspace_id=workspace_id,
            triggered_by_user_id=triggered_by_user_id,
            status="running",
            is_latest=True
        )
        self.db.add(run)
        self.db.commit()
        self.db.refresh(run)
        return run

    def complete_analysis_run(
        self,
        run: AnalysisRun,
        *,
        llm_provider: str | None,
        llm_status: str | None,
        skill_id: str | None,
        package_id: str | None,
        facts_count: int,
        analysis_id: str | None,
        source_fact_ids: str,
        source_refs: str
    ) -> AnalysisRun:
        run.status = "completed"
        run.llm_provider = llm_provider
        run.llm_status = llm_status
        run.skill_id = skill_id
        run.package_id = package_id
        run.facts_count = facts_count
        run.analysis_id = analysis_id
        run.source_fact_ids = source_fact_ids
        run.source_refs = source_refs
        run.completed_at = datetime.utcnow()
        self.db.commit()
        self.db.refresh(run)
        return run

    def create_report_run(
        self,
        *,
        case_id: str,
        workspace_id: str | None,
        triggered_by_user_id: str | None
    ) -> ReportRun:
        self._mark_not_latest(ReportRun, case_id)
        run = ReportRun(
            run_id=self.next_run_id("report"),
            case_id=case_id,
            workspace_id=workspace_id,
            triggered_by_user_id=triggered_by_user_id,
            status="running",
            is_latest=True
        )
        self.db.add(run)
        self.db.commit()
        self.db.refresh(run)
        return run

    def complete_report_run(
        self,
        run: ReportRun,
        *,
        llm_provider: str | None,
        llm_status: str | None,
        skill_id: str | None,
        package_id: str | None,
        analysis_id: str | None,
        report_id: str | None,
        source_refs: str
    ) -> ReportRun:
        run.status = "completed"
        run.llm_provider = llm_provider
        run.llm_status = llm_status
        run.skill_id = skill_id
        run.package_id = package_id
        run.analysis_id = analysis_id
        run.report_id = report_id
        run.source_refs = source_refs
        run.completed_at = datetime.utcnow()
        self.db.commit()
        self.db.refresh(run)
        return run

    def fail_run(self, run: ExtractionRun | AnalysisRun | ReportRun, error_message: str) -> None:
        run.status = "failed"
        run.error_message = error_message[:1000]
        run.completed_at = datetime.utcnow()
        self.db.commit()

    def list_extraction_runs(self, case_id: str) -> list[ExtractionRun]:
        return self._list_runs(ExtractionRun, case_id)

    def list_analysis_runs(self, case_id: str) -> list[AnalysisRun]:
        return self._list_runs(AnalysisRun, case_id)

    def list_report_runs(self, case_id: str) -> list[ReportRun]:
        return self._list_runs(ReportRun, case_id)

    def latest_extraction_run(self, case_id: str) -> ExtractionRun | None:
        return self._latest_run(ExtractionRun, case_id)

    def latest_analysis_run(self, case_id: str) -> AnalysisRun | None:
        return self._latest_run(AnalysisRun, case_id)

    def latest_report_run(self, case_id: str) -> ReportRun | None:
        return self._latest_run(ReportRun, case_id)

    def _mark_not_latest(self, model: type[ExtractionRun] | type[AnalysisRun] | type[ReportRun], case_id: str) -> None:
        self.db.execute(
            update(model)
            .where(model.case_id == case_id)
            .where(model.is_latest.is_(True))
            .values(is_latest=False)
        )
        self.db.commit()

    def _list_runs(
        self,
        model: type[ExtractionRun] | type[AnalysisRun] | type[ReportRun],
        case_id: str
    ):
        return list(
            self.db.execute(
                select(model)
                .where(model.case_id == case_id)
                .order_by(model.created_at.desc(), model.id.desc())
            ).scalars()
        )

    def _latest_run(
        self,
        model: type[ExtractionRun] | type[AnalysisRun] | type[ReportRun],
        case_id: str
    ):
        return self.db.execute(
            select(model)
            .where(model.case_id == case_id)
            .where(model.is_latest.is_(True))
            .order_by(model.created_at.desc(), model.id.desc())
        ).scalar_one_or_none()
