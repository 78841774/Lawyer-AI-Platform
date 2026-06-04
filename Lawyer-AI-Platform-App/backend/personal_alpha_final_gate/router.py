from typing import Any

from fastapi import APIRouter

from personal_alpha_final_gate.gate_engine import (
    get_personal_alpha_final_gate_run,
    get_personal_alpha_final_gate_status,
    get_personal_alpha_final_gate_summary,
    list_gate_decisions_for_run,
    submit_gate_decision_for_run,
)
from personal_alpha_final_gate.schemas import PersonalAlphaFinalGateDecisionRequest

router = APIRouter(prefix="/personal-alpha-final-gate", tags=["personal-alpha-final-gate"])


@router.get("/status")
def personal_alpha_final_gate_status() -> dict[str, Any]:
    return get_personal_alpha_final_gate_status()


@router.get("/run/{workspace_run_id}")
def personal_alpha_final_gate_run(workspace_run_id: str) -> dict[str, Any]:
    return get_personal_alpha_final_gate_run(workspace_run_id)


@router.get("/run/{workspace_run_id}/summary")
def personal_alpha_final_gate_summary(workspace_run_id: str) -> dict[str, Any]:
    return get_personal_alpha_final_gate_summary(workspace_run_id)


@router.get("/run/{workspace_run_id}/decisions")
def personal_alpha_final_gate_decisions(workspace_run_id: str) -> dict[str, Any]:
    return list_gate_decisions_for_run(workspace_run_id)


@router.post("/run/{workspace_run_id}/decisions")
def personal_alpha_final_gate_submit_decision(workspace_run_id: str, request: PersonalAlphaFinalGateDecisionRequest) -> dict[str, Any]:
    return submit_gate_decision_for_run(workspace_run_id, request)
