from personal_provider_readiness.provider_registry import get_provider
from personal_provider_readiness.schemas import UsagePolicy


def build_usage_policy(provider_id: str) -> UsagePolicy | None:
    provider = get_provider(provider_id)
    if provider is None:
        return None
    estimated_token_count = 1200 if provider.provider_category == "ai" else 0
    estimated_page_count = 3 if provider.provider_category in {"ocr", "document"} else 0
    estimated_document_count = 1 if provider.provider_category in {"ocr", "document"} else 0
    return UsagePolicy(
        provider_id=provider.provider_id,
        usage_meter_enabled=False,
        estimated_token_count=estimated_token_count,
        estimated_page_count=estimated_page_count,
        estimated_document_count=estimated_document_count,
        estimated_call_count=1,
        estimated_cost_available=False,
        actual_cost_recorded=False,
        billable_call_executed=False,
        usage_recorded_as_metadata_only=True,
        warnings=["Usage and cost values are dry-run estimates only; no billable call is executed."],
    )

