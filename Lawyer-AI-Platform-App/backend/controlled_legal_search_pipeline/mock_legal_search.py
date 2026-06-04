from typing import Any
from uuid import uuid4

from controlled_legal_search_pipeline.audit import append_controlled_legal_search_audit_log
from controlled_legal_search_pipeline.citation_trace import (
    build_legal_search_source_refs,
    build_mock_citation_resolution_source_ref,
)
from controlled_legal_search_pipeline.guards import (
    check_legal_search_provider_gate,
    check_manual_review_gate,
    redact_legal_query,
    run_all_controlled_legal_search_guards,
)
from controlled_legal_search_pipeline.runtime_storage import load_redacted_legal_search_preview, store_redacted_legal_search_preview
from controlled_legal_search_pipeline.schemas import (
    ControlledLegalCitation,
    ControlledLegalCitationResolutionRequest,
    ControlledLegalCitationResolutionResult,
    ControlledLegalSearchPreviewRecord,
    ControlledLegalSearchPreviewRequest,
    ControlledLegalSearchPreviewResult,
    ControlledLegalSearchStatus,
    utc_now,
)


def get_controlled_legal_search_status() -> dict[str, Any]:
    return ControlledLegalSearchStatus(
        warnings=[
            "v4.5 is local-only controlled legal search citation preview.",
            "Mock legal search is enabled by default.",
            "No real legal database, LLM, OCR, or DeepSeek live provider is called.",
            "Manual lawyer review and explicit legal search confirmation are required.",
        ]
    ).model_dump()


def run_mock_legal_search_preview(request: ControlledLegalSearchPreviewRequest) -> dict[str, Any]:
    created_at = utc_now()
    search_preview_id = f"controlled_legal_search_preview_{uuid4().hex[:12]}"
    audit_log_id = f"controlled_legal_search_audit_{uuid4().hex[:12]}"
    guard_results = run_all_controlled_legal_search_guards(request)
    allowed_to_continue = all(bool(result.get("allowed")) for result in guard_results)
    warnings = _collect_warnings(guard_results)
    query_text_redacted = request.query_text_redacted.strip() or redact_legal_query(request.query_text)

    if not request.preview_only:
        allowed_to_continue = False
        warnings.append("preview_only must remain true for v4.5 controlled legal search preview.")

    if not allowed_to_continue:
        append_controlled_legal_search_audit_log(_audit_event(audit_log_id, request, search_preview_id, None, "blocked_by_controlled_legal_search_guard", warnings, created_at))
        return ControlledLegalSearchPreviewResult(
            search_preview_id=search_preview_id,
            case_id=request.case_id,
            workspace_id=request.workspace_id,
            query_text_redacted=query_text_redacted,
            case_cause_code=request.case_cause_code,
            jurisdiction=request.jurisdiction,
            legal_search_called=False,
            real_legal_search_called=False,
            mock_legal_search_used=False,
            raw_query_stored=False,
            raw_results_stored=False,
            redacted_search_preview_created=False,
            redacted_search_preview="",
            citations=[],
            source_refs=[],
            guard_results=guard_results,
            audit_log_id=audit_log_id,
            allowed_to_continue=False,
            warnings=list(dict.fromkeys(warnings)),
            created_at=created_at,
        ).model_dump()

    citations = _mock_citations(request.jurisdiction)
    source_refs = build_legal_search_source_refs(search_preview_id, citations)
    redacted_search_preview = _build_redacted_search_preview(query_text_redacted, citations)
    storage = store_redacted_legal_search_preview(
        search_preview_id,
        {"redacted_search_preview": redacted_search_preview, "citations": citations, "source_refs": source_refs},
    )
    warnings.extend(storage.get("warnings", []))
    append_controlled_legal_search_audit_log(_audit_event(audit_log_id, request, search_preview_id, None, "redacted_search_preview_created", warnings, created_at))
    return ControlledLegalSearchPreviewResult(
        search_preview_id=search_preview_id,
        case_id=request.case_id,
        workspace_id=request.workspace_id,
        query_text_redacted=query_text_redacted,
        case_cause_code=request.case_cause_code,
        jurisdiction=request.jurisdiction,
        legal_search_called=True,
        real_legal_search_called=False,
        mock_legal_search_used=True,
        raw_query_stored=False,
        raw_results_stored=False,
        redacted_search_preview_created=True,
        redacted_search_preview=redacted_search_preview,
        redacted_search_preview_storage_path=storage["storage_path"],
        citations=citations,
        source_refs=source_refs,
        guard_results=guard_results,
        audit_log_id=audit_log_id,
        allowed_to_continue=True,
        warnings=list(dict.fromkeys(warnings)),
        created_at=created_at,
    ).model_dump()


def get_controlled_legal_search_preview(search_preview_id: str) -> dict[str, Any]:
    loaded = load_redacted_legal_search_preview(search_preview_id)
    return ControlledLegalSearchPreviewRecord(
        search_preview_id=str(loaded.get("search_preview_id", search_preview_id)),
        redacted_search_preview=str(loaded.get("redacted_search_preview", "")),
        citations=list(loaded.get("citations", [])),
        source_refs=list(loaded.get("source_refs", [])),
        warnings=list(loaded.get("warnings", [])),
        created_at=str(loaded.get("created_at", utc_now())),
    ).model_dump()


def resolve_mock_citation(request: ControlledLegalCitationResolutionRequest) -> dict[str, Any]:
    created_at = utc_now()
    audit_log_id = f"controlled_legal_search_audit_{uuid4().hex[:12]}"
    guard_results = [check_manual_review_gate(request), check_legal_search_provider_gate(request)]
    allowed = all(bool(result.get("allowed")) for result in guard_results)
    warnings = ["Mock citation resolution only.", "No real legal database was called."]
    for result in guard_results:
        warnings.extend(str(item) for item in result.get("warnings", []))
    source_ref = build_mock_citation_resolution_source_ref(request.citation_id, request.search_preview_id)
    append_controlled_legal_search_audit_log(
        {
            "audit_log_id": audit_log_id,
            "event_type": "controlled_legal_citation_resolution",
            "case_id": "",
            "workspace_id": "",
            "search_preview_id": request.search_preview_id,
            "citation_id": request.citation_id,
            "result": "mock_resolution" if allowed else "blocked_by_controlled_legal_search_guard",
            "warnings": warnings,
            "created_at": created_at,
        }
    )
    return ControlledLegalCitationResolutionResult(
        citation_id=request.citation_id,
        search_preview_id=request.search_preview_id,
        resolved=allowed,
        real_legal_database_called=False,
        mock_resolution_used=True,
        source_ref=source_ref,
        warnings=list(dict.fromkeys(warnings)),
        audit_log_id=audit_log_id,
        created_at=created_at,
    ).model_dump()


def _mock_citations(jurisdiction: str) -> list[dict[str, Any]]:
    return [
        ControlledLegalCitation(
            citation_id="mock_citation_001",
            title="Mock Civil Code Contract Rule Reference",
            citation_type="statute",
            jurisdiction=jurisdiction or "CN",
            source_name="Mock Legal Search Provider",
            source_ref_id="source_ref_mock_legal_001",
            relevance="mock reference for contract/payment dispute workflow",
            mock_only=True,
            warnings=["Mock citation only. Not retrieved from a real legal database."],
        ).model_dump(),
        ControlledLegalCitation(
            citation_id="mock_citation_002",
            title="Mock Similar Case Reference",
            citation_type="case",
            jurisdiction=jurisdiction or "CN",
            source_name="Mock Legal Search Provider",
            source_ref_id="source_ref_mock_legal_002",
            relevance="mock similar case reference for dry-run preview",
            mock_only=True,
            warnings=["Mock citation only. Not retrieved from a real legal database."],
        ).model_dump(),
    ]


def _build_redacted_search_preview(query_text_redacted: str, citations: list[dict[str, Any]]) -> str:
    titles = "; ".join(citation["title"] for citation in citations)
    return f"Controlled legal search preview. Query: {query_text_redacted}. Mock citations: {titles}. No real legal database was called."


def _collect_warnings(guard_results: list[dict[str, Any]]) -> list[str]:
    warnings = [
        "v4.5 controlled legal search preview only.",
        "Mock legal search by default.",
        "No real legal database, LLM, OCR, or DeepSeek live provider was called.",
        "Raw query and raw legal search results are not returned, logged, or stored in Git.",
    ]
    for result in guard_results:
        warnings.extend(str(item) for item in result.get("warnings", []))
    return list(dict.fromkeys(warnings))


def _audit_event(audit_log_id: str, request: ControlledLegalSearchPreviewRequest, search_preview_id: str, citation_id: str | None, result: str, warnings: list[str], created_at: str) -> dict[str, Any]:
    return {
        "audit_log_id": audit_log_id,
        "event_type": "controlled_legal_search_preview",
        "case_id": request.case_id,
        "workspace_id": request.workspace_id,
        "search_preview_id": search_preview_id,
        "citation_id": citation_id,
        "result": result,
        "warnings": warnings,
        "created_at": created_at,
    }
