import json
from typing import Any

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session

from app.core.auth import AuthContext, get_auth_context
from app.core.database import get_db
from app.models.case import Case
from app.repositories.case_repository import CaseRepository
from app.repositories.fact_repository import FactRepository
from app.repositories.identity_repository import IdentityRepository
from app.repositories.legal_analysis_repository import LegalAnalysisRepository
from app.repositories.material_repository import MaterialRepository
from app.repositories.report_repository import ReportRepository
from app.services.case_service import CaseService
from app.services.identity_service import IdentityService

router = APIRouter(prefix="/cases", tags=["cases"])


class CaseCreate(BaseModel):
    case_id: str | None = None
    title: str = "MVP Demo Case"
    description: str | None = None
    client_name: str | None = None
    counterparty_name: str | None = None
    opposing_party: str | None = None
    case_type: str | None = "contract_dispute"
    contract_type: str | None = None
    dispute_amount: str | None = None
    status: str = "draft"
    parties: list[dict[str, Any]] = Field(default_factory=list)
    objective: str | None = None
    jurisdiction: str | None = None
    intake_notes: str | None = None
    priority: str | None = None
    tags: list[str] = Field(default_factory=list)


def serialize_case(case: Case) -> dict[str, Any]:
    return {
        "case_id": case.case_id,
        "title": case.title,
        "description": case.description,
        "client_name": case.client_name,
        "counterparty_name": case.counterparty_name,
        "opposing_party": case.opposing_party,
        "case_type": case.case_type,
        "contract_type": case.contract_type,
        "dispute_amount": case.dispute_amount,
        "status": case.status,
        "objective": case.objective,
        "jurisdiction": case.jurisdiction,
        "intake_notes": case.intake_notes,
        "intake_status": None,
        "priority": case.priority,
        "tags": parse_case_tags(case.tags),
        "workspace_id": case.workspace_id,
        "owner_user_id": case.owner_user_id,
        "created_at": case.created_at,
        "updated_at": case.updated_at
    }


def parse_case_tags(value: str | None) -> list[str]:
    if not value:
        return []
    try:
        parsed = json.loads(value)
    except json.JSONDecodeError:
        return [value]
    if not isinstance(parsed, list):
        return []
    return [str(item) for item in parsed]


def build_intake_status(case: Case, db: Session) -> dict[str, Any]:
    materials_count = len(MaterialRepository(db).list_by_case_id(case.case_id))
    facts_count = len(FactRepository(db).list_by_case_id(case.case_id))
    analyses_count = len(LegalAnalysisRepository(db).list_by_case_id(case.case_id))
    reports_count = len(ReportRepository(db).list_by_case_id(case.case_id))

    has_materials = materials_count > 0
    ready_for_fact_extraction = has_materials and facts_count == 0
    ready_for_analysis = facts_count > 0 and analyses_count == 0
    ready_for_report = analyses_count > 0 and reports_count == 0
    next_recommended_action = resolve_next_action(
        has_materials=has_materials,
        facts_count=facts_count,
        analyses_count=analyses_count,
        reports_count=reports_count
    )

    return {
        "case_id": case.case_id,
        "intake_status": next_recommended_action,
        "has_materials": has_materials,
        "materials_count": materials_count,
        "facts_count": facts_count,
        "analyses_count": analyses_count,
        "reports_count": reports_count,
        "ready_for_fact_extraction": ready_for_fact_extraction,
        "ready_for_analysis": ready_for_analysis,
        "ready_for_report": ready_for_report,
        "next_recommended_action": next_recommended_action
    }


def resolve_next_action(
    *,
    has_materials: bool,
    facts_count: int,
    analyses_count: int,
    reports_count: int
) -> str:
    if reports_count > 0:
        return "review_report"
    if analyses_count > 0:
        return "generate_report"
    if facts_count > 0:
        return "run_analysis"
    if has_materials:
        return "extract_facts"
    return "upload_material"


@router.get("")
def list_cases(
    context: AuthContext = Depends(get_auth_context),
    db: Session = Depends(get_db)
) -> list[dict[str, Any]]:
    identity_service = IdentityService(IdentityRepository(db))
    service = CaseService(CaseRepository(db))
    workspace_ids = [
        workspace.workspace_id
        for workspace in identity_service.list_user_workspaces(context.user)
    ]
    return [
        serialize_case(case)
        for case in service.list_cases_for_workspaces(workspace_ids)
    ]


@router.post("")
def create_case(
    payload: CaseCreate | None = None,
    context: AuthContext = Depends(get_auth_context),
    db: Session = Depends(get_db)
) -> dict[str, Any]:
    case_payload = payload or CaseCreate()
    identity_service = IdentityService(IdentityRepository(db))
    service = CaseService(CaseRepository(db))

    try:
        workspace = identity_service.get_first_active_workspace(context.user)
        if workspace is None:
            raise ValueError("current user has no active workspace")
        case = service.create_case(
            case_id=case_payload.case_id,
            title=case_payload.title,
            description=case_payload.description,
            client_name=case_payload.client_name,
            counterparty_name=case_payload.counterparty_name,
            opposing_party=case_payload.opposing_party,
            case_type=case_payload.case_type,
            contract_type=case_payload.contract_type,
            dispute_amount=case_payload.dispute_amount,
            status=case_payload.status,
            objective=case_payload.objective,
            jurisdiction=case_payload.jurisdiction,
            intake_notes=case_payload.intake_notes,
            priority=case_payload.priority,
            tags=case_payload.tags,
            workspace_id=workspace.workspace_id,
            owner_user_id=context.user.user_id
        )
    except ValueError as error:
        detail = str(error)
        if "case_id already exists" in detail:
            status_code = 409
        elif "no active workspace" in detail:
            status_code = 400
        else:
            status_code = 404
        raise HTTPException(status_code=status_code, detail=detail) from error
    except PermissionError as error:
        raise HTTPException(status_code=403, detail=str(error)) from error
    except LookupError as error:
        raise HTTPException(status_code=404, detail=str(error)) from error
    return serialize_case(case)


@router.get("/{case_id}/intake/status")
def get_case_intake_status(
    case_id: str,
    context: AuthContext = Depends(get_auth_context),
    db: Session = Depends(get_db)
) -> dict[str, Any]:
    identity_service = IdentityService(IdentityRepository(db))
    service = CaseService(CaseRepository(db))
    case = service.get_case(case_id)
    if case is None:
        raise HTTPException(status_code=404, detail="case not found")
    try:
        identity_service.get_user_workspace(context.user, case.workspace_id)
    except PermissionError as error:
        raise HTTPException(status_code=403, detail=str(error)) from error
    except LookupError as error:
        raise HTTPException(status_code=404, detail=str(error)) from error
    return build_intake_status(case, db)


@router.get("/{case_id}")
def get_case(
    case_id: str,
    context: AuthContext = Depends(get_auth_context),
    db: Session = Depends(get_db)
) -> dict[str, Any]:
    identity_service = IdentityService(IdentityRepository(db))
    service = CaseService(CaseRepository(db))
    case = service.get_case(case_id)
    if case is None:
        raise HTTPException(status_code=404, detail="case not found")
    try:
        identity_service.get_user_workspace(context.user, case.workspace_id)
    except PermissionError as error:
        raise HTTPException(status_code=403, detail=str(error)) from error
    except LookupError as error:
        raise HTTPException(status_code=404, detail=str(error)) from error
    return serialize_case(case)
