import json
from typing import Any

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.models.legal_analysis import LegalAnalysis
from app.repositories.case_repository import CaseRepository
from app.repositories.fact_repository import FactRepository
from app.repositories.legal_analysis_repository import LegalAnalysisRepository
from app.repositories.skill_repository import SkillRepository
from app.repositories.workspace_skill_repository import WorkspaceSkillRepository
from app.services.legal_analysis_service import LegalAnalysisService
from app.services.skill_runtime_service import SkillRuntimeService

router = APIRouter(prefix="/cases/{case_id}/analysis", tags=["legal-analysis"])


def get_legal_analysis_service(db: Session) -> LegalAnalysisService:
    return LegalAnalysisService(
        legal_analysis_repository=LegalAnalysisRepository(db),
        fact_repository=FactRepository(db),
        case_repository=CaseRepository(db),
        skill_runtime_service=SkillRuntimeService(
            skill_repository=SkillRepository(db),
            workspace_skill_repository=WorkspaceSkillRepository(db)
        )
    )


def serialize_analysis(analysis: LegalAnalysis) -> dict[str, Any]:
    return {
        "analysis_id": analysis.analysis_id,
        "case_id": analysis.case_id,
        "issues": json.loads(analysis.issues),
        "rules": json.loads(analysis.rules),
        "reasoning": json.loads(analysis.reasoning),
        "conclusion": analysis.conclusion,
        "risk_level": analysis.risk_level,
        "confidence": analysis.confidence,
        "status": analysis.status,
        "created_at": analysis.created_at
    }


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


@router.post("/run")
def run_analysis(
    case_id: str,
    db: Session = Depends(get_db)
) -> dict[str, Any]:
    service = get_legal_analysis_service(db)
    try:
        result = service.run_analysis_with_runtime(case_id)
    except ValueError as error:
        if str(error) == "case not found":
            raise HTTPException(status_code=404, detail=str(error)) from error
        if str(error) == "facts required":
            raise HTTPException(
                status_code=400,
                detail="facts required: run Fact Runtime before Legal Analysis Runtime"
            ) from error
        if is_runtime_error(error):
            raise HTTPException(status_code=400, detail=str(error)) from error
        if str(error) == "llm generation failed":
            raise HTTPException(status_code=500, detail=str(error)) from error
        raise HTTPException(status_code=500, detail="analysis generation failed") from error
    except Exception as error:
        raise HTTPException(status_code=500, detail="analysis generation failed") from error
    response = serialize_analysis(result.analysis)
    response["llm_provider"] = result.llm_provider
    response["llm_status"] = result.llm_status
    response["skill_used"] = result.skill_used
    response["package_used"] = result.package_used
    return response


@router.get("")
def list_analyses(
    case_id: str,
    db: Session = Depends(get_db)
) -> dict[str, Any]:
    service = get_legal_analysis_service(db)
    try:
        analyses = service.list_analyses(case_id)
    except ValueError as error:
        raise HTTPException(status_code=404, detail=str(error)) from error
    except Exception as error:
        raise HTTPException(status_code=500, detail="analysis query failed") from error
    return {
        "case_id": case_id,
        "analyses": [serialize_analysis(analysis) for analysis in analyses]
    }
