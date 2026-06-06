from typing import Any

from fastapi import APIRouter, HTTPException

from personal_production_pilot.audit_engine import build_audit_timeline
from personal_production_pilot.dashboard_engine import (
    build_dashboard_metrics,
    build_dashboard_safety,
    build_dashboard_status,
    build_quality_items,
)
from personal_production_pilot.document_output_engine import build_output_list, build_skill_final_drafts, create_mock_output, get_output
from personal_production_pilot.export_boundary import build_export_boundary
from personal_production_pilot.owner_download_engine import build_owner_download_list, create_owner_download, get_owner_download
from personal_production_pilot.pilot_orchestrator import build_case_analysis_summary, build_run_list, create_mock_run, get_run
from personal_production_pilot.pilot_readiness import build_readiness
from personal_production_pilot.pilot_registry import list_runtimes
from personal_production_pilot.provider_gate_summary import build_provider_gate_summary
from personal_production_pilot.review_queue import build_review_queue, submit_review_action
from personal_production_pilot.safety_engine import build_safety_status
from personal_production_pilot.schemas import (
    OwnerDownloadMockRequest,
    PilotOutputMockRequest,
    PilotReviewActionRequest,
    PilotRunMockRequest,
    PilotStatus,
)
from personal_production_pilot.source_trace_engine import build_source_trace_list
from personal_production_pilot.workflow_engine import build_workflow


router = APIRouter(prefix="/personal-production-pilot", tags=["personal-production-pilot"])


@router.get("/status")
def status() -> dict[str, Any]:
    return PilotStatus(
        warnings=[
            "v7.17 is the closing pilot for the v7.10-v7.17 large stage.",
            "Real providers remain disabled by default and require explicit confirmation before eligibility.",
            "Owner downloads are metadata only; no public link, email, final legal opinion, formal report, or external delivery is triggered.",
        ],
    ).model_dump()


@router.get("/readiness")
def readiness() -> dict[str, Any]:
    return build_readiness()


@router.get("/workflow")
def workflow() -> dict[str, Any]:
    return build_workflow()


@router.get("/runtimes")
def runtimes() -> dict[str, Any]:
    return list_runtimes()


@router.get("/provider-gates")
def provider_gates() -> dict[str, Any]:
    return build_provider_gate_summary()


@router.get("/safety")
def safety() -> dict[str, Any]:
    return build_safety_status()


@router.post("/runs/mock")
def run_mock(request: PilotRunMockRequest) -> dict[str, Any]:
    return create_mock_run(request)


@router.post("/runs")
def run_controlled(request: PilotRunMockRequest) -> dict[str, Any]:
    return create_mock_run(request)


@router.get("/runs")
def runs() -> dict[str, Any]:
    return build_run_list()


@router.get("/runs/{run_id}")
def run_detail(run_id: str) -> dict[str, Any]:
    record = get_run(run_id)
    if record is None:
        raise HTTPException(status_code=404, detail="run_id 不存在")
    return record.model_dump()


@router.get("/case-analysis-summary")
def case_analysis_summary() -> dict[str, Any]:
    return build_case_analysis_summary()


@router.get("/skill-final-drafts")
def skill_final_drafts() -> dict[str, Any]:
    return build_skill_final_drafts()


@router.get("/skill-final-drafts/{draft_id}")
def skill_final_draft_detail(draft_id: str) -> dict[str, Any]:
    drafts = build_skill_final_drafts()["skill_final_drafts"]
    for draft in drafts:
        if draft["draft_id"] == draft_id:
            return draft
    raise HTTPException(status_code=404, detail="draft_id 不存在")


@router.post("/outputs/mock")
def output_mock(request: PilotOutputMockRequest) -> dict[str, Any]:
    return create_mock_output(request)


@router.get("/outputs")
def outputs() -> dict[str, Any]:
    return build_output_list()


@router.get("/outputs/{output_id}")
def output_detail(output_id: str) -> dict[str, Any]:
    record = get_output(output_id)
    if record is None:
        raise HTTPException(status_code=404, detail="output_id 不存在")
    return record.model_dump()


@router.post("/outputs/{output_id}/owner-downloads/mock")
def owner_download_mock(output_id: str, request: OwnerDownloadMockRequest) -> dict[str, Any]:
    return create_owner_download(output_id, request)


@router.get("/owner-downloads")
def owner_downloads() -> dict[str, Any]:
    return build_owner_download_list()


@router.get("/owner-downloads/{download_id}")
def owner_download_detail(download_id: str) -> dict[str, Any]:
    record = get_owner_download(download_id)
    if record is None:
        raise HTTPException(status_code=404, detail="download_id 不存在")
    return record.model_dump()


@router.get("/review-queue")
def review_queue() -> dict[str, Any]:
    return build_review_queue()


@router.post("/review-queue/{review_item_id}/actions")
def review_action(review_item_id: str, request: PilotReviewActionRequest) -> dict[str, Any]:
    return submit_review_action(review_item_id, request)


@router.get("/source-traces")
def source_traces() -> dict[str, Any]:
    return build_source_trace_list()


@router.get("/audit")
def audit() -> dict[str, Any]:
    return build_audit_timeline()


@router.get("/export-boundary")
def export_boundary() -> dict[str, Any]:
    return build_export_boundary()


@router.get("/dashboard/status")
def dashboard_status() -> dict[str, Any]:
    return build_dashboard_status()


@router.get("/dashboard/metrics")
def dashboard_metrics() -> dict[str, Any]:
    return build_dashboard_metrics()


@router.get("/dashboard/quality")
def dashboard_quality() -> dict[str, Any]:
    return build_quality_items()


@router.get("/dashboard/safety")
def dashboard_safety() -> dict[str, Any]:
    return build_dashboard_safety()
