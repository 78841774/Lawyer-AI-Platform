from personal_material_runtime.provider_config import get_live_provider_config, list_live_provider_configs
from personal_material_runtime.schemas import PersonalMaterialLiveProviderReadiness, PersonalMaterialLiveProviderReadinessList


PROVIDER_KEY_ENVS = {
    "paddleocr": [],
    "mineru": [],
    "docling": [],
    "local_document_parser_placeholder": [],
}


def _provider_category(provider_type: str) -> str:
    return "ocr" if provider_type == "ocr" else "document"


def _adapter_registered(provider_id: str) -> bool:
    return provider_id in {"paddleocr"}


def build_provider_readiness(provider_id: str) -> PersonalMaterialLiveProviderReadiness | None:
    provider = get_live_provider_config(provider_id)
    if provider is None:
        return None
    key_env_names = PROVIDER_KEY_ENVS.get(provider.provider_id, [])
    return PersonalMaterialLiveProviderReadiness(
        provider_id=provider.provider_id,
        display_name=provider.display_name,
        provider_type=provider.provider_type,
        provider_category=_provider_category(provider.provider_type),
        live_supported=provider.live_supported,
        live_enabled=False,
        dry_run_ready=True,
        key_required=provider.key_required,
        key_loaded=provider.key_loaded,
        key_source=provider.key_source,
        key_env_names=key_env_names,
        adapter_registered=_adapter_registered(provider.provider_id),
        supported_file_types=provider.supported_file_types,
        max_file_size_mb=provider.max_file_size_mb,
        supports_page_range=provider.supports_page_range,
        supports_bbox=provider.supports_bbox,
        supports_table_extraction=provider.supports_table_extraction,
        supports_layout_extraction=provider.supports_layout_extraction,
        timeout_seconds=provider.timeout_seconds,
        safety_notes=[
            *provider.safety_notes,
            "v7.27 only returns dry-run readiness metadata.",
            "Provider calls, uploads, raw OCR text, and raw document content remain blocked.",
        ],
        warnings=[
            "Provider readiness metadata only. No OCR / document provider network call is executed.",
            "key_loaded is boolean metadata only; key values, prefixes, suffixes, and masked keys are not returned.",
        ],
    )


def list_provider_readiness() -> list[PersonalMaterialLiveProviderReadiness]:
    providers = list_live_provider_configs()["providers"]
    return [
        readiness
        for provider in providers
        if (readiness := build_provider_readiness(provider["provider_id"])) is not None
    ]


def build_provider_readiness_list() -> dict:
    providers = list_provider_readiness()
    return PersonalMaterialLiveProviderReadinessList(
        providers=providers,
        provider_count=len(providers),
        dry_run_ready_count=sum(1 for provider in providers if provider.dry_run_ready),
        key_loaded_count=sum(1 for provider in providers if provider.key_loaded),
        live_disabled_count=len(providers),
        blocked_provider_count=len(providers),
        warnings=[
            "OCR / Document live connection is dry-run ready and live-disabled by default.",
            "Responses are owner-only, metadata-only, draft-only, and source-trace required.",
        ],
    ).model_dump()

