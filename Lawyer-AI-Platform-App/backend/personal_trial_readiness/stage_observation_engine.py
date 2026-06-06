from uuid import uuid4

from personal_trial_readiness.schemas import StageObservation, StageObservationList, StageObservationMockRequest
from personal_trial_readiness.storage import list_json, write_json


STAGES = [
    ("case_intake", "案件录入"),
    ("material_workspace", "材料工作台"),
    ("ocr_review", "OCR 状态复核"),
    ("fact_preview", "事实预览"),
    ("fact_correction", "事实输入纠正"),
    ("legal_analysis_draft", "法律分析草稿"),
    ("skill_final_drafts", "Skill 最终稿"),
    ("owner_output_center", "用户本人产出下载中心"),
    ("trust_safety", "Trust / Safety 面板"),
    ("diagnostics", "Developer Diagnostics"),
]


def _stage_name(stage_id: str) -> str:
    return dict(STAGES).get(stage_id, stage_id)


def default_observations(trial_id: str) -> list[StageObservation]:
    observations = []
    for index, (stage_id, stage_name) in enumerate(STAGES):
        observations.append(
            StageObservation(
                trial_id=trial_id,
                stage_id=stage_id,
                stage_name=stage_name,
                usability_score=84 - index % 4,
                quality_score=82 - index % 3,
                issue_count=0 if index < 6 else 1,
                optimization_suggestions=[
                    "保持中文状态文案，避免像调试页面。",
                    "继续突出 metadata-only、律师复核必需和不自动对外交付。",
                ],
            )
        )
    return observations


def list_observations(trial_id: str) -> dict:
    records = [
        StageObservation(**item)
        for item in list_json("observations")
        if item.get("trial_id") == trial_id
    ]
    if not records:
        records = default_observations(trial_id)
    return StageObservationList(trial_id=trial_id, observations=records, observation_count=len(records)).model_dump()


def create_mock_observation(trial_id: str, request: StageObservationMockRequest) -> dict:
    observation = StageObservation(
        trial_id=trial_id,
        stage_id=request.stage_id,
        stage_name=_stage_name(request.stage_id),
        issue_count=max(0, int(request.issue_count)),
        notes=request.notes,
        optimization_suggestions=["该观察仅进入 v7.26 优化 backlog，不阻断当前试运行。"],
    )
    object_id = f"{trial_id}_{request.stage_id}_{uuid4().hex[:8]}"
    write_json("observations", object_id, observation.model_dump())
    return observation.model_dump()

