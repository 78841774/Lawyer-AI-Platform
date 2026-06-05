from personal_case_production.schemas import WorkflowStage, WorkflowStageList


STAGE_DEFINITIONS = [
    ("case_intake_stage", "案件录入阶段", "case_intake", ["案件 metadata 检查", "脱敏状态记录", "生产流程准备度检查"]),
    ("material_processing_stage", "材料处理阶段", "material_processing", ["关联 v7.2 Material Runtime metadata", "记录 OCR/解析状态", "标记是否经过人工复核"]),
    ("ai_draft_stage", "AI 草稿阶段", "ai_draft", ["关联 v7.1 AI Gateway metadata", "草稿状态记录", "不生成最终意见"]),
    ("intelligence_check_stage", "法律与企业信息核验阶段", "intelligence_check", ["关联 v7.3 Personal Intelligence metadata", "source trace 状态", "律师确认状态"]),
    ("skill_studio_stage", "经验包与技能沉淀阶段", "skill_studio", ["关联 v7.4 Skill Studio metadata", "经验包草案状态", "技能候选草案状态"]),
    ("lawyer_review_stage", "律师复核阶段", "lawyer_review", ["人工复核记录", "request revision / approve / reject", "final gate 前置确认"]),
    ("final_readiness_stage", "最终准备度阶段", "final_readiness", ["最终交付前检查", "未生成最终法律意见", "未生成最终报告", "未对外交付"]),
]


def list_stages() -> dict:
    stages = [WorkflowStage(stage_id=stage_id, display_name=name, stage_type=stage_type, capabilities=capabilities) for stage_id, name, stage_type, capabilities in STAGE_DEFINITIONS]
    return WorkflowStageList(workflow_stages=stages, stage_count=len(stages), warnings=["当前仅为受控生产流程骨架。"]).model_dump()


def get_stage(stage_id: str) -> WorkflowStage | None:
    for stage in list_stages()["workflow_stages"]:
        if stage.get("stage_id") == stage_id:
            return WorkflowStage(**stage)
    return None


def required_stage_ids() -> list[str]:
    return [stage_id for stage_id, _, _, _ in STAGE_DEFINITIONS]
