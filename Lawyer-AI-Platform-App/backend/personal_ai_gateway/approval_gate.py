from personal_ai_gateway.schemas import PersonalAIMockRunRequest, PersonalAIPromptRenderPreviewRequest


def validate_preview_confirmations(request: PersonalAIPromptRenderPreviewRequest) -> list[str]:
    missing: list[str] = []
    if not request.manual_review_confirmed:
        missing.append("manual_review_confirmed is required")
    if not request.mock_data_only_confirmation:
        missing.append("mock_data_only_confirmation is required")
    if not request.no_raw_content_confirmation:
        missing.append("no_raw_content_confirmation is required")
    return missing


def validate_mock_run_confirmations(request: PersonalAIMockRunRequest) -> list[str]:
    required_flags = {
        "manual_approval_confirmed": request.manual_approval_confirmed,
        "lawyer_review_required_confirmation": request.lawyer_review_required_confirmation,
        "draft_only_confirmation": request.draft_only_confirmation,
        "source_trace_required_confirmation": request.source_trace_required_confirmation,
        "no_final_legal_opinion_confirmation": request.no_final_legal_opinion_confirmation,
        "no_final_report_generation_confirmation": request.no_final_report_generation_confirmation,
    }
    return [f"{flag} is required" for flag, confirmed in required_flags.items() if not confirmed]
