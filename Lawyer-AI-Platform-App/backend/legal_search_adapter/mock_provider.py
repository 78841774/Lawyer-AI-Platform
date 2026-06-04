from legal_search_adapter.provider import LegalSearchProvider
from legal_search_adapter.schemas import (
    LegalSearchHit,
    LegalSearchProviderStatus,
    LegalSearchRequest,
    LegalSearchResult,
    LegalSearchSourceRef,
    utc_now
)


class MockLegalSearchProvider(LegalSearchProvider):
    def get_status(self) -> LegalSearchProviderStatus:
        return LegalSearchProviderStatus(
            provider="mock_legal_search",
            connected=False,
            mock_only=True,
            supports_case_law=True,
            supports_statutes=True,
            notes="Legal Search adapter prepared. Real legal database not connected."
        )

    def search(self, request: LegalSearchRequest) -> LegalSearchResult:
        retrieved_at = utc_now()
        source_ref = LegalSearchSourceRef(
            provider="mock_legal_search",
            source_id="mock_case_law_payment_dispute_001",
            citation="Mock Citation",
            url=None,
            quote="Mock quote only.",
            retrieved_at=retrieved_at
        )
        hit = LegalSearchHit(
            hit_id="mock_hit_payment_dispute_001",
            title="Mock Case Law Result for Payment Dispute",
            source_type="mock_case_law",
            court="Mock Court",
            date="2026-06-04",
            summary="Mock legal search result. No external legal database was queried.",
            relevance_score=0.0,
            source_ref=source_ref
        )
        return LegalSearchResult(
            search_run_id="legal_search_mock_payment_dispute_001",
            query=request.query,
            case_cause_code=request.case_cause_code,
            jurisdiction=request.jurisdiction,
            provider="mock_legal_search",
            provider_mode="mock",
            status="completed_mock",
            hits=[hit],
            warnings=[
                "Mock legal search only.",
                "No external legal database queried.",
                "No real case law retrieved."
            ],
            created_at=retrieved_at
        )
