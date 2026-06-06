import json
from datetime import datetime, timezone
from pathlib import Path
from uuid import uuid4

from personal_ai_gateway.live_guard import build_confirmations, validate_live_gate
from personal_ai_gateway.prompt_boundary import validate_prompt_boundary
from personal_ai_gateway.provider_config import get_live_provider_config, live_mode_enabled
from personal_ai_gateway.response_sanitizer import build_draft_metadata
from personal_ai_gateway.schemas import (
    PersonalAILiveAuditEvent,
    PersonalAILiveAuditTimeline,
    PersonalAILiveRunList,
    PersonalAILiveRunRecord,
    PersonalAILiveRunRequest,
    PersonalAILiveSafetyStatus,
)
from personal_ai_gateway.usage_meter import estimate_live_usage


RUNTIME_ROOT = Path(__file__).resolve().parents[1] / "storage" / "runtime" / "personal_ai_gateway" / "live"
LIVE_RUNS_DIR = RUNTIME_ROOT / "runs"
LIVE_AUDIT_DIR = RUNTIME_ROOT / "audit"


def execute_live_gateway_run(request: PersonalAILiveRunRequest) -> dict:
    provider = get_live_provider_config(request.provider_id)
    model = request.model or (provider.model_options[0] if provider and provider.model_options else "not_configured")
    boundary_blocks = validate_prompt_boundary(request)
    live_blocks = validate_live_gate(request)
    blocked_reasons = [*boundary_blocks, *live_blocks]
    created_at = datetime.now(timezone.utc).isoformat()
    run_id = f"personal_ai_live_run_{uuid4().hex[:12]}"
    token_usage = estimate_live_usage(request)

    if request.dry_run and not boundary_blocks and provider is not None:
        status = "dry_run_completed"
        blocked_reason = None
        would_call_provider = True
    elif blocked_reasons:
        status = "live_call_blocked"
        blocked_reason = "; ".join(blocked_reasons)
        would_call_provider = False
    else:
        status = "provider_not_configured"
        blocked_reason = "provider adapter is not configured in v7.12"
        would_call_provider = True

    live_call_executed = False
    record = PersonalAILiveRunRecord(
        run_id=run_id,
        provider_id=request.provider_id,
        model=model,
        prompt_template_id=request.prompt_template_id,
        prompt_purpose=request.prompt_purpose,
        case_id=request.case_id,
        source_trace_ids=request.source_trace_ids,
        status=status,
        dry_run=request.dry_run,
        would_call_provider=would_call_provider,
        live_call_requested=not request.dry_run,
        live_call_executed=live_call_executed,
        blocked_reason=blocked_reason,
        confirmations=build_confirmations(request),
        draft_output_metadata=build_draft_metadata(request.provider_id, model, token_usage),
        created_at=created_at,
        live_mode_enabled=live_mode_enabled(),
        warnings=[
            "AI output is draft metadata only.",
            "No final legal opinion, final report, external delivery, email, or final file generation is triggered.",
        ],
    )
    _persist_live_record(record, request.actor_id, token_usage)
    return record.model_dump()


def list_live_runs() -> list[PersonalAILiveRunRecord]:
    return [PersonalAILiveRunRecord(**payload) for payload in _read_payloads(LIVE_RUNS_DIR)]


def get_live_run(run_id: str) -> PersonalAILiveRunRecord | None:
    for run in list_live_runs():
        if run.run_id == run_id:
            return run
    return None


def build_live_run_list() -> dict:
    runs = sorted(list_live_runs(), key=lambda item: item.created_at, reverse=True)
    return PersonalAILiveRunList(
        runs=runs,
        run_count=len(runs),
        live_mode_enabled=live_mode_enabled(),
        warnings=["Live run records are metadata only. No raw prompt, provider response, local path, or secret is returned."],
    ).model_dump()


def build_live_audit_timeline() -> dict:
    events = [PersonalAILiveAuditEvent(**payload) for payload in _read_payloads(LIVE_AUDIT_DIR)]
    events = sorted(events, key=lambda item: item.created_at, reverse=True)
    return PersonalAILiveAuditTimeline(
        events=events,
        event_count=len(events),
        live_mode_enabled=live_mode_enabled(),
        warnings=["Audit records contain metadata only and never return provider secrets."],
    ).model_dump()


def build_live_safety_status() -> dict:
    return PersonalAILiveSafetyStatus(
        live_mode_enabled=live_mode_enabled(),
        safety={
            "live_mode_disabled_by_default": not live_mode_enabled(),
            "api_key_exposed": False,
            "raw_content_included": False,
            "draft_only": True,
            "lawyer_review_required": True,
            "source_trace_required": True,
            "final_legal_opinion_generated": False,
            "final_report_generated": False,
            "external_delivery_triggered": False,
            "email_sent": False,
            "real_final_file_generated": False,
        },
        warnings=["v7.12 live gateway is gated and dry-run-first."],
    ).model_dump()


def _persist_live_record(record: PersonalAILiveRunRecord, actor_id: str, token_usage: dict[str, int | None]) -> None:
    _write_json(LIVE_RUNS_DIR / f"{record.run_id}.json", record.model_dump())
    event = PersonalAILiveAuditEvent(
        event_id=record.run_id,
        provider_id=record.provider_id,
        action=record.status,
        actor_id=actor_id,
        live_call_requested=record.live_call_requested,
        live_call_executed=record.live_call_executed,
        blocked_reason=record.blocked_reason,
        confirmations=record.confirmations,
        token_usage=token_usage,
        created_at=record.created_at,
    )
    _write_json(LIVE_AUDIT_DIR / f"{record.run_id}.json", event.model_dump())


def _write_json(path: Path, payload: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=True, indent=2), encoding="utf-8")


def _read_payloads(directory: Path) -> list[dict]:
    if not directory.exists():
        return []
    payloads: list[dict] = []
    for path in sorted(directory.glob("*.json")):
        try:
            payloads.append(json.loads(path.read_text(encoding="utf-8")))
        except (json.JSONDecodeError, OSError):
            continue
    return payloads
