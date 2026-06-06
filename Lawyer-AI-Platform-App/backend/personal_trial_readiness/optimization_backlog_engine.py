from uuid import uuid4

from personal_trial_readiness.schemas import OptimizationBacklogItem, OptimizationBacklogList, OptimizationBacklogMockRequest
from personal_trial_readiness.storage import list_json, write_json


DEFAULT_BACKLOG = [
    OptimizationBacklogItem(
        backlog_id="backlog_mock_001",
        source_trial_id="trial_mock_001",
        source_issue_ids=["issue_mock_001", "issue_mock_002"],
        priority="medium",
        target_area="personal_trial_readiness",
        title="试运行说明与安全边界提示统一优化",
        description="根据 v7.25 试运行观察，把按钮旁提示、诊断摘要和下载边界说明统一到 v7.26。",
        recommended_version="v7.26",
        status="proposed",
    )
]


def list_backlog() -> dict:
    records = [OptimizationBacklogItem(**item) for item in list_json("optimization_backlog")]
    if not records:
        records = DEFAULT_BACKLOG
    return OptimizationBacklogList(backlog_items=records, backlog_count=len(records)).model_dump()


def create_mock_backlog(request: OptimizationBacklogMockRequest) -> dict:
    item = OptimizationBacklogItem(
        backlog_id=f"backlog_{uuid4().hex[:10]}",
        source_trial_id=request.source_trial_id,
        source_issue_ids=request.source_issue_ids,
        priority=request.priority,
        target_area=request.target_area,
        title=request.title,
        description=request.description,
        recommended_version=request.recommended_version,
        status="proposed",
        warnings=["优化 backlog 只用于后续规划，不自动修改 Skill、训练集或交付材料。"],
    )
    write_json("optimization_backlog", item.backlog_id, item.model_dump())
    return item.model_dump()

