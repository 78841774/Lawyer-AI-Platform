import json
from typing import Any

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.auth import AuthContext, get_auth_context
from app.core.config import settings
from app.core.database import get_db
from app.models.report import Report
from app.repositories.case_repository import CaseRepository
from app.repositories.fact_repository import FactRepository
from app.repositories.legal_analysis_repository import LegalAnalysisRepository
from app.repositories.material_repository import MaterialRepository
from app.repositories.report_repository import ReportRepository
from app.repositories.runtime_run_repository import RuntimeRunRepository
from app.repositories.skill_repository import SkillRepository
from app.repositories.workspace_skill_repository import WorkspaceSkillRepository
from app.services.report_service import ReportService
from app.services.skill_runtime_service import SkillRuntimeService

router = APIRouter(prefix="/cases/{case_id}/reports", tags=["reports"])


def get_report_service(db: Session) -> ReportService:
    return ReportService(
        report_repository=ReportRepository(db),
        fact_repository=FactRepository(db),
        material_repository=MaterialRepository(db),
        legal_analysis_repository=LegalAnalysisRepository(db),
        case_repository=CaseRepository(db),
        storage_root=settings.storage_root,
        skill_runtime_service=SkillRuntimeService(
            skill_repository=SkillRepository(db),
            workspace_skill_repository=WorkspaceSkillRepository(db)
        )
    )


def serialize_report(report: Report) -> dict[str, Any]:
    source_refs = parse_report_source_refs(report.source_refs)
    return {
        "report_id": report.report_id,
        "case_id": report.case_id,
        "report_type": report.report_type,
        "title": report.title,
        "content": report.content,
        "status": report.status,
        "version": report.version,
        "storage_path": report.storage_path,
        "source_refs": source_refs,
        "citations": source_refs.get("citations", []),
        "trace": source_refs.get("trace", {}),
        "citation_summary": source_refs.get("citation_summary", {}),
        "created_at": report.created_at
    }


def parse_report_source_refs(value: str | None) -> dict[str, Any]:
    if not value:
        return {}
    try:
        parsed = json.loads(value)
    except json.JSONDecodeError:
        return {}
    return parsed if isinstance(parsed, dict) else {}


def is_runtime_error(error: ValueError) -> bool:
    message = str(error)
    return (
        message
        in {
            "skill not found",
            "skill not published",
            "package not found",
            "package not published"
        }
        or message.startswith("package file")
    )


@router.post("/generate")
def generate_report(
    case_id: str,
    context: AuthContext = Depends(get_auth_context),
    db: Session = Depends(get_db)
) -> dict[str, Any]:
    case = CaseRepository(db).get_by_case_id(case_id)
    if case is None:
        raise HTTPException(status_code=404, detail="case not found")
    run_repository = RuntimeRunRepository(db)
    run = run_repository.create_report_run(
        case_id=case_id,
        workspace_id=case.workspace_id,
        triggered_by_user_id=context.user.user_id
    )
    service = get_report_service(db)
    try:
        result = service.generate_report_with_runtime(case_id)
    except ValueError as error:
        run_repository.fail_run(run, safe_error_message(error))
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
        if is_runtime_error(error):
            raise HTTPException(status_code=400, detail=str(error)) from error
        if str(error) == "llm generation failed":
            raise HTTPException(status_code=500, detail=str(error)) from error
        raise HTTPException(status_code=500, detail="report generation failed") from error
    except Exception as error:
        run_repository.fail_run(run, safe_error_message(error))
        raise HTTPException(status_code=500, detail="report generation failed") from error
    run = run_repository.complete_report_run(
        run,
        llm_provider=result.llm_provider,
        llm_status=result.llm_status,
        skill_id=result.skill_used,
        package_id=result.package_used,
        analysis_id=result.analysis_id,
        report_id=result.report.report_id,
        source_refs=json.dumps(result.source_refs or {}, ensure_ascii=False)
    )
    response = serialize_report(result.report)
    response["run_id"] = run.run_id
    response["run_type"] = "report_generation"
    response["llm_provider"] = result.llm_provider
    response["llm_status"] = result.llm_status
    response["skill_used"] = result.skill_used
    response["package_used"] = result.package_used
    response["analysis_id"] = result.analysis_id
    response["source_refs"] = result.source_refs or response["source_refs"]
    return response


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


def safe_error_message(error: Exception) -> str:
    message = str(error).strip()
    return message or "runtime execution failed"
