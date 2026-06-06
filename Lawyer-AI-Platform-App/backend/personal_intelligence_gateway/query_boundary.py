from personal_intelligence_gateway.schemas import PersonalIntelligenceLiveRunRequest


LEGAL_QUERY_TYPES = {"regulation_search", "case_law_search", "judgment_rule_search", "article_detail_preview", "case_detail_preview"}
ENTERPRISE_QUERY_TYPES = {
    "business_profile_preview",
    "shareholder_officer_preview",
    "operating_status_preview",
    "judicial_risk_preview",
    "enforcement_signal_preview",
}


def validate_legal_query_boundary(request: PersonalIntelligenceLiveRunRequest) -> list[str]:
    blocked: list[str] = []
    if not request.query_text.strip():
        blocked.append("query_text is required")
    if len(request.query_text) > 500:
        blocked.append("query_text exceeds metadata preview limit")
    if request.query_type not in LEGAL_QUERY_TYPES:
        blocked.append("query_type is not supported for legal search")
    return blocked


def validate_enterprise_query_boundary(request: PersonalIntelligenceLiveRunRequest) -> list[str]:
    blocked: list[str] = []
    if not request.query_text.strip():
        blocked.append("query_text is required")
    if len(request.query_text) > 500:
        blocked.append("query_text exceeds metadata preview limit")
    if request.query_type not in ENTERPRISE_QUERY_TYPES:
        blocked.append("query_type is not supported for enterprise query")
    return blocked


def redacted_query_text(query_text: str) -> str:
    value = " ".join(query_text.strip().split())
    if not value:
        return "redacted_empty_query"
    if len(value) <= 24:
        return f"{value[:8]}...redacted"
    return f"{value[:12]}...{value[-4:]} (redacted)"
