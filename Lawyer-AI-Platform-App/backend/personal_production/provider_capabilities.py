from personal_production.schemas import (
    PersonalProductionProviderCapabilities,
    PersonalProductionProviderCapability,
)


PROVIDER_DEFINITIONS = [
    ("openai_provider", "OpenAI / GPT Provider", "ai_model", "configure_provider_gateway_in_v7_1"),
    ("deepseek_provider", "DeepSeek Provider", "ai_model", "configure_provider_gateway_in_v7_1"),
    ("local_model_provider", "Local Model Provider", "ai_model", "configure_local_model_gateway_in_v7_1"),
    ("ocr_provider", "OCR Provider", "ocr", "configure_controlled_ocr_runtime_in_v7_2"),
    ("legal_search_provider", "Legal Search Provider", "legal_search", "configure_legal_search_gateway_in_v7_3"),
    ("case_law_provider", "Case Law API Provider", "legal_search", "configure_case_law_gateway_in_v7_3"),
    ("skill_training_provider", "Skill Training Provider", "skill_training", "configure_skill_studio_in_v7_4"),
]


def build_provider_capabilities() -> dict:
    providers = [
        PersonalProductionProviderCapability(
            provider_id=provider_id,
            label=label,
            category=category,
            next_action=next_action,
        )
        for provider_id, label, category, next_action in PROVIDER_DEFINITIONS
    ]
    return PersonalProductionProviderCapabilities(
        providers=providers,
        provider_count=len(providers),
        configured_provider_count=sum(1 for provider in providers if provider.configured),
        live_provider_count=sum(1 for provider in providers if provider.live_enabled),
        warnings=["Provider capabilities are placeholders only. No provider secrets are read or displayed."],
    ).model_dump()
