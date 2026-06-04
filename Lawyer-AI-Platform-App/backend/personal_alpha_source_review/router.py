from typing import Any

from fastapi import APIRouter

from personal_alpha_source_review.decision_engine import (
    get_decision_summary_for_run,
    list_decisions_for_run,
    submit_decision_for_run,
)
from personal_alpha_source_review.schemas import PersonalAlphaSourceReviewDecisionRequest
from personal_alpha_source_review.source_review_engine import (
    get_personal_alpha_evidence_summary,
    get_personal_alpha_source_review_run,
    get_personal_alpha_source_review_status,
    get_personal_alpha_source_traces,
)

router = APIRouter(prefix="/personal-alpha-source-review", tags=["personal-alpha-source-review"])


@router.get("/status")
def personal_alpha_source_review_status() -> dict[str, Any]:
    return get_personal_alpha_source_review_status()


@router.get("/run/{workspace_run_id}")
def personal_alpha_source_review_run(workspace_run_id: str) -> dict[str, Any]:
    return get_personal_alpha_source_review_run(workspace_run_id)


@router.get("/run/{workspace_run_id}/source-traces")
def personal_alpha_source_review_source_traces(workspace_run_id: str) -> dict[str, Any]:
    return get_personal_alpha_source_traces(workspace_run_id)


@router.get("/run/{workspace_run_id}/evidence-summary")
def personal_alpha_source_review_evidence_summary(workspace_run_id: str) -> dict[str, Any]:
    return get_personal_alpha_evidence_summary(workspace_run_id)


@router.get("/run/{workspace_run_id}/decisions")
def personal_alpha_source_review_decisions(workspace_run_id: str) -> dict[str, Any]:
    return list_decisions_for_run(workspace_run_id)


@router.post("/run/{workspace_run_id}/decisions")
def personal_alpha_source_review_submit_decision(workspace_run_id: str, request: PersonalAlphaSourceReviewDecisionRequest) -> dict[str, Any]:
    return submit_decision_for_run(workspace_run_id, request)


@router.get("/run/{workspace_run_id}/decision-summary")
def personal_alpha_source_review_decision_summary(workspace_run_id: str) -> dict[str, Any]:
    return get_decision_summary_for_run(workspace_run_id)
