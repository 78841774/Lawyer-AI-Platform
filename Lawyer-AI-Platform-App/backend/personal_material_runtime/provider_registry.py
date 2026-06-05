from personal_material_runtime.schemas import PersonalMaterialProvider, PersonalMaterialProviderList


PROVIDER_DEFINITIONS = [
    {
        "provider_id": "mineru_file_parser_provider",
        "label": "MinerU File Parser",
        "category": "file_parser",
        "next_action": "evaluate_local_mineru_runtime",
    },
    {
        "provider_id": "docling_file_parser_provider",
        "label": "Docling File Parser",
        "category": "file_parser",
        "next_action": "evaluate_local_docling_runtime",
    },
    {
        "provider_id": "paddleocr_provider",
        "label": "PaddleOCR / Baidu AI Studio",
        "category": "ocr",
        "next_action": "configure_controlled_paddleocr_runtime",
    },
]


def list_providers() -> dict:
    providers = [
        PersonalMaterialProvider(
            warnings=["Provider metadata only. v7.2 does not read secrets or execute live OCR/parser calls."],
            **definition,
        )
        for definition in PROVIDER_DEFINITIONS
    ]
    return PersonalMaterialProviderList(
        providers=providers,
        provider_count=len(providers),
        configured_provider_count=sum(1 for provider in providers if provider.configured),
        live_provider_count=sum(1 for provider in providers if provider.live_enabled),
        warnings=["Material/OCR providers are registered as mock-first placeholders. Provider secrets are never visible."],
    ).model_dump()


def get_provider(provider_id: str) -> PersonalMaterialProvider | None:
    for provider in list_providers()["providers"]:
        if provider.get("provider_id") == provider_id:
            return PersonalMaterialProvider(**provider)
    return None


def validate_provider(provider_id: str, category: str) -> list[str]:
    provider = get_provider(provider_id)
    if provider is None:
        return ["provider_id is not registered"]
    if provider.category != category:
        return [f"provider must be category {category}"]
    if not provider.mock_supported:
        return ["provider does not support mock mode"]
    if provider.live_enabled:
        return ["provider live mode must remain disabled in v7.2"]
    return []
