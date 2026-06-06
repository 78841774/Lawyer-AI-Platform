from datetime import datetime, timezone
from uuid import uuid4

from personal_live_connection.audit_engine import record_audit_event
from personal_live_connection.health_engine import build_health_dry_run
from personal_live_connection.live_gate_engine import build_live_gate
from personal_live_connection.provider_registry import build_provider
from personal_live_connection.schemas import (
    LiveConnectionRunActionRequest,
    LiveConnectionRunActionResult,
    LiveConnectionRunList,
    LiveConnectionRunRecord,
    LiveConnectionRunRequest,
)
from personal_live_connection.storage import RUNS_DIR, read_payload, read_payloads, write_payload
from personal_live_connection.usage_policy_engine import build_usage_policy


def now_iso() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def create_run(request: LiveConnectionRunRequest, *, dry_run: bool) -> dict:
    provider = build_provider(request.provider_id)
    if provider is None:
        return LiveConnectionRunRecord(
            run_id=f"personal_live_run_{uuid4().hex[:12]}",
            provider_id=request.provider_id,
            provider_category="unknown",
            run_type=request.run_type,
            case_id=request.case_id,
            material_id=request.material_id,
            status="blocked",
            dry_run=dry_run,
            blocked_reasons=["provider_id is not registered"],
            created_at=now_iso(),
        ).model_dump()
    gate = build_live_gate(provider.provider_id, request)
    blocked_reasons = []
    status = "dry_run_completed"
    live_requested = not dry_run
    if not dry_run:
        blocked_reasons = (gate.live_blocked_reason if gate else "gate_unavailable").split("; ")
        status = "live_call_blocked" if blocked_reasons else "provider_adapter_not_executed"
    usage = build_usage_policy(provider.provider_id)
    health = build_health_dry_run(provider.provider_id)
    run_id = f"personal_live_run_{uuid4().hex[:12]}"
    record = LiveConnectionRunRecord(
        run_id=run_id,
        provider_id=provider.provider_id,
        provider_category=provider.provider_category,
        run_type=request.run_type,
        case_id=request.case_id,
        material_id=request.material_id,
        status=status,
        dry_run=dry_run,
        live_call_requested=live_requested,
        live_call_allowed=bool(gate.live_call_allowed if gate else False),
        live_call_executed=False,
        network_call_executed=False,
        blocked_reasons=[reason for reason in blocked_reasons if reason],
        usage_metadata=(usage.model_dump() if usage else {}),
        cost_metadata={"estimated_cost_available": False, "actual_cost_recorded": False, "billable_call_executed": False},
        health_metadata=(health.model_dump() if health else {}),
        source_trace_ids=[f"source_trace_{provider.provider_id}_metadata"],
        created_at=now_iso(),
        warnings=[
            "Run output is draft metadata only.",
            "No provider network call, raw content exposure, final legal opinion, final report, file generation, email, public link, or external delivery occurred.",
        ],
    )
    write_payload(RUNS_DIR, run_id, record.model_dump())
    record_audit_event(provider.provider_id, "dry_run_created" if dry_run else "live_run_blocked", run_id)
    return record.model_dump()


def get_run(run_id: str) -> LiveConnectionRunRecord | None:
    payload = read_payload(RUNS_DIR, run_id)
    return LiveConnectionRunRecord(**payload) if payload else None


def list_runs() -> dict:
    runs = [LiveConnectionRunRecord(**payload) for payload in read_payloads(RUNS_DIR)]
    runs = sorted(runs, key=lambda run: run.created_at, reverse=True)
    return LiveConnectionRunList(runs=runs, run_count=len(runs)).model_dump()


def record_action(run_id: str, request: LiveConnectionRunActionRequest) -> dict:
    run = get_run(run_id)
    if run is None:
        return LiveConnectionRunActionResult(
            run_id=run_id,
            action=request.action,
            status="blocked",
            blocked_reasons=["run_id is not registered"],
        ).model_dump()
    blocked = []
    if not request.owner_confirmation:
        blocked.append("owner_confirmation_missing")
    if not request.lawyer_gate_acknowledged:
        blocked.append("lawyer_gate_missing")
    if not request.source_trace_acknowledged:
        blocked.append("source_trace_acknowledged_missing")
    record_audit_event(run.provider_id, f"run_action_{request.action}", run_id)
    return LiveConnectionRunActionResult(
        run_id=run_id,
        action=request.action,
        status="blocked" if blocked else "action_recorded_metadata_only",
        blocked_reasons=blocked,
        warnings=["Action updates metadata only and does not trigger final output, provider calls, email, public links, or delivery."],
    ).model_dump()

