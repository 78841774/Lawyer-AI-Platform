from personal_production.schemas import (
    PersonalProductionProviderCapabilities,
    PersonalProductionProviderCapability,
)


PROVIDER_DEFINITIONS = [
    ("openai_provider", "OpenAI / GPT Provider", "ai_model", "ai_gateway_registered_mock_first", "/personal-ai-gateway", True),
    ("deepseek_provider", "DeepSeek Provider", "ai_model", "ai_gateway_registered_mock_first", "/personal-ai-gateway", True),
    ("local_model_provider", "Local Model Provider", "ai_model", "ai_gateway_registered_mock_first", "/personal-ai-gateway", True),
    ("mineru_file_parser_provider", "MinerU File Parser", "file_parser", "material_runtime_registered_mock_first", "/personal-material-runtime", True),
    ("docling_file_parser_provider", "Docling File Parser", "file_parser", "material_runtime_registered_mock_first", "/personal-material-runtime", True),
    ("paddleocr_provider", "PaddleOCR / Baidu AI Studio", "ocr", "material_runtime_registered_mock_first", "/personal-material-runtime", True),
    ("ocr_provider", "OCR Provider", "ocr", "paddleocr_placeholder_registered_in_v7_2", "/personal-material-runtime", True),
    ("kuaicha365_lawskills_provider", "快查 365 LawSkills", "legal_search", "personal_intelligence_gateway_registered_mock_first", "/personal-intelligence", True),
    ("tianyancha_ai_provider", "天眼查 AI", "enterprise_intelligence", "personal_intelligence_gateway_registered_mock_first", "/personal-intelligence", True),
    ("qichacha_provider_placeholder", "企查查 Placeholder", "enterprise_intelligence", "reserved_optional_provider_placeholder", "/personal-intelligence", True),
    ("pkulaw_provider_placeholder", "北大法宝 Placeholder", "legal_search", "reserved_optional_provider_placeholder", "/personal-intelligence", True),
    ("national_law_database_provider_placeholder", "国家法律法规数据库 Placeholder", "legal_search", "reserved_optional_provider_placeholder", "/personal-intelligence", True),
    ("skill_training_provider", "Skill Training Provider", "skill_training", "skill_studio_registered_mock_first", "/personal-skill-studio", True),
]


def build_provider_capabilities() -> dict:
    providers = [
        PersonalProductionProviderCapability(
            provider_id=provider_id,
            label=label,
            category=category,
            next_action=next_action,
            target_route=target_route,
            gateway_registered=gateway_registered,
        )
        for provider_id, label, category, next_action, target_route, gateway_registered in PROVIDER_DEFINITIONS
    ]
    return PersonalProductionProviderCapabilities(
        providers=providers,
        provider_count=len(providers),
        configured_provider_count=sum(1 for provider in providers if provider.configured),
        live_provider_count=sum(1 for provider in providers if provider.live_enabled),
        warnings=["AI、材料/OCR、法律与企业信息网关均为 mock-first。未读取或显示 provider secrets。"],
    ).model_dump()
