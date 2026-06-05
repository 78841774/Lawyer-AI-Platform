from personal_skill_studio.schemas import SkillStudioSafetyStatus


SAFETY_CHECKLIST = [
    "未读取真实案件原文",
    "未调用真实 AI provider",
    "未生成最终法律意见",
    "未生成最终报告",
    "未自动发布 Skill",
    "未写入正式 Skill Registry",
    "律师复核必需",
    "人工确认必需",
    "来源追踪必需",
    "仅生成经验包草案和技能候选草案",
]

SAFETY_FLAGS = {
    "raw_case_content_read": False,
    "live_ai_call_executed": False,
    "final_legal_opinion_generated": False,
    "final_report_generated": False,
    "auto_publish_enabled": False,
    "published_to_registry": False,
    "requires_lawyer_review": True,
    "requires_manual_confirmation": True,
    "source_trace_required": True,
    "mock_metadata_only": True,
}


def default_safety_flags() -> dict[str, bool]:
    return dict(SAFETY_FLAGS)


def build_safety_status() -> dict:
    return SkillStudioSafetyStatus(
        safety_checklist=SAFETY_CHECKLIST,
        safety_flags=default_safety_flags(),
        warnings=["v7.4 仅生成经验包草案、技能候选草案和模拟评估，不会自动发布 Skill。"],
    ).model_dump()
