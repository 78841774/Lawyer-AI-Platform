from typing import Any

from fastapi import APIRouter

from personal_alpha_final_readiness.readiness_engine import (
    get_personal_alpha_final_readiness_run,
    get_personal_alpha_final_readiness_status,
    get_personal_alpha_final_readiness_summary,
)

router = APIRouter(prefix="/personal-alpha-final-readiness", tags=["personal-alpha-final-readiness"])


@router.get("/status")
def personal_alpha_final_readiness_status() -> dict[str, Any]:
    return get_personal_alpha_final_readiness_status()


@router.get("/run/{workspace_run_id}")
def personal_alpha_final_readiness_run(workspace_run_id: str) -> dict[str, Any]:
    return get_personal_alpha_final_readiness_run(workspace_run_id)


@router.get("/run/{workspace_run_id}/summary")
def personal_alpha_final_readiness_summary(workspace_run_id: str) -> dict[str, Any]:
    return get_personal_alpha_final_readiness_summary(workspace_run_id)
