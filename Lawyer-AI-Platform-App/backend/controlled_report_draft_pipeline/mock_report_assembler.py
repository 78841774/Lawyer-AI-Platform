from typing import Any
from uuid import uuid4

from controlled_report_draft_pipeline.audit import append_controlled_report_draft_audit_log
from controlled_report_draft_pipeline.guards import run_all_controlled_report_draft_guards
from controlled_report_draft_pipeline.runtime_storage import load_controlled_report_draft, store_controlled_report_draft
from controlled_report_draft_pipeline.schemas import (
    ControlledReportDraftAssembleRequest,
    ControlledReportDraftRecord,
    ControlledReportDraftResult,
    ControlledReportDraftSourceRef,
    ControlledReportDraftStatus,
    utc_now,
)


def get_controlled_report_draft_status() -> dict[str, Any]:
    return ControlledReportDraftStatus(
        warnings=[
            "v4.6 is local-only controlled report draft assembly.",
            "Mock report assembly is enabled by default.",
            "No real LLM, DeepSeek live, real OCR, or real legal database provider is called.",
            "No final legal opinion is generated.",
            "Manual lawyer review and explicit assembly confirmation are required.",
        ]
    ).model_dump()


def assemble_mock_controlled_report(request: ControlledReportDraftAssembleRequest) -> dict[str, Any]:
    created_at = utc_now()
    draft_id = f"controlled_report_draft_{uuid4().hex[:12]}"
    audit_log_id = f"controlled_report_draft_audit_{uuid4().hex[:12]}"
    guard_results = run_all_controlled_report_draft_guards(request)
    allowed_to_continue = all(bool(result.get("allowed")) for result in guard_results)
    warnings = _collect_warnings(guard_results)

    if not request.preview_only:
        allowed_to_continue = False
        warnings.append("preview_only must remain true for v4.6 controlled report draft assembly.")

    if not allowed_to_continue:
        append_controlled_report_draft_audit_log(_audit_event(audit_log_id, request, draft_id, "blocked_by_controlled_report_draft_guard", warnings, created_at))
        return ControlledReportDraftResult(
            draft_id=draft_id,
            case_id=request.case_id,
            workspace_id=request.workspace_id,
            status="blocked",
            mock_report_assembled=False,
            final_legal_opinion_generated=False,
            llm_called=False,
            deepseek_live_called=False,
            real_ocr_called=False,
            real_legal_database_called=False,
            raw_material_text_included=False,
            raw_ocr_text_included=False,
            raw_legal_search_results_included=False,
            mock_assembled_report={},
            source_refs=[],
            citations=[],
            guard_results=guard_results,
            audit_log_id=audit_log_id,
            allowed_to_continue=False,
            warnings=list(dict.fromkeys(warnings)),
            created_at=created_at,
        ).model_dump()

    source_refs = _build_source_refs(draft_id, request)
    citations = _build_citation_summaries(request.citation_ids, request.legal_search_preview_ids)
    mock_assembled_report = _build_mock_assembled_report(request, source_refs, citations)
    storage = store_controlled_report_draft(
        draft_id,
        {
            "case_id": request.case_id,
            "workspace_id": request.workspace_id,
            "mock_assembled_report": mock_assembled_report,
            "source_refs": source_refs,
            "citations": citations,
            "created_at": created_at,
        },
    )
    warnings.extend(storage.get("warnings", []))
    append_controlled_report_draft_audit_log(_audit_event(audit_log_id, request, draft_id, "mock_report_draft_assembled", warnings, created_at))
    return ControlledReportDraftResult(
        draft_id=draft_id,
        case_id=request.case_id,
        workspace_id=request.workspace_id,
        status="mock_draft",
        mock_report_assembled=True,
        final_legal_opinion_generated=False,
        llm_called=False,
        deepseek_live_called=False,
        real_ocr_called=False,
        real_legal_database_called=False,
        raw_material_text_included=False,
        raw_ocr_text_included=False,
        raw_legal_search_results_included=False,
        report_draft_storage_path=storage["storage_path"],
        mock_assembled_report=mock_assembled_report,
        source_refs=source_refs,
        citations=citations,
        guard_results=guard_results,
        audit_log_id=audit_log_id,
        allowed_to_continue=True,
        warnings=list(dict.fromkeys(warnings)),
        created_at=created_at,
    ).model_dump()


def load_mock_controlled_report(draft_id: str) -> dict[str, Any]:
    loaded = load_controlled_report_draft(draft_id)
    return ControlledReportDraftRecord(
        draft_id=str(loaded.get("draft_id", draft_id)),
        case_id=str(loaded.get("case_id", "")),
        workspace_id=str(loaded.get("workspace_id", "")),
        mock_assembled_report=dict(loaded.get("mock_assembled_report", {})),
        source_refs=list(loaded.get("source_refs", [])),
        citations=list(loaded.get("citations", [])),
        warnings=list(loaded.get("warnings", [])),
        created_at=str(loaded.get("created_at", utc_now())),
    ).model_dump()


def _build_mock_assembled_report(request: ControlledReportDraftAssembleRequest, source_refs: list[dict[str, Any]], citations: list[dict[str, Any]]) -> dict[str, Any]:
    return {
        "title": "Mock Controlled Report Draft",
        "status": "mock_draft",
        "case_id": request.case_id,
        "workspace_id": request.workspace_id,
        "sections": {
            "controlled_material_summary": {
                "material_preview_ids": request.material_preview_ids,
                "summary": "Mock material preview summary only. No raw material text included.",
            },
            "controlled_ocr_summary": {
                "ocr_preview_ids": request.ocr_preview_ids,
                "summary": "Mock OCR preview summary only. No raw OCR text included.",
            },
            "controlled_legal_search_summary": {
                "legal_search_preview_ids": request.legal_search_preview_ids,
                "citation_ids": request.citation_ids,
                "summary": "Mock legal search citation summary only. No real legal database result included.",
            },
            "source_trace_summary": {
                "source_ref_count": len(source_refs),
                "citation_count": len(citations),
                "summary": "Source trace merge placeholder. Mock or redacted IDs only.",
            },
            "lawyer_review_checklist": [
                "Confirm controlled material previews before relying on facts.",
                "Confirm controlled OCR previews before using any extracted text.",
                "Confirm citations against authoritative legal sources outside this mock draft.",
                "Confirm A1-A13 analysis remains unchanged; A10 remains 争议焦点法律深化分析.",
                "Do not treat this mock draft as a final legal opinion.",
            ],
        },
        "legal_opinion_finalized": False,
        "requires_human_review": True,
        "mock_only": True,
        "warnings": [
            "No real LLM call.",
            "No real material raw text included.",
            "No raw OCR text included.",
            "No real legal search result included.",
            "Not a final legal opinion.",
            "Manual lawyer review required.",
        ],
    }


def _build_source_refs(draft_id: str, request: ControlledReportDraftAssembleRequest) -> list[dict[str, Any]]:
    linked_sources: list[tuple[str, str]] = []
    linked_sources.extend(("controlled_material_preview", item) for item in request.material_preview_ids)
    linked_sources.extend(("controlled_ocr_preview", item) for item in request.ocr_preview_ids)
    linked_sources.extend(("controlled_legal_search_preview", item) for item in request.legal_search_preview_ids)
    linked_sources.extend(("controlled_legal_citation", item) for item in request.citation_ids)
    if not linked_sources:
        linked_sources.append(("controlled_report_draft", draft_id))
    return [
        ControlledReportDraftSourceRef(
            source_ref_id=f"source_ref_controlled_report_draft_{index:03d}",
            draft_id=draft_id,
            linked_source_type=source_type,
            linked_source_id=source_id,
        ).model_dump()
        for index, (source_type, source_id) in enumerate(linked_sources, start=1)
    ]


def _build_citation_summaries(citation_ids: list[str], legal_search_preview_ids: list[str]) -> list[dict[str, Any]]:
    if not citation_ids:
        return []
    preview_id = legal_search_preview_ids[0] if legal_search_preview_ids else "legal_search_preview_not_provided"
    return [
        {
            "citation_id": citation_id,
            "search_preview_id": preview_id,
            "title": f"Mock citation summary for {citation_id}",
            "mock_only": True,
            "real_legal_database_called": False,
            "warning": "Mock citation summary only. No real legal database was called.",
        }
        for citation_id in citation_ids
    ]


def _collect_warnings(guard_results: list[dict[str, Any]]) -> list[str]:
    warnings = [
        "v4.6 controlled report draft assembly only.",
        "Mock report assembly by default.",
        "No real LLM, DeepSeek live, OCR, or legal database provider was called.",
        "Raw material text, raw OCR text, and raw legal search results are not returned, logged, or stored in Git.",
        "No final legal opinion was generated.",
    ]
    for result in guard_results:
        warnings.extend(str(item) for item in result.get("warnings", []))
    return list(dict.fromkeys(warnings))


def _audit_event(audit_log_id: str, request: ControlledReportDraftAssembleRequest, draft_id: str, result: str, warnings: list[str], created_at: str) -> dict[str, Any]:
    return {
        "audit_log_id": audit_log_id,
        "event_type": "controlled_report_draft_assembly",
        "case_id": request.case_id,
        "workspace_id": request.workspace_id,
        "draft_id": draft_id,
        "result": result,
        "warnings": list(dict.fromkeys(warnings)),
        "created_at": created_at,
    }

