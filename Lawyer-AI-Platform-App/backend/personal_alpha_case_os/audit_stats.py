from collections import defaultdict
from typing import Any

from personal_alpha_case_os.schemas import (
    PersonalAlphaCaseOSAuditStageSummary,
    PersonalAlphaCaseOSAuditTimelineSummary,
    PersonalAlphaCaseOSAuditTimelineSummaryStats,
)


def build_audit_summary(case_id: str, events: list[dict[str, Any]], warnings: list[str] | None = None) -> dict[str, Any]:
    stage_events: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for event in events:
        stage_events[str(event.get("stage_id", "case_os"))].append(event)
    stage_summaries = []
    for stage_id, items in sorted(stage_events.items()):
        latest = sorted(items, key=lambda item: str(item.get("created_at", "")))[-1]
        stage_warnings = [warning for item in items for warning in item.get("warnings", []) if warning]
        stage_summaries.append(
            PersonalAlphaCaseOSAuditStageSummary(
                stage_id=stage_id,
                event_count=len(items),
                latest_result=str(latest.get("result", "")) or None,
                blocked=any(_is_blocked(item) for item in items),
                warnings=list(dict.fromkeys(stage_warnings)),
            )
        )
    summary = PersonalAlphaCaseOSAuditTimelineSummaryStats(
        total_events=len(events),
        stage_count=len(stage_events),
        blocked_event_count=sum(1 for event in events if _is_blocked(event)),
        warning_event_count=sum(1 for event in events if event.get("warnings")),
        redacted_event_count=sum(1 for event in events if event.get("redacted")),
        unsafe_event_count=sum(1 for event in events if str(event.get("safety_status", "")) in {"redacted", "blocked_unsafe_input"}),
        raw_content_event_count=sum(1 for event in events if event.get("raw_content_included")),
        latest_event_at=_latest_event_at(events),
        modules=sorted({str(event.get("module", "")) for event in events if event.get("module")}),
        stages=stage_summaries,
    )
    return PersonalAlphaCaseOSAuditTimelineSummary(
        case_id=case_id,
        summary=summary,
        mock_or_redacted_only=True,
        raw_content_included=False,
        final_legal_opinion_generated=False,
        final_report_generated=False,
        warnings=warnings or [],
    ).model_dump()


def _is_blocked(event: dict[str, Any]) -> bool:
    return str(event.get("result", "")) == "blocked" or str(event.get("event_type", "")) == "blocked"


def _latest_event_at(events: list[dict[str, Any]]) -> str | None:
    dates = sorted(str(event.get("created_at", "")) for event in events if event.get("created_at"))
    return dates[-1] if dates else None
