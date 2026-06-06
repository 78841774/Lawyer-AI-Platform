from typing import Any

from fastapi import APIRouter, HTTPException

from personal_case_analysis.audit_engine import build_audit_timeline
from personal_case_analysis.case_analysis_runtime import build_run_list, create_mock_run, get_run
from personal_case_analysis.evaluation_engine import build_evaluation_list, build_gate_list, get_evaluation, get_gate
from personal_case_analysis.fact_analysis_engine import build_fact_draft_list, create_mock_fact_draft, get_fact_draft
from personal_case_analysis.legal_analysis_draft_engine import (
    build_legal_draft_gate,
    build_legal_draft_list,
    build_legal_draft_quality,
    confirm_legal_draft_for_review,
    create_legal_analysis_draft,
    create_legal_draft_version,
    get_legal_draft,
    list_legal_draft_versions,
)
from personal_case_analysis.review_queue import build_review_queue, submit_review_action
from personal_case_analysis.runtime_registry import get_runtime, list_runtimes
from personal_case_analysis.safety_engine import build_safety_status
from personal_case_analysis.schemas import (
    CaseAnalysisRunMockRequest,
    FactDraftMockRequest,
    LegalDraftMockRequest,
    LegalDraftReviewConfirmRequest,
    LegalDraftVersionMockRequest,
    PersonalCaseAnalysisStatus,
    ReviewActionRequest,
)
from personal_case_analysis.skill_loader import build_skill_baseline_report
from personal_case_analysis.source_trace_engine import build_source_trace_list, get_source_trace


router = APIRouter(prefix="/personal-case-analysis", tags=["personal-case-analysis"])


@router.get("/status")
def status() -> dict[str, Any]:
    return PersonalCaseAnalysisStatus(
        warnings=[
            "v7.21 法律分析草稿工作台基于事实输入 metadata 生成 legal draft。",
            "输出仅为 legal analysis draft metadata，不产生训练数据，不生成最终法律意见或最终报告。",
        ],
    ).model_dump()


@router.get("/runtimes")
def runtimes() -> dict[str, Any]:
    return list_runtimes()


@router.get("/runtimes/{runtime_id}")
def runtime_detail(runtime_id: str) -> dict[str, Any]:
    runtime = get_runtime(runtime_id)
    if runtime is None:
        raise HTTPException(status_code=404, detail="runtime_id 不存在")
    return runtime.model_dump()


@router.get("/skill-baselines")
def skill_baselines() -> dict[str, Any]:
    return build_skill_baseline_report()


@router.post("/runs/mock")
def run_mock(request: CaseAnalysisRunMockRequest) -> dict[str, Any]:
    return create_mock_run(request)


@router.post("/runs")
def run_controlled(request: CaseAnalysisRunMockRequest) -> dict[str, Any]:
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


@router.post("/fact-drafts/mock")
def fact_draft_mock(request: FactDraftMockRequest) -> dict[str, Any]:
    return create_mock_fact_draft(request)


@router.get("/fact-drafts")
def fact_drafts() -> dict[str, Any]:
    return build_fact_draft_list()


@router.get("/fact-drafts/{draft_id}")
def fact_draft_detail(draft_id: str) -> dict[str, Any]:
    record = get_fact_draft(draft_id)
    if record is None:
        raise HTTPException(status_code=404, detail="draft_id 不存在")
    return record.model_dump()


@router.post("/legal-drafts/mock")
def legal_draft_mock(request: LegalDraftMockRequest) -> dict[str, Any]:
    return create_legal_analysis_draft(request)


@router.get("/legal-drafts")
def legal_drafts() -> dict[str, Any]:
    return build_legal_draft_list()


@router.get("/legal-drafts/{draft_id}")
def legal_draft_detail(draft_id: str) -> dict[str, Any]:
    record = get_legal_draft(draft_id)
    if record is None:
        raise HTTPException(status_code=404, detail="draft_id 不存在")
    return record.model_dump()


@router.get("/legal-drafts/{draft_id}/versions")
def legal_draft_versions(draft_id: str) -> dict[str, Any]:
    record = list_legal_draft_versions(draft_id)
    if record is None:
        raise HTTPException(status_code=404, detail="draft_id 不存在")
    return record.model_dump()


@router.post("/legal-drafts/{draft_id}/versions/mock")
def legal_draft_version_mock(draft_id: str, request: LegalDraftVersionMockRequest) -> dict[str, Any]:
    record = create_legal_draft_version(draft_id, request)
    if record is None:
        raise HTTPException(status_code=404, detail="draft_id 不存在")
    return record.model_dump()


@router.get("/legal-drafts/{draft_id}/quality")
def legal_draft_quality(draft_id: str) -> dict[str, Any]:
    record = build_legal_draft_quality(draft_id)
    if record is None:
        raise HTTPException(status_code=404, detail="draft_id 不存在")
    return record.model_dump()


@router.get("/legal-drafts/{draft_id}/gate")
def legal_draft_gate(draft_id: str) -> dict[str, Any]:
    record = build_legal_draft_gate(draft_id)
    if record is None:
        raise HTTPException(status_code=404, detail="draft_id 不存在")
    return record.model_dump()


@router.post("/legal-drafts/{draft_id}/confirm-for-review/mock")
def legal_draft_confirm_for_review(draft_id: str, request: LegalDraftReviewConfirmRequest) -> dict[str, Any]:
    record = confirm_legal_draft_for_review(draft_id, request)
    if record is None:
        raise HTTPException(status_code=404, detail="draft_id 不存在")
    return record.model_dump()


@router.get("/review-queue")
def review_queue() -> dict[str, Any]:
    return build_review_queue()


@router.post("/review-queue/{review_item_id}/actions")
def review_action(review_item_id: str, request: ReviewActionRequest) -> dict[str, Any]:
    return submit_review_action(review_item_id, request)


@router.get("/evaluations")
def evaluations() -> dict[str, Any]:
    return build_evaluation_list()


@router.get("/evaluations/{evaluation_id}")
def evaluation_detail(evaluation_id: str) -> dict[str, Any]:
    record = get_evaluation(evaluation_id)
    if record is None:
        raise HTTPException(status_code=404, detail="evaluation_id 不存在")
    return record.model_dump()


@router.get("/gates")
def gates() -> dict[str, Any]:
    return build_gate_list()


@router.get("/gates/{gate_id}")
def gate_detail(gate_id: str) -> dict[str, Any]:
    record = get_gate(gate_id)
    if record is None:
        raise HTTPException(status_code=404, detail="gate_id 不存在")
    return record.model_dump()


@router.get("/source-traces")
def source_traces() -> dict[str, Any]:
    return build_source_trace_list()


@router.get("/source-traces/{source_trace_id}")
def source_trace_detail(source_trace_id: str) -> dict[str, Any]:
    record = get_source_trace(source_trace_id)
    if record is None:
        raise HTTPException(status_code=404, detail="source_trace_id 不存在")
    return record.model_dump()


@router.get("/audit")
def audit() -> dict[str, Any]:
    return build_audit_timeline()


@router.get("/safety")
def safety() -> dict[str, Any]:
    return build_safety_status()
