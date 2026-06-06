from personal_skill_studio.training_artifacts.intake_safety_engine import intake_safety_flags


def build_intake_audit(intake_id: str, events: list[dict[str, str | bool]]) -> dict:
    return {
        "intake_id": intake_id,
        "events": events,
        "event_count": len(events),
        **intake_safety_flags(redaction_completed=_has_redaction(events), ready_for_codex_training=_is_ready(events)),
        "warnings": ["Audit metadata excludes raw content, local paths, key values, and private identity fields."],
    }


def default_audit_events(intake_id: str) -> list[dict[str, str | bool]]:
    return [
        {"event_id": f"{intake_id}_created", "action": "create_real_closed_case_intake_metadata", "metadata_only": True},
        {"event_id": f"{intake_id}_redaction", "action": "run_redaction_metadata_check", "metadata_only": True},
        {"event_id": f"{intake_id}_classification", "action": "classify_case_cause_metadata", "metadata_only": True},
        {"event_id": f"{intake_id}_segments", "action": "segment_training_sample_metadata", "metadata_only": True},
        {"event_id": f"{intake_id}_review", "action": "create_manual_review_queue", "metadata_only": True},
    ]


def _has_redaction(events: list[dict[str, str | bool]]) -> bool:
    return any(event.get("action") == "run_redaction_metadata_check" for event in events)


def _is_ready(events: list[dict[str, str | bool]]) -> bool:
    return _has_redaction(events) and any(event.get("action") == "segment_training_sample_metadata" for event in events)
