from legal_search_adapter.schemas import LegalSearchProviderStatus, LegalSearchRequest, LegalSearchResult


class LegalSearchProvider:
    def get_status(self) -> LegalSearchProviderStatus:
        raise NotImplementedError

    def search(self, request: LegalSearchRequest) -> LegalSearchResult:
        raise NotImplementedError
