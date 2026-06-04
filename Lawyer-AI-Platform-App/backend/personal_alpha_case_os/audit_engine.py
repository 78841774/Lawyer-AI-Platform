from typing import Any
from uuid import uuid4

from personal_alpha_case_os.schemas import PersonalAlphaCaseOSAuditEvent, PersonalAlphaCaseOSAuditTimeline
from personal_alpha_workspace.schemas import utc_now


def build_case_os_audit_timeline(case_id: str, context: dict[str, Any]) -> dict[str, Any]:
    timeline: list[dict[str, Any]] = []
    for run in context.get("workspace_runs", []):
        if not isinstance(run, dict):
            continue
        for event in run.get("unified_audit_timeline", []):
            if not isinstance(event, dict):
                continue
            timeline.append(
                PersonalAlphaCaseOSAuditEvent(
                    timeline_event_id=str(event.get("timeline_event_id", f"case_os_event_{uuid4().hex[:8]}")),
                    case_id=case_id,
                    workspace_run_id=str(event.get("workspace_run_id", run.get("workspace_run_id", ""))),
                    stage_id=str(event.get("stage_id", "workspace")),
                    event_type=str(event.get("event_type", "metadata_stage_status")),
                    result=str(event.get("result", "metadata_ready")),
                    mock_or_redacted_only=True,
                    raw_content_included=False,
                    created_at=str(event.get("created_at", run.get("created_at", utc_now()))),
                ).model_dump()
            )
    for stage_id, payload_key in [
        ("source_review_decision", "source_decisions"),
        ("final_gate", "gate_decisions"),
        ("final_packet", "packets"),
        ("lawyer_final_review", "lawyer_actions"),
        ("final_lock", "locks"),
    ]:
        for item in context.get(payload_key, []):
            if not isinstance(item, dict):
                continue
            event_source_id = str(
                item.get(
                    "decision_id",
                    item.get(
                        "gate_decision_id",
                        item.get("packet_id", item.get("action_id", item.get("lock_id", uuid4().hex[:8]))),
                    ),
                )
            )
            timeline.append(
                PersonalAlphaCaseOSAuditEvent(
                    timeline_event_id=f"case_os_{stage_id}_{event_source_id}",
                    case_id=case_id,
                    workspace_run_id=str(item.get("workspace_run_id", context.get("latest_workspace_run_id", ""))),
                    stage_id=stage_id,
                    event_type="metadata_stage_status",
                    result=str(item.get("status", item.get("decision", item.get("action", "metadata_ready")))),
                    mock_or_redacted_only=True,
                    raw_content_included=False,
                    created_at=str(item.get("created_at", utc_now())),
                ).model_dump()
            )
    timeline.sort(key=lambda event: str(event.get("created_at", "")))
    return PersonalAlphaCaseOSAuditTimeline(
        case_id=case_id,
        timeline=timeline,
        event_count=len(timeline),
        mock_or_redacted_only=True,
        raw_content_included=False,
        warnings=["Case OS audit timeline is metadata-only. No raw content is returned."],
    ).model_dump()
