from personal_ai_gateway.schemas import PersonalAIRunRecord, PersonalAITokenUsage, PersonalAITokenUsageSummary


def estimate_token_usage(template_id: str, provider_id: str) -> PersonalAITokenUsage:
    estimated_input_tokens = max(12, len(template_id) + len(provider_id))
    estimated_output_tokens = 96
    return PersonalAITokenUsage(
        estimated_input_tokens=estimated_input_tokens,
        estimated_output_tokens=estimated_output_tokens,
        estimated_total_tokens=estimated_input_tokens + estimated_output_tokens,
        actual_input_tokens=None,
        actual_output_tokens=None,
        actual_total_tokens=None,
        live_usage_available=False,
    )


def summarize_token_usage(runs: list[PersonalAIRunRecord]) -> dict:
    provider_usage: dict[str, int] = {}
    template_usage: dict[str, int] = {}
    estimated_total = 0

    for run in runs:
        total = run.token_usage.estimated_total_tokens
        estimated_total += total
        provider_usage[run.provider_id] = provider_usage.get(run.provider_id, 0) + total
        template_usage[run.template_id] = template_usage.get(run.template_id, 0) + total

    return PersonalAITokenUsageSummary(
        run_count=len(runs),
        estimated_total_tokens=estimated_total,
        actual_total_tokens=None,
        live_usage_available=False,
        provider_usage_breakdown=provider_usage,
        template_usage_breakdown=template_usage,
        warnings=["Actual token usage is unavailable because v7.1 does not execute live provider calls."],
    ).model_dump()
