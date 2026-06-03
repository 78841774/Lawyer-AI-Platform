import json
from typing import Any

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.models.case import Case
from app.models.report import Report
from app.repositories.case_repository import CaseRepository
from app.repositories.fact_repository import FactRepository
from app.repositories.legal_analysis_repository import LegalAnalysisRepository
from app.repositories.material_repository import MaterialRepository
from app.repositories.report_repository import ReportRepository
from app.services.workspace_service import WorkspaceService

router = APIRouter(tags=["workspace"])


def get_workspace_service(db: Session) -> WorkspaceService:
    return WorkspaceService(
        case_repository=CaseRepository(db),
        material_repository=MaterialRepository(db),
        fact_repository=FactRepository(db),
        legal_analysis_repository=LegalAnalysisRepository(db),
        report_repository=ReportRepository(db)
    )


def serialize_case(case: Case) -> dict[str, Any]:
    return {
        "case_id": case.case_id,
        "title": case.title,
        "case_type": case.case_type,
        "status": case.status,
        "objective": case.objective,
        "created_at": case.created_at,
        "updated_at": case.updated_at
    }


def serialize_report(report: Report) -> dict[str, Any]:
    return {
        "report_id": report.report_id,
        "case_id": report.case_id,
        "report_type": report.report_type,
        "title": report.title,
        "content": report.content,
        "status": report.status,
        "version": report.version,
        "storage_path": report.storage_path,
        "source_refs": json.loads(report.source_refs),
        "created_at": report.created_at
    }


@router.get("/cases")
def list_cases(db: Session = Depends(get_db)) -> list[dict[str, Any]]:
    service = get_workspace_service(db)
    return [serialize_case(case) for case in service.list_cases()]


@router.get("/reports")
def list_reports(db: Session = Depends(get_db)) -> list[dict[str, Any]]:
    service = get_workspace_service(db)
    return [serialize_report(report) for report in service.list_reports()]


@router.get("/reports/{report_id}")
def get_report(
    report_id: str,
    db: Session = Depends(get_db)
) -> dict[str, Any]:
    service = get_workspace_service(db)
    report = service.get_report(report_id)
    if report is None:
        raise HTTPException(status_code=404, detail="report not found")
    return serialize_report(report)


@router.get("/dashboard/stats")
def dashboard_stats(db: Session = Depends(get_db)) -> dict[str, int]:
    service = get_workspace_service(db)
    return service.dashboard_stats()
