from personal_intelligence_gateway.schemas import PersonalIntelligenceSafetyStatus


SAFETY_CHECKLIST = [
    "未调用真实法律检索服务",
    "未调用真实企业信息服务",
    "未读取 API key",
    "未返回原始外部内容",
    "未自动引用检索结果",
    "未自动送入 AI Prompt",
    "未生成最终法律意见",
    "未生成最终报告",
    "律师确认必需",
    "来源追踪必需",
    "仅返回模拟 metadata",
]

SAFETY_FLAGS = {
    "live_legal_search_executed": False,
    "live_enterprise_query_executed": False,
    "api_key_accessed": False,
    "raw_external_content_returned": False,
    "auto_citation_used": False,
    "used_in_ai_prompt": False,
    "final_legal_opinion_generated": False,
    "final_report_generated": False,
    "requires_lawyer_confirmation": True,
    "source_trace_required": True,
    "mock_metadata_only": True,
}


def default_safety_flags() -> dict[str, bool]:
    return dict(SAFETY_FLAGS)


def build_safety_status() -> dict:
    return PersonalIntelligenceSafetyStatus(
        safety_checklist=SAFETY_CHECKLIST,
        safety_flags=default_safety_flags(),
        all_safety_checks_passed=True,
        warnings=["v7.3 仅返回模拟 metadata，未调用真实法律或企业信息服务。"],
    ).model_dump()
