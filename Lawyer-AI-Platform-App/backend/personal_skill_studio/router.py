from typing import Any

from fastapi import APIRouter, HTTPException

from personal_skill_studio.audit_engine import build_audit_timeline
from personal_skill_studio.evaluation_runtime import build_evaluation_list, create_mock_evaluation, get_evaluation
from personal_skill_studio.experience_package_runtime import build_experience_package_list, create_mock_experience_package, get_experience_package
from personal_skill_studio.provider_registry import get_runtime, list_runtimes
from personal_skill_studio.promotion_gate import build_promotion_queue, submit_promotion_action
from personal_skill_studio.safety_engine import build_final_drafts_safety_status, build_safety_status
from personal_skill_studio.schemas import (
    EvaluationMockRequest,
    ExperiencePackageMockRequest,
    PersonalSkillStudioStatus,
    PromotionActionRequest,
    SkillCandidateMockRequest,
    SkillFinalOwnerDownloadRequest,
    TestCaseMockRequest,
)
from personal_skill_studio.skill_baseline_discovery import build_baseline_discovery_metadata
from personal_skill_studio.skill_candidate_runtime import build_skill_candidate_list, create_mock_skill_candidate, get_skill_candidate
from personal_skill_studio.skill_final_audit_engine import build_skill_final_audit
from personal_skill_studio.skill_final_download_engine import (
    build_skill_final_owner_download_list,
    create_skill_final_owner_download,
    get_skill_final_owner_download,
)
from personal_skill_studio.skill_final_draft_engine import get_skill_final_draft, list_skill_final_drafts
from personal_skill_studio.skill_final_gate_engine import build_skill_final_gate
from personal_skill_studio.skill_final_quality_engine import build_skill_final_quality
from personal_skill_studio.skill_final_source_trace_engine import build_skill_final_source_traces
from personal_skill_studio.skill_lineage_engine import build_skill_lineage
from personal_skill_studio.skill_optimization_engine import build_skill_optimization
from personal_skill_studio.skill_sample_registry import build_skill_sample_registry
from personal_skill_studio.skill_training_runtime import build_runtime as build_skill_training_runtime
from personal_skill_studio.source_trace_engine import build_source_trace_list, get_source_trace
from personal_skill_studio.test_case_runtime import build_test_case_list, create_mock_test_case, get_test_case
from personal_skill_studio.training_artifacts.router import router as training_artifacts_router


router = APIRouter(prefix="/personal-skill-studio", tags=["personal-skill-studio"])
router.include_router(training_artifacts_router)


@router.get("/status")
def status() -> dict[str, Any]:
    return PersonalSkillStudioStatus(
        version="v7.22",
        warnings=["v7.22 增加两个 Skill 最终稿与优化工作台。仅生成 owner-only metadata，不会真实训练或自动发布 Skill。"],
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


@router.get("/skill-training/status")
def skill_training_status() -> dict[str, Any]:
    return build_skill_training_runtime()


@router.get("/skill-training/sample-registry")
def skill_training_sample_registry() -> dict[str, Any]:
    return build_skill_sample_registry()


@router.post("/experience-packages/mock")
def experience_package_mock(request: ExperiencePackageMockRequest) -> dict[str, Any]:
    return create_mock_experience_package(request)


@router.get("/experience-packages")
def experience_packages() -> dict[str, Any]:
    return build_experience_package_list()


@router.get("/experience-packages/{experience_package_id}")
def experience_package_detail(experience_package_id: str) -> dict[str, Any]:
    record = get_experience_package(experience_package_id)
    if record is None:
        raise HTTPException(status_code=404, detail="experience_package_id 不存在")
    return record.model_dump()


@router.post("/skill-candidates/mock")
def skill_candidate_mock(request: SkillCandidateMockRequest) -> dict[str, Any]:
    return create_mock_skill_candidate(request)


@router.get("/skill-candidates")
def skill_candidates() -> dict[str, Any]:
    return build_skill_candidate_list()


@router.get("/skill-candidates/{skill_candidate_id}")
def skill_candidate_detail(skill_candidate_id: str) -> dict[str, Any]:
    record = get_skill_candidate(skill_candidate_id)
    if record is None:
        raise HTTPException(status_code=404, detail="skill_candidate_id 不存在")
    return record.model_dump()


@router.post("/test-cases/mock")
def test_case_mock(request: TestCaseMockRequest) -> dict[str, Any]:
    return create_mock_test_case(request)


@router.get("/test-cases")
def test_cases() -> dict[str, Any]:
    return build_test_case_list()


@router.get("/test-cases/{test_case_id}")
def test_case_detail(test_case_id: str) -> dict[str, Any]:
    record = get_test_case(test_case_id)
    if record is None:
        raise HTTPException(status_code=404, detail="test_case_id 不存在")
    return record.model_dump()


@router.post("/evaluations/mock")
def evaluation_mock(request: EvaluationMockRequest) -> dict[str, Any]:
    return create_mock_evaluation(request)


@router.get("/evaluations")
def evaluations() -> dict[str, Any]:
    return build_evaluation_list()


@router.get("/evaluations/{evaluation_id}")
def evaluation_detail(evaluation_id: str) -> dict[str, Any]:
    record = get_evaluation(evaluation_id)
    if record is None:
        raise HTTPException(status_code=404, detail="evaluation_id 不存在")
    return record.model_dump()


@router.get("/promotion-queue")
def promotion_queue() -> dict[str, Any]:
    return build_promotion_queue()


@router.post("/promotion-queue/{skill_candidate_id}/actions")
def promotion_action(skill_candidate_id: str, request: PromotionActionRequest) -> dict[str, Any]:
    return submit_promotion_action(skill_candidate_id, request)


@router.get("/final-drafts")
def skill_final_drafts() -> dict[str, Any]:
    return list_skill_final_drafts()


@router.get("/final-drafts/{skill_id}")
def skill_final_draft_detail(skill_id: str) -> dict[str, Any]:
    draft = get_skill_final_draft(skill_id)
    if draft is None:
        raise HTTPException(status_code=404, detail="skill_id 不存在")
    return draft.model_dump()


@router.get("/final-drafts/{skill_id}/lineage")
def skill_final_lineage(skill_id: str) -> dict[str, Any]:
    lineage = build_skill_lineage(skill_id)
    if lineage is None:
        raise HTTPException(status_code=404, detail="skill_id 不存在")
    return lineage.model_dump()


@router.get("/final-drafts/{skill_id}/baseline")
def skill_final_baseline(skill_id: str) -> dict[str, Any]:
    draft = get_skill_final_draft(skill_id)
    if draft is None:
        raise HTTPException(status_code=404, detail="skill_id 不存在")
    discovery = build_baseline_discovery_metadata()
    return discovery.model_dump()


@router.get("/final-drafts/{skill_id}/quality")
def skill_final_quality(skill_id: str) -> dict[str, Any]:
    quality = build_skill_final_quality(skill_id)
    if quality is None:
        raise HTTPException(status_code=404, detail="skill_id 不存在")
    return quality.model_dump()


@router.get("/final-drafts/{skill_id}/gate")
def skill_final_gate(skill_id: str) -> dict[str, Any]:
    gate = build_skill_final_gate(skill_id)
    if gate is None:
        raise HTTPException(status_code=404, detail="skill_id 不存在")
    return gate.model_dump()


@router.get("/final-drafts/{skill_id}/optimization")
def skill_final_optimization(skill_id: str) -> dict[str, Any]:
    optimization = build_skill_optimization(skill_id)
    if optimization is None:
        raise HTTPException(status_code=404, detail="skill_id 不存在")
    return optimization.model_dump()


@router.get("/final-drafts/{skill_id}/source-traces")
def skill_final_source_traces(skill_id: str) -> dict[str, Any]:
    traces = build_skill_final_source_traces(skill_id)
    if traces is None:
        raise HTTPException(status_code=404, detail="skill_id 不存在")
    return traces.model_dump()


@router.get("/final-drafts/{skill_id}/audit")
def skill_final_audit(skill_id: str) -> dict[str, Any]:
    timeline = build_skill_final_audit(skill_id)
    if timeline is None:
        raise HTTPException(status_code=404, detail="skill_id 不存在")
    return timeline.model_dump()


@router.post("/final-drafts/{skill_id}/owner-downloads/mock")
def skill_final_owner_download_mock(skill_id: str, request: SkillFinalOwnerDownloadRequest) -> dict[str, Any]:
    return create_skill_final_owner_download(skill_id, request)


@router.get("/final-draft-downloads")
def skill_final_downloads() -> dict[str, Any]:
    return build_skill_final_owner_download_list()


@router.get("/final-draft-downloads/{download_id}")
def skill_final_download_detail(download_id: str) -> dict[str, Any]:
    record = get_skill_final_owner_download(download_id)
    if record is None:
        raise HTTPException(status_code=404, detail="download_id 不存在")
    return record.model_dump()


@router.get("/final-drafts-safety")
def skill_final_safety() -> dict[str, Any]:
    return build_final_drafts_safety_status()


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
