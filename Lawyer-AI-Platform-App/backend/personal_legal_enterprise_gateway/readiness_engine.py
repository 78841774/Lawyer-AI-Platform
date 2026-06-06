from personal_legal_enterprise_gateway.provider_registry import list_provider_metadata
from personal_legal_enterprise_gateway.schemas import LegalEnterpriseStatus


def build_status() -> dict:
    providers = list_provider_metadata()
    legal_count = sum(1 for provider in providers if provider.provider_category == "legal")
    enterprise_count = sum(1 for provider in providers if provider.provider_category == "enterprise")
    return LegalEnterpriseStatus(
        provider_count=len(providers),
        legal_provider_count=legal_count,
        enterprise_provider_count=enterprise_count,
        warnings=["v7.29 Legal / Enterprise API connection is dry-run metadata only and live-disabled by default."],
    ).model_dump()

