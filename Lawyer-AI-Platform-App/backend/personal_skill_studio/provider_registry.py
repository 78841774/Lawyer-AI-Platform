from personal_skill_studio.schemas import PersonalSkillStudioRuntime, PersonalSkillStudioRuntimeList


RUNTIME_DEFINITIONS = [
    {
        "runtime_id": "experience_package_studio_runtime",
        "display_name": "经验包工作室",
        "runtime_type": "experience_package_studio",
        "capabilities": ["经验包草案生成", "来源追踪聚合", "安全边界检查", "律师复核状态记录"],
    },
    {
        "runtime_id": "skill_candidate_studio_runtime",
        "display_name": "技能候选工作室",
        "runtime_type": "skill_candidate_studio",
        "capabilities": ["技能候选草案生成", "prompt template 草案", "reasoning pattern 草案", "limitation / safety note 草案"],
    },
    {
        "runtime_id": "skill_test_case_runtime",
        "display_name": "技能测试用例工作室",
        "runtime_type": "skill_test_case",
        "capabilities": ["mock test case 生成", "input / expected behavior metadata", "source trace mapping", "review-required 标记"],
    },
    {
        "runtime_id": "skill_evaluation_runtime",
        "display_name": "技能评估工作室",
        "runtime_type": "skill_evaluation",
        "capabilities": ["mock evaluation checklist", "scoring metadata", "risk flags", "manual review gate"],
    },
    {
        "runtime_id": "skill_training_runtime",
        "display_name": "受控 Skill Training Runtime",
        "runtime_type": "skill_training",
        "capabilities": ["脱敏训练样本 metadata", "人工确认门禁", "draft-only training metadata", "no auto publish"],
    },
    {
        "runtime_id": "controlled_promotion_gate",
        "display_name": "受控发布门禁",
        "runtime_type": "promotion_gate",
        "capabilities": ["publish readiness metadata", "manual approval required", "no auto publish"],
    },
    {
        "runtime_id": "skill_final_draft_workbench",
        "display_name": "两个 Skill 最终稿与优化工作台",
        "runtime_type": "skill_final_draft",
        "capabilities": ["baseline discovery metadata", "owner-only final draft metadata", "reference-only quality / gate", "no auto publish"],
    },
]


def list_runtimes() -> dict:
    runtimes = [PersonalSkillStudioRuntime(**definition) for definition in RUNTIME_DEFINITIONS]
    return PersonalSkillStudioRuntimeList(
        runtimes=runtimes,
        runtime_count=len(runtimes),
        live_runtime_count=sum(1 for runtime in runtimes if runtime.live_enabled),
        warnings=["Skill Studio Runtime 仅生成草案、模拟评估和最终稿 metadata，不会自动发布 Skill。"],
    ).model_dump()


def get_runtime(runtime_id: str) -> PersonalSkillStudioRuntime | None:
    for runtime in list_runtimes()["runtimes"]:
        if runtime.get("runtime_id") == runtime_id:
            return PersonalSkillStudioRuntime(**runtime)
    return None
