from personal_skill_studio.training_artifacts.practice_runtime_safety_engine import v731g_safety_flags
from personal_skill_studio.training_artifacts.schemas import (
    PracticeRuntimeLoadAudit,
    PracticeRuntimeLoadList,
    PracticeRuntimeLoadRecord,
    PracticeRuntimeRiskEvent,
    PracticeRuntimeSourceTraceBundle,
    PracticeRuntimeUsageEvent,
    PracticeRuntimeUsageList,
    V731gPracticeRuntimeStatus,
)
from personal_skill_studio.training_artifacts.storage import (
    PRACTICE_RUNTIME_LOADS_DIR,
    PRACTICE_RUNTIME_RISK_EVENTS_DIR,
    PRACTICE_RUNTIME_USAGE_DIR,
    read_payload,
    read_payloads,
    write_payload,
)


def write_runtime_load(record: PracticeRuntimeLoadRecord) -> None:
    write_payload(PRACTICE_RUNTIME_LOADS_DIR, record.runtime_load_id, record.model_dump())


def get_runtime_load(runtime_load_id: str) -> dict | None:
    record = _read_runtime_load(runtime_load_id)
    return record.model_dump() if record else None


def list_runtime_load_records() -> list[PracticeRuntimeLoadRecord]:
    records = [
        PracticeRuntimeLoadRecord(**payload)
        for payload in read_payloads(PRACTICE_RUNTIME_LOADS_DIR)
        if payload.get("runtime_load_id")
    ]
    return sorted(records, key=lambda item: item.loaded_at, reverse=True)


def list_runtime_loads() -> dict:
    records = list_runtime_load_records()
    return PracticeRuntimeLoadList(
        runtime_loads=records,
        load_count=len(records),
        loaded_disabled_count=_count_status(records, "loaded_disabled"),
        loaded_gray_count=_count_status(records, "loaded_gray"),
        loaded_active_count=_count_status(records, "loaded_active"),
        disabled_count=_count_status(records, "disabled"),
        rolled_back_count=_count_status(records, "rolled_back"),
        blocked_count=_count_status(records, "blocked"),
        warnings=[
            "Practice runtime load registry stores lawyer-approved metadata only.",
            "Disable and rollback change load status only; packages and trace records are preserved.",
        ],
        **v731g_safety_flags(),
    ).model_dump()


def get_runtime_load_audit(runtime_load_id: str) -> dict | None:
    record = _read_runtime_load(runtime_load_id)
    if record is None:
        return None
    return PracticeRuntimeLoadAudit(
        runtime_load_id=runtime_load_id,
        events=record.audit_events,
        event_count=len(record.audit_events),
        warnings=["Runtime audit contains metadata events only."],
        **v731g_safety_flags(),
    ).model_dump()


def get_runtime_load_source_trace(runtime_load_id: str) -> dict | None:
    record = _read_runtime_load(runtime_load_id)
    if record is None:
        return None
    return PracticeRuntimeSourceTraceBundle(**record.source_trace_bundle.model_dump()).model_dump()


def write_usage_event(event: PracticeRuntimeUsageEvent) -> None:
    write_payload(PRACTICE_RUNTIME_USAGE_DIR, event.usage_event_id, event.model_dump())


def write_risk_event(event: PracticeRuntimeRiskEvent) -> None:
    write_payload(PRACTICE_RUNTIME_RISK_EVENTS_DIR, event.risk_event_id, event.model_dump())


def list_usage_events() -> list[PracticeRuntimeUsageEvent]:
    events = [
        PracticeRuntimeUsageEvent(**payload)
        for payload in read_payloads(PRACTICE_RUNTIME_USAGE_DIR)
        if payload.get("usage_event_id")
    ]
    return sorted(events, key=lambda item: item.timestamp, reverse=True)


def list_risk_events() -> list[PracticeRuntimeRiskEvent]:
    events = [
        PracticeRuntimeRiskEvent(**payload)
        for payload in read_payloads(PRACTICE_RUNTIME_RISK_EVENTS_DIR)
        if payload.get("risk_event_id")
    ]
    return sorted(events, key=lambda item: item.created_at, reverse=True)


def list_runtime_usage() -> dict:
    usage_events = list_usage_events()
    risk_events = list_risk_events()
    return PracticeRuntimeUsageList(
        usage_events=usage_events,
        usage_event_count=len(usage_events),
        risk_events=risk_events,
        risk_event_count=len(risk_events),
        warnings=["Usage monitoring stores request metadata and policy outcomes only."],
        **v731g_safety_flags(),
    ).model_dump()


def count_usage_for_load(runtime_load_id: str) -> int:
    return sum(1 for event in list_usage_events() if event.runtime_load_id == runtime_load_id and event.allowed)


def build_v731g_status() -> dict:
    records = list_runtime_load_records()
    usage_events = list_usage_events()
    risk_events = list_risk_events()
    return V731gPracticeRuntimeStatus(
        runtime_load_count=len(records),
        loaded_gray_count=_count_status(records, "loaded_gray"),
        loaded_active_count=_count_status(records, "loaded_active"),
        disabled_count=_count_status(records, "disabled"),
        blocked_count=_count_status(records, "blocked"),
        usage_event_count=len(usage_events),
        risk_event_count=len(risk_events),
        warnings=[
            "v7.31g loads only v7.31f lawyer-approved package metadata into controlled runtime registry.",
            "Policy evaluation, monitoring, disable, and rollback remain owner-only and metadata-safe.",
        ],
        **v731g_safety_flags(),
    ).model_dump()


def _read_runtime_load(runtime_load_id: str) -> PracticeRuntimeLoadRecord | None:
    payload = read_payload(PRACTICE_RUNTIME_LOADS_DIR, runtime_load_id)
    return PracticeRuntimeLoadRecord(**payload) if payload else None


def _count_status(records: list[PracticeRuntimeLoadRecord], status: str) -> int:
    return sum(1 for record in records if record.load_status == status)
