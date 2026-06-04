import json
from typing import Any

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.auth import AuthContext, get_auth_context
from app.core.database import get_db
from app.models.fact import Fact
from app.models.material import Material
from app.repositories.case_repository import CaseRepository
from app.repositories.fact_repository import FactRepository
from app.repositories.material_repository import MaterialRepository
from app.repositories.runtime_run_repository import RuntimeRunRepository
from app.repositories.skill_repository import SkillRepository
from app.repositories.workspace_skill_repository import WorkspaceSkillRepository
from app.services.fact_service import FactService
from app.services.skill_runtime_service import SkillRuntimeService

router = APIRouter(prefix="/cases/{case_id}/facts", tags=["facts"])


def get_fact_service(db: Session) -> FactService:
    return FactService(
        fact_repository=FactRepository(db),
        material_repository=MaterialRepository(db),
        case_repository=CaseRepository(db),
        skill_runtime_service=SkillRuntimeService(
            skill_repository=SkillRepository(db),
            workspace_skill_repository=WorkspaceSkillRepository(db)
        )
    )


def serialize_fact(
    fact: Fact,
    material_lookup: dict[str, Material] | None = None
) -> dict[str, Any]:
    material = (material_lookup or {}).get(fact.material_id)
    return {
        "fact_id": fact.fact_id,
        "case_id": fact.case_id,
        "material_id": fact.material_id,
        "content": fact.content,
        "fact_type": fact.fact_type,
        "confidence": fact.confidence,
        "source_text": fact.source_text,
        "source_refs": {
            "material_id": fact.material_id,
            "filename": material.filename if material else None,
            "relative_path": (material.relative_path or material.filename) if material else None
        },
        "status": fact.status,
        "created_at": fact.created_at
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


@router.post("/extract")
def extract_facts(
    case_id: str,
    context: AuthContext = Depends(get_auth_context),
    db: Session = Depends(get_db)
) -> dict[str, Any]:
    case = CaseRepository(db).get_by_case_id(case_id)
    if case is None:
        raise HTTPException(status_code=404, detail="case not found")
    run_repository = RuntimeRunRepository(db)
    run = run_repository.create_extraction_run(
        case_id=case_id,
        workspace_id=case.workspace_id,
        triggered_by_user_id=context.user.user_id
    )
    service = get_fact_service(db)
    try:
        result = service.extract_facts_with_runtime(case_id)
    except ValueError as error:
        run_repository.fail_run(run, safe_error_message(error))
        if str(error) == "case not found":
            raise HTTPException(status_code=404, detail=str(error)) from error
        if is_runtime_error(error):
            raise HTTPException(status_code=400, detail=str(error)) from error
        if str(error) == "llm generation failed":
            raise HTTPException(status_code=500, detail=str(error)) from error
        raise HTTPException(status_code=500, detail="fact extraction failed") from error
    except Exception as error:
        run_repository.fail_run(run, safe_error_message(error))
        raise HTTPException(status_code=500, detail="fact extraction failed") from error
    material_lookup = build_material_lookup(db, case_id)
    run = run_repository.complete_extraction_run(
        run,
        llm_provider=result.llm_provider,
        llm_status=result.llm_status,
        skill_id=result.skill_used,
        package_id=result.package_used,
        materials_count=result.materials_count,
        facts_created_count=result.facts_created_count,
        facts_reused_count=result.facts_reused_count,
        facts_skipped_count=result.facts_skipped_count,
        source_material_ids=json.dumps(
            [ref["material_id"] for ref in result.source_refs or []],
            ensure_ascii=False
        ),
        source_refs=json.dumps(result.source_refs or [], ensure_ascii=False)
    )
    response = {
        "case_id": case_id,
        "run_id": run.run_id,
        "run_type": "fact_extraction",
        "status": run.status,
        "facts": [serialize_fact(fact, material_lookup) for fact in result.facts],
        "llm_provider": result.llm_provider,
        "llm_status": result.llm_status,
        "skill_used": result.skill_used,
        "package_used": result.package_used,
        "materials_count": result.materials_count,
        "facts_created_count": result.facts_created_count,
        "facts_reused_count": result.facts_reused_count,
        "facts_skipped_count": result.facts_skipped_count,
        "source_refs": result.source_refs or []
    }
    return response


@router.get("")
def list_facts(
    case_id: str,
    db: Session = Depends(get_db)
) -> dict[str, Any]:
    service = get_fact_service(db)
    try:
        facts = service.list_facts(case_id)
    except ValueError as error:
        raise HTTPException(status_code=404, detail=str(error)) from error
    material_lookup = build_material_lookup(db, case_id)
    return {
        "case_id": case_id,
        "facts": [serialize_fact(fact, material_lookup) for fact in facts]
    }


def build_material_lookup(db: Session, case_id: str) -> dict[str, Material]:
    return {
        material.material_id: material
        for material in MaterialRepository(db).list_by_case_id(case_id)
    }


def safe_error_message(error: Exception) -> str:
    message = str(error).strip()
    return message or "runtime execution failed"
