from personal_case_production.schemas import CaseProductionSafetyStatus


SAFETY_CHECKLIST = [
    "未读取真实案件原文",
    "未调用真实 provider",
    "未读取 API key",
    "未生成最终法律意见",
    "未生成最终报告",
    "未自动对外交付",
    "律师复核必需",
    "最终门禁必需",
    "来源追踪必需",
    "仅返回生产流程 metadata",
]

SAFETY_FLAGS = {
    "raw_case_content_read": False,
    "live_provider_call_executed": False,
    "api_key_accessed": False,
    "final_legal_opinion_generated": False,
    "final_report_generated": False,
    "external_delivery_triggered": False,
    "requires_lawyer_review": True,
    "final_gate_required": True,
    "source_trace_required": True,
    "mock_metadata_only": True,
}


def default_safety_flags() -> dict[str, bool]:
    return dict(SAFETY_FLAGS)


def build_safety_status() -> dict:
    return CaseProductionSafetyStatus(
        safety_checklist=SAFETY_CHECKLIST,
        safety_flags=default_safety_flags(),
        warnings=["v7.5 当前仅为真实案件生产流程骨架，不会生成最终法律意见、最终报告或对外交付。"],
    ).model_dump()
