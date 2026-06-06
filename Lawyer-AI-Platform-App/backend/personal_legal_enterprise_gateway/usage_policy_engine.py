from personal_legal_enterprise_gateway.provider_registry import build_provider
from personal_legal_enterprise_gateway.schemas import UsagePolicy


def build_usage_policy(provider_id: str) -> UsagePolicy | None:
    provider = build_provider(provider_id)
    if provider is None:
        return None
    return UsagePolicy(
        provider_id=provider.provider_id,
        estimated_query_count=1,
        estimated_call_count=1,
        estimated_result_count=5 if provider.provider_category == "legal" else 3,
        warnings=["Usage and cost values are dry-run metadata only; no billable call is executed."],
    )

