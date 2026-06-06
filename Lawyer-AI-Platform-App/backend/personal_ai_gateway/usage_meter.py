from personal_ai_gateway.schemas import PersonalAILiveRunRequest


def estimate_live_usage(request: PersonalAILiveRunRequest) -> dict[str, int | None]:
    prompt_size = len(request.prompt_template_id) + len(request.prompt_purpose) + len(request.case_id or "")
    estimated_input_tokens = max(16, prompt_size // 4)
    return {
        "estimated_input_tokens": estimated_input_tokens,
        "estimated_output_tokens": 0 if request.dry_run else None,
        "estimated_total_tokens": estimated_input_tokens,
        "actual_input_tokens": None,
        "actual_output_tokens": None,
        "actual_total_tokens": None,
    }
