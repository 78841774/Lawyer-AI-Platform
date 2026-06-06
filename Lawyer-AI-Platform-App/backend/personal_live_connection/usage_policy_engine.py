from personal_live_connection.provider_registry import build_provider
from personal_live_connection.schemas import LiveConnectionUsagePolicy


def build_usage_policy(provider_id: str) -> LiveConnectionUsagePolicy | None:
    provider = build_provider(provider_id)
    if provider is None:
        return None
    return LiveConnectionUsagePolicy(
        provider_id=provider.provider_id,
        estimated_token_count=1600 if provider.provider_category == "ai" else 0,
        estimated_page_count=4 if provider.provider_category in {"ocr", "document"} else 0,
        estimated_query_count=1 if provider.provider_category in {"legal", "enterprise"} else 0,
        estimated_call_count=1,
        warnings=["Usage and cost are dry-run metadata only; no billable provider call is executed."],
    )

