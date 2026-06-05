from typing import Any

from fastapi import APIRouter, HTTPException

from personal_showcase_pack.audit_engine import build_audit_timeline
from personal_showcase_pack.pilot_sample_runtime import build_pilot_sample_list, create_mock_pilot_sample, get_pilot_sample
from personal_showcase_pack.safety_engine import build_safety_status
from personal_showcase_pack.schemas import PersonalShowcasePackStatus, PilotSampleMockRequest, StoryFlowMockRequest
from personal_showcase_pack.showcase_metrics import build_showcase_metrics
from personal_showcase_pack.showcase_runtime import get_runtime, list_runtimes
from personal_showcase_pack.story_flow_runtime import build_story_flow_list, create_mock_story_flow, get_story_flow
from personal_showcase_pack.trust_panel_engine import build_trust_panel


router = APIRouter(prefix="/personal-showcase-pack", tags=["personal-showcase-pack"])


@router.get("/status")
def status() -> dict[str, Any]:
    return PersonalShowcasePackStatus(
        warnings=["v7.7 当前仅为个人生产试点与展示包 mock metadata，不会调用真实 provider、生成最终意见或对外交付。"],
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


@router.post("/pilot-samples/mock")
def pilot_sample_mock(request: PilotSampleMockRequest) -> dict[str, Any]:
    return create_mock_pilot_sample(request)


@router.get("/pilot-samples")
def pilot_samples() -> dict[str, Any]:
    return build_pilot_sample_list()


@router.get("/pilot-samples/{pilot_sample_id}")
def pilot_sample_detail(pilot_sample_id: str) -> dict[str, Any]:
    record = get_pilot_sample(pilot_sample_id)
    if record is None:
        raise HTTPException(status_code=404, detail="pilot_sample_id 不存在")
    return record.model_dump()


@router.post("/story-flows/mock")
def story_flow_mock(request: StoryFlowMockRequest) -> dict[str, Any]:
    return create_mock_story_flow(request)


@router.get("/story-flows")
def story_flows() -> dict[str, Any]:
    return build_story_flow_list()


@router.get("/story-flows/{story_flow_id}")
def story_flow_detail(story_flow_id: str) -> dict[str, Any]:
    record = get_story_flow(story_flow_id)
    if record is None:
        raise HTTPException(status_code=404, detail="story_flow_id 不存在")
    return record.model_dump()


@router.get("/metrics")
def metrics() -> dict[str, Any]:
    return build_showcase_metrics()


@router.get("/trust-panel")
def trust_panel() -> dict[str, Any]:
    return build_trust_panel()


@router.get("/audit")
def audit() -> dict[str, Any]:
    return build_audit_timeline()


@router.get("/safety")
def safety() -> dict[str, Any]:
    return build_safety_status()
