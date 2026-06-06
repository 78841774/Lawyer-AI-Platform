from personal_intelligence_gateway.provider_config import enterprise_live_mode_enabled, legal_live_mode_enabled
from personal_intelligence_gateway.schemas import PersonalIntelligenceLiveSafetyStatus, PersonalIntelligenceSafetyStatus


SAFETY_CHECKLIST = [
    "未调用真实法律检索服务",
    "未调用真实企业信息服务",
    "未读取密钥值",
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


LIVE_SAFETY_FLAGS = {
    "legal_live_mode_disabled_by_default": True,
    "enterprise_live_mode_disabled_by_default": True,
    "provider_gated": True,
    "api_key_backend_only": True,
    "api_key_exposed": False,
    "dry_run_ready": True,
    "explicit_confirmation_required": True,
    "legal_raw_result_blocked_by_default": True,
    "enterprise_raw_result_blocked_by_default": True,
    "citation_metadata_candidate_only": True,
    "no_ai_prompt_injection": True,
    "no_fact_extraction_trigger": True,
    "no_legal_analysis_trigger": True,
    "no_final_citation": True,
    "source_trace_required": True,
    "lawyer_review_required": True,
    "audit_required": True,
    "no_final_legal_opinion": True,
    "no_final_report": True,
    "no_external_delivery": True,
}


def build_live_safety_status() -> dict:
    safety = {
        **LIVE_SAFETY_FLAGS,
        "legal_live_mode_currently_enabled": legal_live_mode_enabled(),
        "enterprise_live_mode_currently_enabled": enterprise_live_mode_enabled(),
    }
    return PersonalIntelligenceLiveSafetyStatus(
        safety=safety,
        all_safety_checks_passed=all(value is True for key, value in safety.items() if not key.endswith("_currently_enabled")),
        live_mode_enabled=legal_live_mode_enabled() or enterprise_live_mode_enabled(),
        warnings=[
            "v7.14 Legal / Enterprise API Live Gateway is dry-run first and disabled by default.",
            "Legal and enterprise results remain metadata candidates and are not final citations.",
        ],
    ).model_dump()
