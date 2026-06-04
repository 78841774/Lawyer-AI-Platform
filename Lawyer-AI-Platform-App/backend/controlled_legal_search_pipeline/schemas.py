from datetime import datetime, timezone
from typing import Any

from pydantic import BaseModel, Field


def utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


class ControlledLegalSearchStatus(BaseModel):
    enabled: bool = True
    mode: str = "local_only_controlled_legal_search"
    production_enabled: bool = False
    legal_search_live_enabled: bool = False
    legal_search_live_default: bool = False
    mock_legal_search_enabled: bool = True
    requires_explicit_legal_search_confirmation: bool = True
    requires_manual_review: bool = True
    query_redaction_enabled: bool = True
    source_trace_enabled: bool = True
    citation_resolver_enabled: bool = True
    store_raw_query_in_git: bool = False
    store_raw_legal_search_results_in_git: bool = False
    store_redacted_search_preview_in_git: bool = False
    runtime_storage_enabled: bool = True
    runtime_storage_path: str = "storage/runtime/controlled_legal_search_previews"
    final_legal_opinion_enabled: bool = False
    warnings: list[str] = Field(default_factory=list)


class ControlledLegalSearchPreviewRequest(BaseModel):
    case_id: str = "case_v45_demo_001"
    workspace_id: str = "workspace_demo_001"
    query_text: str = ""
    query_text_redacted: str = ""
    case_cause_code: str = "payment_dispute"
    jurisdiction: str = "CN"
    explicit_legal_search_confirmation: bool = False
    manual_review_confirmed: bool = False
    legal_search_mode: str = "mock"
    provider_mode: str = "controlled_local"
    preview_only: bool = True


class ControlledLegalSearchGuardResult(BaseModel):
    guard_name: str
    allowed: bool
    status: str
    warnings: list[str] = Field(default_factory=list)
    metadata: dict[str, Any] = Field(default_factory=dict)


class ControlledLegalCitation(BaseModel):
    citation_id: str
    title: str
    citation_type: str
    jurisdiction: str
    source_name: str
    source_ref_id: str
    relevance: str
    mock_only: bool = True
    warnings: list[str] = Field(default_factory=list)


class ControlledLegalCitationSourceRef(BaseModel):
    source_ref_id: str
    source_type: str = "controlled_legal_search"
    citation_id: str
    title: str
    quote: str = "Mock legal citation placeholder. No real legal database was called."
    provider: str = "controlled_legal_search"
    provider_mode: str = "mock"
    mock_or_redacted_only: bool = True


class ControlledLegalSearchPreviewResult(BaseModel):
    search_preview_id: str
    case_id: str
    workspace_id: str
    query_text_redacted: str
    case_cause_code: str
    jurisdiction: str
    legal_search_called: bool = False
    real_legal_search_called: bool = False
    mock_legal_search_used: bool = False
    raw_query_stored: bool = False
    raw_results_stored: bool = False
    redacted_search_preview_created: bool = False
    redacted_search_preview: str = ""
    redacted_search_preview_storage_path: str = "storage/runtime/controlled_legal_search_previews"
    citations: list[dict[str, Any]] = Field(default_factory=list)
    source_refs: list[dict[str, Any]] = Field(default_factory=list)
    guard_results: list[dict[str, Any]] = Field(default_factory=list)
    audit_log_id: str
    allowed_to_continue: bool = False
    warnings: list[str] = Field(default_factory=list)
    created_at: str


class ControlledLegalSearchPreviewRecord(BaseModel):
    search_preview_id: str
    case_id: str = ""
    workspace_id: str = ""
    query_text_redacted: str = ""
    case_cause_code: str = ""
    jurisdiction: str = "CN"
    redacted_search_preview: str
    citations: list[dict[str, Any]] = Field(default_factory=list)
    source_refs: list[dict[str, Any]] = Field(default_factory=list)
    warnings: list[str] = Field(default_factory=list)
    created_at: str


class ControlledLegalCitationResolutionRequest(BaseModel):
    citation_id: str = "mock_citation_001"
    search_preview_id: str = "search_preview_demo_001"
    manual_review_confirmed: bool = False
    legal_search_mode: str = "mock"
    provider_mode: str = "controlled_local"


class ControlledLegalCitationResolutionResult(BaseModel):
    citation_id: str
    search_preview_id: str
    resolved: bool
    real_legal_database_called: bool = False
    mock_resolution_used: bool = True
    source_ref: dict[str, Any]
    warnings: list[str] = Field(default_factory=list)
    audit_log_id: str
    created_at: str


class RuntimeLegalSearchStorageResult(BaseModel):
    stored: bool
    storage_path: str
    raw_query_stored: bool = False
    raw_results_stored: bool = False
    redacted_search_preview_stored: bool = False
    warnings: list[str] = Field(default_factory=list)
