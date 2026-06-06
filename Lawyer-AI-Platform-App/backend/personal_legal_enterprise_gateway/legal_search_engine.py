from uuid import uuid4

from personal_legal_enterprise_gateway.audit_engine import now_iso, record_audit_event
from personal_legal_enterprise_gateway.live_gate_engine import build_live_gate
from personal_legal_enterprise_gateway.provider_registry import build_provider
from personal_legal_enterprise_gateway.review_queue import create_review_item
from personal_legal_enterprise_gateway.schemas import LegalSearchRequest, LegalSearchRun, RunList
from personal_legal_enterprise_gateway.source_trace_engine import create_source_trace
from personal_legal_enterprise_gateway.storage import LEGAL_RUNS_DIR, read_payload, read_payloads, write_payload


def create_legal_search(request: LegalSearchRequest, *, dry_run: bool) -> dict:
    provider = build_provider(request.provider_id)
    run_id = f"legal_query_{uuid4().hex[:12]}"
    if provider is None:
        return LegalSearchRun(
            legal_query_id=run_id,
            provider_id=request.provider_id,
            query_type=request.query_type,
            query_text_metadata=request.query_text_metadata,
            case_id=request.case_id,
            status="blocked",
            created_at=now_iso(),
            warnings=["provider_id not found"],
        ).model_dump()
    gate = build_live_gate(provider.provider_id)
    status = "dry_run_completed" if dry_run else "adapter_unavailable_metadata_only"
    if not dry_run and gate:
        status = "live_call_blocked"
    source_trace_id = create_source_trace(run_id, provider.provider_id, "legal_search_metadata")
    run = LegalSearchRun(
        legal_query_id=run_id,
        provider_id=provider.provider_id,
        query_type=request.query_type,
        query_text_metadata=request.query_text_metadata,
        case_id=request.case_id,
        status=status,
        dry_run=True,
        live_call_allowed=False,
        live_call_executed=False,
        network_call_executed=False,
        search_results_metadata=[
            {"result_id": "legal_result_metadata_001", "title": "法律检索候选 metadata", "final_citation_selected": False},
            {"result_id": "legal_result_metadata_002", "title": "类案检索候选 metadata", "final_citation_selected": False},
        ],
        source_trace_ids=[source_trace_id],
        final_citation_selected=False,
        created_at=now_iso(),
        warnings=["Legal search results are metadata candidates only and require source trace plus lawyer review."],
    )
    write_payload(LEGAL_RUNS_DIR, run_id, run.model_dump())
    create_review_item(run_id, provider.provider_id, "legal_search_review")
    record_audit_event(provider.provider_id, "legal_search_dry_run" if dry_run else "legal_search_live_blocked", run_id)
    return run.model_dump()


def get_legal_search(run_id: str) -> LegalSearchRun | None:
    payload = read_payload(LEGAL_RUNS_DIR, run_id)
    return LegalSearchRun(**payload) if payload else None


def list_legal_searches() -> dict:
    runs = [LegalSearchRun(**payload) for payload in read_payloads(LEGAL_RUNS_DIR)]
    return RunList(runs=sorted(runs, key=lambda run: run.created_at, reverse=True), run_count=len(runs)).model_dump()

