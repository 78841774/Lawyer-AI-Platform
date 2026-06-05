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
    ("legal_search_provider", "Legal Search Provider", "legal_search", "configure_legal_search_gateway_in_v7_3", "/personal-production", False),
    ("case_law_provider", "Case Law API Provider", "legal_search", "configure_case_law_gateway_in_v7_3", "/personal-production", False),
    ("skill_training_provider", "Skill Training Provider", "skill_training", "configure_skill_studio_in_v7_4", "/personal-production", False),
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
        warnings=["AI and Material/OCR gateways are registered for mock-first use. No provider secrets are read or displayed."],
    ).model_dump()
