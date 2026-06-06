import os

from personal_material_runtime.schemas import PersonalMaterialLiveProviderConfig, PersonalMaterialLiveProviderConfigList


def _env_enabled(name: str) -> bool:
    return os.environ.get(name, "").strip().lower() in {"1", "true", "yes", "on"}


def ocr_live_mode_enabled() -> bool:
    return _env_enabled("OCR_LIVE_MODE_ENABLED")


def document_live_mode_enabled() -> bool:
    return _env_enabled("DOCUMENT_LIVE_MODE_ENABLED")


PROVIDER_DEFINITIONS = [
    {
        "provider_id": "paddleocr",
        "display_name": "PaddleOCR",
        "provider_type": "ocr",
        "live_supported": True,
        "key_required": False,
        "supported_file_types": ["png", "jpg", "jpeg", "pdf", "tiff"],
        "max_file_size_mb": 25,
        "supports_page_range": True,
        "supports_bbox": True,
        "supports_table_extraction": True,
        "supports_layout_extraction": True,
        "timeout_seconds": 45,
        "gate_env": "OCR_LIVE_PROVIDER_PADDLEOCR_ENABLED",
        "key_env": None,
        "safety_notes": [
            "Live OCR is disabled by default.",
            "Raw OCR text is not returned by the v7.13 gateway.",
            "OCR metadata must go through review before downstream use.",
        ],
    },
    {
        "provider_id": "mineru",
        "display_name": "MinerU Document Parser",
        "provider_type": "document_parser",
        "live_supported": True,
        "key_required": False,
        "supported_file_types": ["pdf", "docx", "pptx", "xlsx"],
        "max_file_size_mb": 50,
        "supports_page_range": True,
        "supports_bbox": True,
        "supports_table_extraction": True,
        "supports_layout_extraction": True,
        "timeout_seconds": 60,
        "gate_env": "DOCUMENT_LIVE_PROVIDER_MINERU_ENABLED",
        "key_env": None,
        "safety_notes": [
            "Document parser live mode is disabled by default.",
            "Document text is not exposed through live metadata responses.",
            "Parser output does not enter AI prompts automatically.",
        ],
    },
    {
        "provider_id": "docling",
        "display_name": "Docling Document Parser",
        "provider_type": "document_parser",
        "live_supported": True,
        "key_required": False,
        "supported_file_types": ["pdf", "docx", "html", "md"],
        "max_file_size_mb": 50,
        "supports_page_range": True,
        "supports_bbox": True,
        "supports_table_extraction": True,
        "supports_layout_extraction": True,
        "timeout_seconds": 60,
        "gate_env": "DOCUMENT_LIVE_PROVIDER_DOCLING_ENABLED",
        "key_env": None,
        "safety_notes": [
            "Docling live parser adapter is not implemented in v7.13.",
            "Only safe metadata preview is returned.",
            "Raw document content remains blocked by default.",
        ],
    },
    {
        "provider_id": "local_document_parser_placeholder",
        "display_name": "Local Document Parser Placeholder",
        "provider_type": "document_parser",
        "live_supported": False,
        "key_required": False,
        "supported_file_types": ["pdf", "docx", "txt"],
        "max_file_size_mb": 10,
        "supports_page_range": False,
        "supports_bbox": False,
        "supports_table_extraction": False,
        "supports_layout_extraction": False,
        "timeout_seconds": 10,
        "gate_env": "DOCUMENT_LIVE_PROVIDER_LOCAL_DOCUMENT_PARSER_PLACEHOLDER_ENABLED",
        "key_env": None,
        "safety_notes": [
            "Placeholder provider is metadata-only.",
            "It never reads local files or calls an external service.",
            "Use for dry-run readiness checks only.",
        ],
    },
]


def list_live_provider_configs() -> dict:
    providers = [_build_provider(definition) for definition in PROVIDER_DEFINITIONS]
    return PersonalMaterialLiveProviderConfigList(
        providers=providers,
        provider_count=len(providers),
        live_provider_count=sum(1 for provider in providers if provider.live_enabled),
        key_loaded_count=sum(1 for provider in providers if provider.key_loaded),
        warnings=[
            "OCR / Document providers are disabled by default and provider-gated.",
            "key_loaded is boolean metadata only; API key values are never returned.",
        ],
    ).model_dump()


def get_live_provider_config(provider_id: str) -> PersonalMaterialLiveProviderConfig | None:
    for definition in PROVIDER_DEFINITIONS:
        if definition["provider_id"] == provider_id:
            return _build_provider(definition)
    return None


def _build_provider(definition: dict) -> PersonalMaterialLiveProviderConfig:
    key_env = definition.get("key_env")
    key_loaded = str(key_env) in os.environ if key_env else False
    key_source = "env" if key_loaded else "unavailable"
    if not definition["key_required"]:
        key_source = "not_required"
        key_loaded = False
    return PersonalMaterialLiveProviderConfig(
        provider_id=definition["provider_id"],
        display_name=definition["display_name"],
        provider_type=definition["provider_type"],
        live_supported=definition["live_supported"],
        live_enabled=_env_enabled(definition["gate_env"]),
        key_required=definition["key_required"],
        key_loaded=key_loaded,
        key_source=key_source,
        supported_file_types=definition["supported_file_types"],
        max_file_size_mb=definition["max_file_size_mb"],
        supports_page_range=definition["supports_page_range"],
        supports_bbox=definition["supports_bbox"],
        supports_table_extraction=definition["supports_table_extraction"],
        supports_layout_extraction=definition["supports_layout_extraction"],
        timeout_seconds=definition["timeout_seconds"],
        safety_notes=definition["safety_notes"],
    )
