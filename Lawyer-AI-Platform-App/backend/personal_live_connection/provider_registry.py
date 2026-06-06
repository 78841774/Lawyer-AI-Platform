import os

from personal_live_connection.schemas import LiveConnectionProvider, LiveConnectionProviderList


PROVIDERS = [
    ("openai", "OpenAI", "ai", "ai_model", "OPENAI_API_KEY", True, False),
    ("deepseek", "DeepSeek", "ai", "ai_model", "DEEPSEEK_API_KEY", True, False),
    ("local_model_placeholder", "Local Model Placeholder", "ai", "local_model", None, False, True),
    ("paddleocr", "PaddleOCR", "ocr", "ocr", None, False, True),
    ("baidu_ocr_placeholder", "百度 OCR Placeholder", "ocr", "ocr", "BAIDU_OCR_API_KEY", True, False),
    ("mineru", "MinerU Document Parser", "document", "document_parser", None, False, False),
    ("docling", "Docling Document Parser", "document", "document_parser", None, False, False),
    ("kuaicha365_lawskills_provider", "快查 365 LawSkills", "legal", "legal_search", "KUAICHA365_LAWSKILLS_API_KEY", True, False),
    ("pkulaw_provider_placeholder", "北大法宝 Placeholder", "legal", "legal_search", "PKULAW_API_KEY", True, False),
    ("national_law_database_provider_placeholder", "国家法律法规数据库 Placeholder", "legal", "legal_search", None, False, False),
    ("tianyancha_ai_provider", "天眼查 AI", "enterprise", "enterprise_info", "TIANYANCHA_AI_API_KEY", True, False),
    ("qichacha_provider_placeholder", "企查查 Placeholder", "enterprise", "enterprise_info", "QICHACHA_API_KEY", True, False),
]


def global_live_enabled() -> bool:
    return _env_enabled("PERSONAL_LIVE_CONNECTION_ENABLED")


def provider_live_enabled(provider_id: str) -> bool:
    return global_live_enabled() and _env_enabled(f"PERSONAL_LIVE_PROVIDER_{provider_id.upper()}_ENABLED")


def build_provider(provider_id: str) -> LiveConnectionProvider | None:
    for current_id, name, category, provider_type, key_env, key_required, adapter_registered in PROVIDERS:
        if current_id != provider_id:
            continue
        key_loaded = bool(key_env and key_env in os.environ)
        return LiveConnectionProvider(
            provider_id=current_id,
            display_name=name,
            provider_category=category,
            provider_type=provider_type,
            key_env_name=key_env,
            key_loaded=key_loaded if key_required else False,
            key_source="env" if key_loaded else "not_required" if not key_required else "unavailable",
            key_required=key_required,
            provider_live_enabled=False,
            adapter_registered=adapter_registered,
            usage_meter_supported=category == "ai",
            cost_metadata_supported=True,
            warnings=[
                "Provider is registered for controlled live connection readiness.",
                "Only key_loaded boolean metadata is returned; key values are not read or returned.",
                "Live calls are disabled by default and remain blocked unless all future gates pass.",
            ],
        )
    return None


def list_providers() -> list[LiveConnectionProvider]:
    return [provider for provider_id, *_ in PROVIDERS if (provider := build_provider(provider_id)) is not None]


def build_provider_list() -> dict:
    providers = list_providers()
    return LiveConnectionProviderList(
        providers=providers,
        provider_count=len(providers),
        category_count=len({provider.provider_category for provider in providers}),
        dry_run_ready_count=sum(1 for provider in providers if provider.dry_run_ready),
        key_loaded_count=sum(1 for provider in providers if provider.key_loaded),
        live_disabled_count=len(providers),
        blocked_provider_count=len(providers),
        warnings=["Unified live connection providers are metadata-only and live-disabled by default."],
    ).model_dump()


def _env_enabled(name: str) -> bool:
    value = os.environ.get(name)
    return bool(value and value.strip().lower() in {"1", "true", "yes", "on"})

