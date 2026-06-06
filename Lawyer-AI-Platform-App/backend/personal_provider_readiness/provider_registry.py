from personal_provider_readiness.schemas import ProviderDefinition, ProviderList, ProviderMetadata
from personal_provider_readiness.secret_boundary import key_loaded_for_env_names, key_source_for_env_names


PROVIDER_DEFINITIONS = [
    ProviderDefinition(
        provider_id="openai",
        provider_name="OpenAI",
        provider_category="ai",
        key_env_names=["OPENAI_API_KEY"],
        adapter_registered=False,
        status="registered_live_blocked",
    ),
    ProviderDefinition(
        provider_id="deepseek",
        provider_name="DeepSeek",
        provider_category="ai",
        key_env_names=["DEEPSEEK_API_KEY"],
        adapter_registered=False,
        status="registered_live_blocked",
    ),
    ProviderDefinition(
        provider_id="local_model_placeholder",
        provider_name="Local Model Placeholder",
        provider_category="ai",
        requires_api_key=False,
        key_env_names=[],
        external_transfer_required=False,
        usage_meter_supported=False,
        cost_metadata_supported=False,
        adapter_registered=True,
        status="placeholder_dry_run_ready",
    ),
    ProviderDefinition(
        provider_id="paddleocr_local",
        provider_name="PaddleOCR Local",
        provider_category="ocr",
        requires_api_key=False,
        key_env_names=[],
        external_transfer_required=False,
        usage_meter_supported=False,
        cost_metadata_supported=False,
        adapter_registered=True,
        status="local_dry_run_ready",
    ),
    ProviderDefinition(
        provider_id="baidu_paddle_ai_studio_placeholder",
        provider_name="Baidu Paddle AI Studio Placeholder",
        provider_category="ocr",
        key_env_names=["BAIDU_PADDLE_AI_STUDIO_API_KEY"],
        adapter_registered=False,
        status="placeholder_live_blocked",
    ),
    ProviderDefinition(
        provider_id="mineru_placeholder",
        provider_name="MinerU Placeholder",
        provider_category="document",
        requires_api_key=False,
        key_env_names=[],
        external_transfer_required=False,
        usage_meter_supported=False,
        cost_metadata_supported=False,
        adapter_registered=False,
        status="placeholder_dry_run_ready",
    ),
    ProviderDefinition(
        provider_id="docling_placeholder",
        provider_name="Docling Placeholder",
        provider_category="document",
        requires_api_key=False,
        key_env_names=[],
        external_transfer_required=False,
        usage_meter_supported=False,
        cost_metadata_supported=False,
        adapter_registered=False,
        status="placeholder_dry_run_ready",
    ),
    ProviderDefinition(
        provider_id="kuaicha_365_lawskills_placeholder",
        provider_name="快查 365 LawSkills Placeholder",
        provider_category="legal",
        key_env_names=["KUAICHA365_LAWSKILLS_API_KEY"],
        adapter_registered=False,
        status="placeholder_live_blocked",
    ),
    ProviderDefinition(
        provider_id="legal_search_placeholder",
        provider_name="Legal Search Placeholder",
        provider_category="legal",
        requires_api_key=False,
        key_env_names=[],
        external_transfer_required=False,
        usage_meter_supported=False,
        cost_metadata_supported=False,
        adapter_registered=False,
        status="placeholder_dry_run_ready",
    ),
    ProviderDefinition(
        provider_id="national_law_database_placeholder",
        provider_name="National Law Database Placeholder",
        provider_category="legal",
        requires_api_key=False,
        key_env_names=[],
        external_transfer_required=True,
        usage_meter_supported=False,
        cost_metadata_supported=False,
        adapter_registered=False,
        status="placeholder_live_blocked",
    ),
    ProviderDefinition(
        provider_id="tianyancha_ai_placeholder",
        provider_name="天眼查 AI Placeholder",
        provider_category="enterprise",
        key_env_names=["TIANYANCHA_AI_API_KEY"],
        adapter_registered=False,
        status="placeholder_live_blocked",
    ),
    ProviderDefinition(
        provider_id="qichacha_placeholder",
        provider_name="企查查 Placeholder",
        provider_category="enterprise",
        key_env_names=["QICHACHA_API_KEY"],
        adapter_registered=False,
        status="placeholder_live_blocked",
    ),
    ProviderDefinition(
        provider_id="enterprise_registry_placeholder",
        provider_name="Enterprise Registry Placeholder",
        provider_category="enterprise",
        requires_api_key=False,
        key_env_names=[],
        external_transfer_required=True,
        usage_meter_supported=False,
        cost_metadata_supported=False,
        adapter_registered=False,
        status="placeholder_live_blocked",
    ),
]


def build_provider_metadata(definition: ProviderDefinition) -> ProviderMetadata:
    key_loaded = key_loaded_for_env_names(definition.key_env_names)
    return ProviderMetadata(
        provider_id=definition.provider_id,
        provider_name=definition.provider_name,
        provider_category=definition.provider_category,
        live_supported=definition.live_supported,
        dry_run_supported=definition.dry_run_supported,
        requires_api_key=definition.requires_api_key,
        key_env_names=definition.key_env_names,
        key_loaded=key_loaded if definition.requires_api_key else False,
        key_source=key_source_for_env_names(definition.requires_api_key, definition.key_env_names),
        external_transfer_required=definition.external_transfer_required,
        usage_meter_supported=definition.usage_meter_supported,
        cost_metadata_supported=definition.cost_metadata_supported,
        adapter_registered=definition.adapter_registered,
        status=definition.status,
        warnings=[
            "Only key_loaded boolean metadata is returned; key values, prefixes, suffixes, and masked keys are not returned.",
            "Live calls are blocked by default in v7.26.",
        ],
    )


def list_provider_metadata() -> list[ProviderMetadata]:
    return [build_provider_metadata(definition) for definition in PROVIDER_DEFINITIONS]


def build_provider_list() -> dict:
    providers = list_provider_metadata()
    return ProviderList(
        providers=providers,
        provider_count=len(providers),
        key_loaded_count=sum(1 for provider in providers if provider.key_loaded),
        dry_run_ready_count=sum(1 for provider in providers if provider.dry_run_supported),
        live_disabled_count=len(providers),
        blocked_provider_count=len(providers),
        warnings=["Provider readiness is metadata-only. No provider network call is executed."],
    ).model_dump()


def get_provider(provider_id: str) -> ProviderMetadata | None:
    for provider in list_provider_metadata():
        if provider.provider_id == provider_id:
            return provider
    return None

