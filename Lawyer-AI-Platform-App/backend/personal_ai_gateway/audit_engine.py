import json
from pathlib import Path

from personal_ai_gateway.schemas import PersonalAIAuditEvent, PersonalAIAuditTimeline, PersonalAIRunList, PersonalAIRunRecord


RUNTIME_ROOT = Path(__file__).resolve().parents[1] / "storage" / "runtime" / "personal_ai_gateway"
AUDIT_DIR = RUNTIME_ROOT / "audit"
RUNS_DIR = RUNTIME_ROOT / "runs"


def persist_run(record: PersonalAIRunRecord) -> None:
    _write_json(RUNS_DIR / f"{record.ai_run_id}.json", record.model_dump())
    event = PersonalAIAuditEvent(
        ai_run_id=record.ai_run_id,
        provider_id=record.provider_id,
        template_id=record.template_id,
        case_id=record.case_id,
        purpose=record.purpose,
        mode=record.mode,
        would_call_provider=record.would_call_provider,
        live_call_executed=record.live_call_executed,
        manual_approval_confirmed=record.manual_approval_confirmed,
        draft_only=record.draft_only,
        requires_lawyer_review=record.requires_lawyer_review,
        token_usage_estimate={
            "estimated_input_tokens": record.token_usage.estimated_input_tokens,
            "estimated_output_tokens": record.token_usage.estimated_output_tokens,
            "estimated_total_tokens": record.token_usage.estimated_total_tokens,
        },
        created_at=record.created_at,
    )
    _write_json(AUDIT_DIR / f"{record.ai_run_id}.json", event.model_dump())


def list_runs() -> list[PersonalAIRunRecord]:
    return [PersonalAIRunRecord(**payload) for payload in _read_payloads(RUNS_DIR)]


def get_run(ai_run_id: str) -> PersonalAIRunRecord | None:
    for run in list_runs():
        if run.ai_run_id == ai_run_id:
            return run
    return None


def build_run_list() -> dict:
    runs = sorted(list_runs(), key=lambda run: run.created_at, reverse=True)
    return PersonalAIRunList(
        runs=runs,
        run_count=len(runs),
        warnings=["Run records are mock metadata only. Raw prompts and provider responses are not stored."],
    ).model_dump()


def build_audit_timeline() -> dict:
    events = [PersonalAIAuditEvent(**payload) for payload in _read_payloads(AUDIT_DIR)]
    events = sorted(events, key=lambda event: event.created_at, reverse=True)
    return PersonalAIAuditTimeline(
        events=events,
        event_count=len(events),
        warnings=["Audit records contain metadata only. No raw material, local path, or provider secret is returned."],
    ).model_dump()


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
