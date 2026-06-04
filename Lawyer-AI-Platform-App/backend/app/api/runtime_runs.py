import json
from typing import Any

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.auth import AuthContext, get_auth_context
from app.core.database import get_db
from app.models.case import Case
from app.models.runtime_run import AnalysisRun, ExtractionRun, ReportRun
from app.repositories.case_repository import CaseRepository
from app.repositories.identity_repository import IdentityRepository
from app.repositories.runtime_run_repository import RuntimeRunRepository
from app.services.identity_service import IdentityService

router = APIRouter(prefix="/cases/{case_id}/runtime-runs", tags=["runtime-runs"])


@router.get("")
def list_runtime_runs(
    case_id: str,
    context: AuthContext = Depends(get_auth_context),
    db: Session = Depends(get_db)
) -> dict[str, Any]:
    ensure_case_access(case_id, context, db)
    repository = RuntimeRunRepository(db)
    return {
        "case_id": case_id,
        "extraction_runs": [
            serialize_extraction_run(run)
            for run in repository.list_extraction_runs(case_id)
        ],
        "analysis_runs": [
            serialize_analysis_run(run)
            for run in repository.list_analysis_runs(case_id)
        ],
        "report_runs": [
            serialize_report_run(run)
            for run in repository.list_report_runs(case_id)
        ]
    }


@router.get("/latest")
def latest_runtime_runs(
    case_id: str,
    context: AuthContext = Depends(get_auth_context),
    db: Session = Depends(get_db)
) -> dict[str, Any]:
    ensure_case_access(case_id, context, db)
    repository = RuntimeRunRepository(db)
    extraction_run = repository.latest_extraction_run(case_id)
    analysis_run = repository.latest_analysis_run(case_id)
    report_run = repository.latest_report_run(case_id)
    return {
        "case_id": case_id,
        "latest_extraction_run": serialize_extraction_run(extraction_run) if extraction_run else None,
        "latest_analysis_run": serialize_analysis_run(analysis_run) if analysis_run else None,
        "latest_report_run": serialize_report_run(report_run) if report_run else None
    }


def ensure_case_access(case_id: str, context: AuthContext, db: Session) -> Case:
    case = CaseRepository(db).get_by_case_id(case_id)
    if case is None:
        raise HTTPException(status_code=404, detail="case not found")
    try:
        IdentityService(IdentityRepository(db)).get_user_workspace(context.user, case.workspace_id)
    except PermissionError as error:
        raise HTTPException(status_code=403, detail=str(error)) from error
    except LookupError as error:
        raise HTTPException(status_code=404, detail=str(error)) from error
    return case


def serialize_extraction_run(run: ExtractionRun) -> dict[str, Any]:
    return {
        **serialize_common_run(run, "fact_extraction"),
        "counts": {
            "materials_count": run.materials_count,
            "facts_created_count": run.facts_created_count,
            "facts_reused_count": run.facts_reused_count,
            "facts_skipped_count": run.facts_skipped_count
        },
        "materials_count": run.materials_count,
        "facts_created_count": run.facts_created_count,
        "facts_reused_count": run.facts_reused_count,
        "facts_skipped_count": run.facts_skipped_count,
        "source_material_ids": parse_json_value(run.source_material_ids, [])
    }


def serialize_analysis_run(run: AnalysisRun) -> dict[str, Any]:
    return {
        **serialize_common_run(run, "legal_analysis"),
        "counts": {
            "facts_count": run.facts_count
        },
        "facts_count": run.facts_count,
        "analysis_id": run.analysis_id,
        "source_fact_ids": parse_json_value(run.source_fact_ids, [])
    }


def serialize_report_run(run: ReportRun) -> dict[str, Any]:
    return {
        **serialize_common_run(run, "report_generation"),
        "counts": {},
        "analysis_id": run.analysis_id,
        "report_id": run.report_id
    }


def serialize_common_run(
    run: ExtractionRun | AnalysisRun | ReportRun,
    run_type: str
) -> dict[str, Any]:
    return {
        "run_id": run.run_id,
        "run_type": run_type,
        "case_id": run.case_id,
        "status": run.status,
        "is_latest": run.is_latest,
        "llm_provider": run.llm_provider,
        "llm_status": run.llm_status,
        "skill_id": run.skill_id,
        "package_id": run.package_id,
        "source_refs": parse_json_value(run.source_refs, []),
        "error_message": run.error_message,
        "created_at": run.created_at,
        "completed_at": run.completed_at
    }


def parse_json_value(value: str | None, fallback: Any) -> Any:
    if not value:
        return fallback
    try:
        return json.loads(value)
    except json.JSONDecodeError:
        return fallback
