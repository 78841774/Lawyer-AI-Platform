from uuid import uuid4

from personal_legal_enterprise_gateway.audit_engine import now_iso, record_audit_event
from personal_legal_enterprise_gateway.live_gate_engine import build_live_gate
from personal_legal_enterprise_gateway.provider_registry import build_provider
from personal_legal_enterprise_gateway.review_queue import create_review_item
from personal_legal_enterprise_gateway.schemas import EnterpriseLookupRequest, EnterpriseLookupRun, RunList
from personal_legal_enterprise_gateway.source_trace_engine import create_source_trace
from personal_legal_enterprise_gateway.storage import ENTERPRISE_RUNS_DIR, read_payload, read_payloads, write_payload


def create_enterprise_lookup(request: EnterpriseLookupRequest, *, dry_run: bool) -> dict:
    provider = build_provider(request.provider_id)
    run_id = f"enterprise_lookup_{uuid4().hex[:12]}"
    if provider is None:
        return EnterpriseLookupRun(
            enterprise_lookup_id=run_id,
            provider_id=request.provider_id,
            lookup_type=request.lookup_type,
            company_query_metadata=request.company_query_metadata,
            case_id=request.case_id,
            status="blocked",
            created_at=now_iso(),
            warnings=["provider_id not found"],
        ).model_dump()
    gate = build_live_gate(provider.provider_id)
    status = "dry_run_completed" if dry_run else "adapter_unavailable_metadata_only"
    if not dry_run and gate:
        status = "live_call_blocked"
    source_trace_id = create_source_trace(run_id, provider.provider_id, "enterprise_lookup_metadata")
    run = EnterpriseLookupRun(
        enterprise_lookup_id=run_id,
        provider_id=provider.provider_id,
        lookup_type=request.lookup_type,
        company_query_metadata=request.company_query_metadata,
        case_id=request.case_id,
        status=status,
        dry_run=True,
        live_call_allowed=False,
        live_call_executed=False,
        network_call_executed=False,
        enterprise_results_metadata=[
            {"result_id": "enterprise_result_metadata_001", "title": "企业登记候选 metadata", "final_company_finding": False},
            {"result_id": "enterprise_result_metadata_002", "title": "企业风险候选 metadata", "final_company_finding": False},
        ],
        source_trace_ids=[source_trace_id],
        verification_required=True,
        created_at=now_iso(),
        warnings=["Enterprise results are verification metadata only and do not become final fact findings."],
    )
    write_payload(ENTERPRISE_RUNS_DIR, run_id, run.model_dump())
    create_review_item(run_id, provider.provider_id, "enterprise_verification_review")
    record_audit_event(provider.provider_id, "enterprise_lookup_dry_run" if dry_run else "enterprise_lookup_live_blocked", run_id)
    return run.model_dump()


def get_enterprise_lookup(run_id: str) -> EnterpriseLookupRun | None:
    payload = read_payload(ENTERPRISE_RUNS_DIR, run_id)
    return EnterpriseLookupRun(**payload) if payload else None


def list_enterprise_lookups() -> dict:
    runs = [EnterpriseLookupRun(**payload) for payload in read_payloads(ENTERPRISE_RUNS_DIR)]
    return RunList(runs=sorted(runs, key=lambda run: run.created_at, reverse=True), run_count=len(runs)).model_dump()

