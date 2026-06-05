from typing import Any

from fastapi import APIRouter, HTTPException

from personal_case_production.audit_engine import build_audit_timeline
from personal_case_production.case_production_runtime import build_production_case_list, create_mock_production_case, get_production_case
from personal_case_production.readiness_engine import build_case_readiness, build_readiness_list
from personal_case_production.review_gate import build_review_gate_queue, submit_review_gate_action
from personal_case_production.safety_engine import build_safety_status
from personal_case_production.schemas import (
    PersonalCaseProductionStatus,
    ProductionCaseMockRequest,
    ReviewGateActionRequest,
    StageRunMockRequest,
    WorkflowRunMockRequest,
)
from personal_case_production.source_trace_engine import build_source_trace_list, get_source_trace
from personal_case_production.stage_orchestrator import (
    build_stage_run_list,
    build_workflow_run_list,
    create_mock_stage_run,
    create_mock_workflow_run,
    get_stage_run,
    get_workflow_run,
)
from personal_case_production.workflow_registry import get_stage, list_stages


router = APIRouter(prefix="/personal-case-production", tags=["personal-case-production"])


@router.get("/status")
def status() -> dict[str, Any]:
    return PersonalCaseProductionStatus(
        warnings=["v7.5 当前仅为真实案件生产流程骨架，不会生成最终法律意见、最终报告或对外交付。"],
    ).model_dump()


@router.get("/workflow-stages")
def workflow_stages() -> dict[str, Any]:
    return list_stages()


@router.get("/workflow-stages/{stage_id}")
def workflow_stage_detail(stage_id: str) -> dict[str, Any]:
    stage = get_stage(stage_id)
    if stage is None:
        raise HTTPException(status_code=404, detail="stage_id 不存在")
    return stage.model_dump()


@router.post("/cases/mock")
def production_case_mock(request: ProductionCaseMockRequest) -> dict[str, Any]:
    return create_mock_production_case(request)


@router.get("/cases")
def production_cases() -> dict[str, Any]:
    return build_production_case_list()


@router.get("/cases/{production_case_id}")
def production_case_detail(production_case_id: str) -> dict[str, Any]:
    record = get_production_case(production_case_id)
    if record is None:
        raise HTTPException(status_code=404, detail="production_case_id 不存在")
    return record.model_dump()


@router.post("/workflow-runs/mock")
def workflow_run_mock(request: WorkflowRunMockRequest) -> dict[str, Any]:
    return create_mock_workflow_run(request)


@router.get("/workflow-runs")
def workflow_runs() -> dict[str, Any]:
    return build_workflow_run_list()


@router.get("/workflow-runs/{workflow_run_id}")
def workflow_run_detail(workflow_run_id: str) -> dict[str, Any]:
    record = get_workflow_run(workflow_run_id)
    if record is None:
        raise HTTPException(status_code=404, detail="workflow_run_id 不存在")
    return record.model_dump()


@router.post("/stage-runs/mock")
def stage_run_mock(request: StageRunMockRequest) -> dict[str, Any]:
    return create_mock_stage_run(request)


@router.get("/stage-runs")
def stage_runs() -> dict[str, Any]:
    return build_stage_run_list()


@router.get("/stage-runs/{stage_run_id}")
def stage_run_detail(stage_run_id: str) -> dict[str, Any]:
    record = get_stage_run(stage_run_id)
    if record is None:
        raise HTTPException(status_code=404, detail="stage_run_id 不存在")
    return record.model_dump()


@router.get("/readiness")
def readiness() -> dict[str, Any]:
    return build_readiness_list()


@router.get("/readiness/{production_case_id}")
def readiness_detail(production_case_id: str) -> dict[str, Any]:
    record = build_case_readiness(production_case_id)
    if record is None:
        raise HTTPException(status_code=404, detail="production_case_id 不存在")
    return record


@router.get("/review-gates")
def review_gates() -> dict[str, Any]:
    return build_review_gate_queue()


@router.post("/review-gates/{production_case_id}/actions")
def review_gate_action(production_case_id: str, request: ReviewGateActionRequest) -> dict[str, Any]:
    return submit_review_gate_action(production_case_id, request)


@router.get("/source-traces")
def source_traces() -> dict[str, Any]:
    return build_source_trace_list()


@router.get("/source-traces/{source_trace_id}")
def source_trace_detail(source_trace_id: str) -> dict[str, Any]:
    trace = get_source_trace(source_trace_id)
    if trace is None:
        raise HTTPException(status_code=404, detail="source_trace_id 不存在")
    return trace.model_dump()


@router.get("/audit")
def audit() -> dict[str, Any]:
    return build_audit_timeline()


@router.get("/safety")
def safety() -> dict[str, Any]:
    return build_safety_status()
