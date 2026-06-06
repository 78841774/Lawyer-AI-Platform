from personal_legal_enterprise_gateway.provider_config import key_loaded_for, key_source_for
from personal_legal_enterprise_gateway.schemas import LegalEnterpriseCategorySummary, LegalEnterpriseCategorySummaryList, LegalEnterpriseProvider, LegalEnterpriseProviderList


PROVIDER_DEFINITIONS = [
    ("kuaicha_365_lawskills_placeholder", "快查 365 LawSkills Placeholder", "legal", "legal_question_search", ["KUAICHA365_LAWSKILLS_API_KEY"], True),
    ("national_law_database_placeholder", "国家法律法规数据库 Placeholder", "legal", "statute_search", [], False),
    ("legal_search_placeholder", "Legal Search Placeholder", "legal", "legal_question_search", ["LEGAL_SEARCH_API_KEY"], True),
    ("court_case_search_placeholder", "Court Case Search Placeholder", "legal", "case_search", ["COURT_CASE_SEARCH_API_KEY"], True),
    ("statute_search_placeholder", "Statute Search Placeholder", "legal", "statute_search", [], False),
    ("tianyancha_ai_placeholder", "天眼查 AI Placeholder", "enterprise", "company_registry", ["TIANYANCHA_API_KEY", "TIANYANCHA_AI_API_KEY"], True),
    ("qichacha_placeholder", "企查查 Placeholder", "enterprise", "credit_info", ["QICHACHA_API_KEY"], True),
    ("enterprise_registry_placeholder", "Enterprise Registry Placeholder", "enterprise", "company_registry", [], False),
    ("company_credit_search_placeholder", "Company Credit Search Placeholder", "enterprise", "credit_info", ["COMPANY_CREDIT_SEARCH_API_KEY"], True),
]


def build_provider(provider_id: str) -> LegalEnterpriseProvider | None:
    for current_id, name, category, subtype, env_names, requires_key in PROVIDER_DEFINITIONS:
        if current_id != provider_id:
            continue
        return LegalEnterpriseProvider(
            provider_id=current_id,
            provider_name=name,
            provider_category=category,
            provider_subtype=subtype,
            requires_api_key=requires_key,
            key_env_names=env_names,
            key_loaded=key_loaded_for(env_names) if requires_key else False,
            key_source=key_source_for(requires_key, env_names),
            external_transfer_required=requires_key,
            usage_meter_supported=True,
            cost_metadata_supported=True,
            status="registered_dry_run_ready_live_blocked",
            warnings=[
                "Provider metadata only. No legal or enterprise provider network call is executed.",
                "key_loaded is boolean metadata only; key values are not returned.",
            ],
        )
    return None


def list_provider_metadata() -> list[LegalEnterpriseProvider]:
    return [provider for provider_id, *_ in PROVIDER_DEFINITIONS if (provider := build_provider(provider_id)) is not None]


def build_provider_list(providers: list[LegalEnterpriseProvider] | None = None) -> dict:
    safe_providers = providers or list_provider_metadata()
    return LegalEnterpriseProviderList(
        providers=safe_providers,
        provider_count=len(safe_providers),
        key_loaded_count=sum(1 for provider in safe_providers if provider.key_loaded),
        dry_run_ready_count=sum(1 for provider in safe_providers if provider.dry_run_supported),
        live_disabled_count=len(safe_providers),
        blocked_provider_count=len(safe_providers),
        warnings=["Legal / Enterprise providers are dry-run ready and live-disabled by default."],
    ).model_dump()


def build_categories() -> dict:
    providers = list_provider_metadata()
    categories = []
    for category in sorted({provider.provider_category for provider in providers}):
        category_providers = [provider for provider in providers if provider.provider_category == category]
        categories.append(
            LegalEnterpriseCategorySummary(
                category=category,
                provider_count=len(category_providers),
                key_loaded_count=sum(1 for provider in category_providers if provider.key_loaded),
                dry_run_ready_count=sum(1 for provider in category_providers if provider.dry_run_supported),
                live_disabled_count=len(category_providers),
                blocked_provider_count=len(category_providers),
            )
        )
    return LegalEnterpriseCategorySummaryList(categories=categories, category_count=len(categories)).model_dump()

