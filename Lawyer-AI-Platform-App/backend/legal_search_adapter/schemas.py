from datetime import datetime, timezone

from pydantic import BaseModel


def utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


class LegalSearchRequest(BaseModel):
    query: str
    case_cause_code: str | None = None
    jurisdiction: str | None = "CN"
    provider: str = "mock_legal_search"
    mode: str = "mock"
    mock_only: bool = True


class LegalSearchSourceRef(BaseModel):
    provider: str
    source_id: str
    citation: str
    url: str | None = None
    quote: str
    retrieved_at: str


class LegalSearchHit(BaseModel):
    hit_id: str
    title: str
    source_type: str
    court: str
    date: str
    summary: str
    relevance_score: float
    source_ref: LegalSearchSourceRef


class LegalSearchResult(BaseModel):
    search_run_id: str
    query: str
    case_cause_code: str | None = None
    jurisdiction: str | None = None
    provider: str
    provider_mode: str
    status: str
    hits: list[LegalSearchHit]
    warnings: list[str]
    created_at: str


class LegalSearchProviderStatus(BaseModel):
    provider: str
    connected: bool
    mock_only: bool
    supports_case_law: bool
    supports_statutes: bool
    notes: str
