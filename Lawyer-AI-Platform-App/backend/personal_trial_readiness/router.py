from typing import Any

from fastapi import APIRouter, HTTPException

from personal_trial_readiness.audit_engine import build_audit_timeline
from personal_trial_readiness.issue_log_engine import create_mock_issue, list_issues, require_issue
from personal_trial_readiness.optimization_backlog_engine import create_mock_backlog, list_backlog
from personal_trial_readiness.quality_review_engine import build_quality_review, create_mock_quality_review
from personal_trial_readiness.safety_confirmation_engine import build_safety_confirmation, create_mock_safety_confirmation
from personal_trial_readiness.safety_engine import build_safety_status, build_status
from personal_trial_readiness.schemas import (
    IssueLogMockRequest,
    OptimizationBacklogMockRequest,
    StageObservationMockRequest,
    TrialSessionMockRequest,
)
from personal_trial_readiness.stage_observation_engine import create_mock_observation, list_observations
from personal_trial_readiness.trial_checklist_engine import build_checklist, create_mock_checklist
from personal_trial_readiness.trial_session_engine import create_mock_trial, get_trial, list_trials


router = APIRouter(prefix="/personal-trial-readiness", tags=["personal-trial-readiness"])


@router.get("/status")
def status() -> dict[str, Any]:
    return build_status()


@router.get("/checklist")
def checklist() -> dict[str, Any]:
    return build_checklist().model_dump()


@router.get("/safety")
def safety() -> dict[str, Any]:
    return build_safety_status()


@router.post("/trials/mock")
def create_trial(request: TrialSessionMockRequest) -> dict[str, Any]:
    return create_mock_trial(request)


@router.get("/trials")
def trials() -> dict[str, Any]:
    return list_trials()


@router.get("/trials/{trial_id}")
def trial_detail(trial_id: str) -> dict[str, Any]:
    trial = get_trial(trial_id)
    if trial is None:
        raise HTTPException(status_code=404, detail="trial_id 不存在")
    return trial.model_dump()


@router.get("/trials/{trial_id}/checklist")
def trial_checklist(trial_id: str) -> dict[str, Any]:
    return build_checklist(trial_id).model_dump()


@router.post("/trials/{trial_id}/checklist/mock")
def trial_checklist_mock(trial_id: str) -> dict[str, Any]:
    return create_mock_checklist(trial_id)


@router.get("/trials/{trial_id}/observations")
def observations(trial_id: str) -> dict[str, Any]:
    return list_observations(trial_id)


@router.post("/trials/{trial_id}/observations/mock")
def observations_mock(trial_id: str, request: StageObservationMockRequest) -> dict[str, Any]:
    return create_mock_observation(trial_id, request)


@router.get("/trials/{trial_id}/issues")
def trial_issues(trial_id: str) -> dict[str, Any]:
    return list_issues(trial_id)


@router.post("/trials/{trial_id}/issues/mock")
def issues_mock(trial_id: str, request: IssueLogMockRequest) -> dict[str, Any]:
    return create_mock_issue(trial_id, request)


@router.get("/issues")
def issues() -> dict[str, Any]:
    return list_issues()


@router.get("/issues/{issue_id}")
def issue_detail(issue_id: str) -> dict[str, Any]:
    return require_issue(issue_id).model_dump()


@router.get("/trials/{trial_id}/quality")
def quality(trial_id: str) -> dict[str, Any]:
    return build_quality_review(trial_id).model_dump()


@router.post("/trials/{trial_id}/quality/mock")
def quality_mock(trial_id: str) -> dict[str, Any]:
    return create_mock_quality_review(trial_id)


@router.get("/trials/{trial_id}/safety-confirmation")
def safety_confirmation(trial_id: str) -> dict[str, Any]:
    return build_safety_confirmation(trial_id).model_dump()


@router.post("/trials/{trial_id}/safety-confirmation/mock")
def safety_confirmation_mock(trial_id: str) -> dict[str, Any]:
    return create_mock_safety_confirmation(trial_id)


@router.get("/optimization-backlog")
def optimization_backlog() -> dict[str, Any]:
    return list_backlog()


@router.post("/optimization-backlog/mock")
def optimization_backlog_mock(request: OptimizationBacklogMockRequest) -> dict[str, Any]:
    return create_mock_backlog(request)


@router.get("/audit")
def audit() -> dict[str, Any]:
    return build_audit_timeline()

