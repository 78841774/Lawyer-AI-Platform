from fastapi import APIRouter

from legal_search_adapter.mock_provider import MockLegalSearchProvider
from legal_search_adapter.schemas import LegalSearchProviderStatus, LegalSearchRequest, LegalSearchResult

router = APIRouter(prefix="/legal-search", tags=["legal-search-adapter"])
provider = MockLegalSearchProvider()


@router.get("/status")
def get_legal_search_status() -> LegalSearchProviderStatus:
    return provider.get_status()


@router.post("/mock-search")
def mock_legal_search(payload: LegalSearchRequest) -> LegalSearchResult:
    return provider.search(payload)
