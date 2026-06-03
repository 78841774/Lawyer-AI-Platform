import json
from typing import Any

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.config import settings
from app.core.database import get_db
from app.models.report import Report
from app.repositories.case_repository import CaseRepository
from app.repositories.fact_repository import FactRepository
from app.repositories.legal_analysis_repository import LegalAnalysisRepository
from app.repositories.report_repository import ReportRepository
from app.repositories.skill_repository import SkillRepository
from app.repositories.workspace_skill_repository import WorkspaceSkillRepository
from app.services.report_service import ReportService
from app.services.skill_runtime_service import SkillRuntimeService

router = APIRouter(prefix="/cases/{case_id}/reports", tags=["reports"])


def get_report_service(db: Session) -> ReportService:
    return ReportService(
        report_repository=ReportRepository(db),
        fact_repository=FactRepository(db),
        legal_analysis_repository=LegalAnalysisRepository(db),
        case_repository=CaseRepository(db),
        storage_root=settings.storage_root,
        skill_runtime_service=SkillRuntimeService(
            skill_repository=SkillRepository(db),
            workspace_skill_repository=WorkspaceSkillRepository(db)
        )
    )


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


@router.post("/generate")
def generate_report(
    case_id: str,
    db: Session = Depends(get_db)
) -> dict[str, Any]:
    service = get_report_service(db)
    try:
        report = service.generate_report(case_id)
    except ValueError as error:
        if str(error) == "case not found":
            raise HTTPException(status_code=404, detail=str(error)) from error
        if str(error) == "facts required":
            raise HTTPException(
                status_code=400,
                detail="facts required: run Fact Runtime before Report Runtime"
            ) from error
        if str(error) == "analysis required":
            raise HTTPException(
                status_code=400,
                detail="legal analysis required: run Legal Analysis Runtime before Report Runtime"
            ) from error
        raise HTTPException(status_code=500, detail="report generation failed") from error
    except Exception as error:
        raise HTTPException(status_code=500, detail="report generation failed") from error
    return serialize_report(report)


@router.get("")
def list_case_reports(
    case_id: str,
    db: Session = Depends(get_db)
) -> dict[str, Any]:
    service = get_report_service(db)
    try:
        reports = service.list_reports(case_id)
    except ValueError as error:
        raise HTTPException(status_code=404, detail=str(error)) from error
    except Exception as error:
        raise HTTPException(status_code=500, detail="report query failed") from error
    return {
        "case_id": case_id,
        "reports": [serialize_report(report) for report in reports]
    }
