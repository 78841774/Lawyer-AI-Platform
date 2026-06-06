import os

from personal_intelligence_gateway.schemas import (
    PersonalIntelligenceLiveProviderConfig,
    PersonalIntelligenceLiveProviderConfigList,
)


def _env_enabled(name: str) -> bool:
    return os.environ.get(name, "").strip().lower() in {"1", "true", "yes", "on"}


def legal_live_mode_enabled() -> bool:
    return _env_enabled("LEGAL_LIVE_MODE_ENABLED")


def enterprise_live_mode_enabled() -> bool:
    return _env_enabled("ENTERPRISE_LIVE_MODE_ENABLED")


PROVIDER_DEFINITIONS = [
    {
        "provider_id": "kuaicha365_lawskills_provider",
        "display_name": "快查 365 LawSkills",
        "provider_type": "legal_search",
        "key_required": True,
        "key_env": "KUAICHA365_LAWSKILLS_API_KEY",
        "gate_env": "LEGAL_LIVE_PROVIDER_KUAICHA365_LAWSKILLS_PROVIDER_ENABLED",
        "supported_query_types": ["regulation_search", "case_law_search", "judgment_rule_search", "article_detail_preview"],
        "supports_case_search": True,
        "supports_law_search": True,
        "supports_company_profile": False,
        "supports_company_risk": False,
        "supports_citation_metadata": True,
    },
    {
        "provider_id": "pkulaw_provider_placeholder",
        "display_name": "北大法宝 Placeholder",
        "provider_type": "legal_search",
        "key_required": True,
        "key_env": "PKULAW_API_KEY",
        "gate_env": "LEGAL_LIVE_PROVIDER_PKULAW_PROVIDER_PLACEHOLDER_ENABLED",
        "supported_query_types": ["case_law_search", "regulation_search"],
        "supports_case_search": True,
        "supports_law_search": True,
        "supports_company_profile": False,
        "supports_company_risk": False,
        "supports_citation_metadata": True,
    },
    {
        "provider_id": "national_law_database_provider_placeholder",
        "display_name": "国家法律法规数据库 Placeholder",
        "provider_type": "legal_search",
        "key_required": False,
        "key_env": None,
        "gate_env": "LEGAL_LIVE_PROVIDER_NATIONAL_LAW_DATABASE_PROVIDER_PLACEHOLDER_ENABLED",
        "supported_query_types": ["regulation_search", "article_detail_preview"],
        "supports_case_search": False,
        "supports_law_search": True,
        "supports_company_profile": False,
        "supports_company_risk": False,
        "supports_citation_metadata": True,
    },
    {
        "provider_id": "tianyancha_ai_provider",
        "display_name": "天眼查 AI",
        "provider_type": "enterprise_info",
        "key_required": True,
        "key_env": "TIANYANCHA_AI_API_KEY",
        "gate_env": "ENTERPRISE_LIVE_PROVIDER_TIANYANCHA_AI_PROVIDER_ENABLED",
        "supported_query_types": ["business_profile_preview", "shareholder_officer_preview", "judicial_risk_preview"],
        "supports_case_search": False,
        "supports_law_search": False,
        "supports_company_profile": True,
        "supports_company_risk": True,
        "supports_citation_metadata": True,
    },
    {
        "provider_id": "qichacha_provider_placeholder",
        "display_name": "企查查 Placeholder",
        "provider_type": "enterprise_info",
        "key_required": True,
        "key_env": "QICHACHA_API_KEY",
        "gate_env": "ENTERPRISE_LIVE_PROVIDER_QICHACHA_PROVIDER_PLACEHOLDER_ENABLED",
        "supported_query_types": ["business_profile_preview", "judicial_risk_preview"],
        "supports_case_search": False,
        "supports_law_search": False,
        "supports_company_profile": True,
        "supports_company_risk": True,
        "supports_citation_metadata": True,
    },
]


def list_live_provider_configs() -> dict:
    providers = [_build_provider(definition) for definition in PROVIDER_DEFINITIONS]
    return PersonalIntelligenceLiveProviderConfigList(
        providers=providers,
        provider_count=len(providers),
        live_provider_count=sum(1 for provider in providers if provider.live_enabled),
        key_loaded_count=sum(1 for provider in providers if provider.key_loaded),
        warnings=[
            "Legal / Enterprise providers are disabled by default and provider-gated.",
            "key_loaded is boolean metadata only; API key values and env var values are never returned.",
        ],
    ).model_dump()


def get_live_provider_config(provider_id: str) -> PersonalIntelligenceLiveProviderConfig | None:
    for definition in PROVIDER_DEFINITIONS:
        if definition["provider_id"] == provider_id:
            return _build_provider(definition)
    return None


def _build_provider(definition: dict) -> PersonalIntelligenceLiveProviderConfig:
    key_env = definition.get("key_env")
    key_loaded = bool(key_env and os.environ.get(str(key_env)))
    key_source = "env" if key_loaded else "unavailable"
    if not definition["key_required"]:
        key_loaded = False
        key_source = "not_required"
    return PersonalIntelligenceLiveProviderConfig(
        provider_id=definition["provider_id"],
        display_name=definition["display_name"],
        provider_type=definition["provider_type"],
        live_supported=True,
        live_enabled=_env_enabled(definition["gate_env"]),
        key_required=definition["key_required"],
        key_loaded=key_loaded,
        key_source=key_source,
        supported_query_types=definition["supported_query_types"],
        max_query_size=500,
        supports_case_search=definition["supports_case_search"],
        supports_law_search=definition["supports_law_search"],
        supports_company_profile=definition["supports_company_profile"],
        supports_company_risk=definition["supports_company_risk"],
        supports_citation_metadata=definition["supports_citation_metadata"],
        timeout_seconds=45,
        safety_notes=[
            "Live mode is disabled by default.",
            "Raw provider result content is not returned by the v7.14 gateway.",
            "Candidates require lawyer review and source trace before downstream use.",
        ],
    )
