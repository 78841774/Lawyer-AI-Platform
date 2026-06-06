from personal_ai_gateway.schemas import PersonalAILiveRunRequest


FORBIDDEN_PURPOSES = {
    "final_legal_opinion",
    "final_report",
    "external_delivery",
    "auto_send_client",
}


def validate_prompt_boundary(request: PersonalAILiveRunRequest) -> list[str]:
    blocked: list[str] = []
    if request.prompt_purpose in FORBIDDEN_PURPOSES:
        blocked.append("prompt purpose is forbidden for v7.12 live gateway")
    if request.raw_content_included:
        blocked.append("raw content must not be included in live prompt boundary")
    if request.final_legal_opinion_requested:
        blocked.append("final legal opinion must not be requested")
    if request.final_report_requested:
        blocked.append("final report must not be requested")
    return blocked
