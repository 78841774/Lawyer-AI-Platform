from personal_provider_readiness.usage_policy_engine import build_usage_policy


def build_cost_metadata(provider_id: str) -> dict | None:
    usage = build_usage_policy(provider_id)
    return usage.model_dump() if usage else None

