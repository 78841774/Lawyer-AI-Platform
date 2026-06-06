from personal_intelligence_gateway.provider_config import get_live_provider_config
from personal_intelligence_gateway.query_boundary import redacted_query_text
from personal_intelligence_gateway.schemas import PersonalIntelligenceLiveMetadataPreview, PersonalIntelligenceLiveRunRequest


def build_live_metadata_preview(request: PersonalIntelligenceLiveRunRequest, *, run_type: str, query_id: str) -> PersonalIntelligenceLiveMetadataPreview:
    provider = get_live_provider_config(request.provider_id)
    provider_type = provider.provider_type if provider else ("enterprise_info" if run_type == "enterprise" else "legal_search")
    return PersonalIntelligenceLiveMetadataPreview(
        query_id=query_id,
        query_text_redacted=redacted_query_text(request.query_text),
        query_type=request.query_type,
        provider_id=request.provider_id,
        provider_type=provider_type,
        jurisdiction=request.jurisdiction,
        result_count_estimate=3 if run_type == "legal" else 2,
        citation_candidate_count=2 if run_type == "legal" else 0,
        enterprise_candidate_count=2 if run_type == "enterprise" else 0,
        confidence_summary="metadata_candidate_only",
    )
