from datetime import UTC, datetime
from uuid import uuid4

from personal_skill_studio.training_artifacts.case_cause_classifier import classify_case_cause
from personal_skill_studio.training_artifacts.intake_audit_engine import build_intake_audit, default_audit_events
from personal_skill_studio.training_artifacts.intake_review_queue import apply_review_action, build_review_queue
from personal_skill_studio.training_artifacts.intake_safety_engine import build_intake_safety, intake_safety_flags
from personal_skill_studio.training_artifacts.intake_source_trace_engine import build_source_traces
from personal_skill_studio.training_artifacts.redaction_engine import build_redaction_report
from personal_skill_studio.training_artifacts.schemas import (
    RealClosedCaseIntakeStatus,
    RealClosedCaseTrainingIntake,
    RealClosedCaseTrainingIntakeList,
    RealClosedCaseTrainingIntakeRecord,
    RealClosedCaseTrainingIntakeRequest,
    TrainingIntakeReviewActionRequest,
)
from personal_skill_studio.training_artifacts.storage import (
    REAL_CLOSED_CASE_INTAKES_DIR,
    read_payload,
    read_payloads,
    write_payload,
)
from personal_skill_studio.training_artifacts.training_sample_registry import summarize_segments
from personal_skill_studio.training_artifacts.training_sample_segmenter import build_segments


def build_intake_status() -> dict:
    records = [_record_from_payload(payload) for payload in read_payloads(REAL_CLOSED_CASE_INTAKES_DIR)]
    return RealClosedCaseIntakeStatus(
        intake_count=len(records),
        redaction_completed=all(record.redaction_completed for record in records) if records else False,
        ready_for_codex_training=any(record.ready_for_codex_training for record in records),
        warnings=[
            "v7.31a prepares real closed-case intake metadata only.",
            "No Codex training execution, provider call, or training-set write is performed.",
        ],
    ).model_dump()


def create_intake(request: RealClosedCaseTrainingIntakeRequest) -> dict:
    intake_id = f"real_closed_case_intake_v7_31a_{uuid4().hex[:12]}"
    intake = RealClosedCaseTrainingIntake(
        intake_id=intake_id,
        case_reference_label=request.case_reference_label,
        owner_user_id=request.owner_user_id,
        authorization_confirmed=request.authorization_confirmed,
        case_closed_confirmed=request.case_closed_confirmed,
        target_case_cause_path=request.target_case_cause_path,
        target_skill_ids=request.target_skill_ids,
        created_at=datetime.now(UTC).isoformat(),
        warnings=[
            "Input is represented as authorized closed-case metadata only.",
            "Raw content is neither retained nor returned.",
        ],
    )
    record = RealClosedCaseTrainingIntakeRecord(
        intake=intake,
        source_traces=build_source_traces(intake_id),
        review_queue=build_review_queue(intake_id),
        audit_events=[
            {"event_id": f"{intake_id}_created", "action": "create_real_closed_case_intake_metadata", "metadata_only": True}
        ],
        warnings=["v7.31a intake is not ready for Codex training until redaction, classification, segmentation, and review metadata exist."],
    )
    _write_record(record)
    return _record_payload(record)


def list_intakes() -> dict:
    records = [_record_from_payload(payload) for payload in read_payloads(REAL_CLOSED_CASE_INTAKES_DIR)]
    return RealClosedCaseTrainingIntakeList(
        intakes=[record.intake for record in records],
        intake_count=len(records),
        redaction_completed=all(record.redaction_completed for record in records) if records else False,
        ready_for_codex_training=any(record.ready_for_codex_training for record in records),
        warnings=["Real closed-case intakes are metadata-only and owner-only."],
    ).model_dump()


def get_intake(intake_id: str) -> dict | None:
    record = _read_record(intake_id)
    if record is None:
        return None
    return _record_payload(record)


def get_redaction_report(intake_id: str) -> dict | None:
    record = _ensure_redaction(_read_record(intake_id))
    if record is None:
        return None
    return record.redaction_report.model_dump() if record.redaction_report else None


def run_redaction(intake_id: str) -> dict | None:
    record = _read_record(intake_id)
    if record is None:
        return None
    record = _ensure_redaction(record)
    _write_record(record)
    return record.redaction_report.model_dump() if record.redaction_report else None


def get_classification(intake_id: str) -> dict | None:
    record = _ensure_classification(_ensure_redaction(_read_record(intake_id)))
    if record is None:
        return None
    return record.classification.model_dump() if record.classification else None


def run_classification(intake_id: str) -> dict | None:
    record = _ensure_classification(_ensure_redaction(_read_record(intake_id)))
    if record is None:
        return None
    _write_record(record)
    return record.classification.model_dump() if record.classification else None


def get_segments(intake_id: str) -> dict | None:
    record = _ensure_segments(_ensure_classification(_ensure_redaction(_read_record(intake_id))))
    if record is None:
        return None
    return _segments_payload(record)


def run_segmentation(intake_id: str) -> dict | None:
    record = _ensure_segments(_ensure_classification(_ensure_redaction(_read_record(intake_id))))
    if record is None:
        return None
    _write_record(record)
    return _segments_payload(record)


def get_review_queue(intake_id: str) -> dict | None:
    record = _read_record(intake_id)
    if record is None:
        return None
    if not record.review_queue:
        record.review_queue = build_review_queue(intake_id)
        _write_record(record)
    return {
        "intake_id": intake_id,
        "review_items": [item.model_dump() for item in record.review_queue],
        "review_item_count": len(record.review_queue),
        **_flags(record),
    }


def submit_review_action(intake_id: str, review_item_id: str, request: TrainingIntakeReviewActionRequest) -> dict | None:
    record = _read_record(intake_id)
    if record is None:
        return None
    if not record.review_queue:
        record.review_queue = build_review_queue(intake_id)
    updated = []
    matched = None
    for item in record.review_queue:
        if item.review_item_id == review_item_id:
            item = apply_review_action(item, request)
            matched = item
        updated.append(item)
    if matched is None:
        return None
    record.review_queue = updated
    record.audit_events.append({"event_id": f"{review_item_id}_action", "action": request.action, "metadata_only": True})
    _write_record(record)
    return {"intake_id": intake_id, "review_item": matched.model_dump(), **_flags(record)}


def get_source_traces(intake_id: str) -> dict | None:
    record = _read_record(intake_id)
    if record is None:
        return None
    if not record.source_traces:
        record.source_traces = build_source_traces(intake_id)
        _write_record(record)
    return {
        "intake_id": intake_id,
        "source_traces": [trace.model_dump() for trace in record.source_traces],
        "source_trace_count": len(record.source_traces),
        **_flags(record),
    }


def get_audit(intake_id: str) -> dict | None:
    record = _read_record(intake_id)
    if record is None:
        return None
    events = record.audit_events or default_audit_events(intake_id)
    return build_intake_audit(intake_id, events)


def get_safety(intake_id: str) -> dict | None:
    if _read_record(intake_id) is None:
        return None
    return build_intake_safety(intake_id)


def _ensure_redaction(record: RealClosedCaseTrainingIntakeRecord | None) -> RealClosedCaseTrainingIntakeRecord | None:
    if record is None:
        return None
    if record.redaction_report is None:
        record.redaction_report = build_redaction_report(record.intake.intake_id)
        record.intake.redaction_status = "redaction_metadata_completed"
        record.intake.redaction_completed = True
        record.redaction_completed = True
        record.audit_events.append({"event_id": f"{record.intake.intake_id}_redaction", "action": "run_redaction_metadata_check", "metadata_only": True})
    return record


def _ensure_classification(record: RealClosedCaseTrainingIntakeRecord | None) -> RealClosedCaseTrainingIntakeRecord | None:
    if record is None:
        return None
    if record.classification is None:
        record.classification = classify_case_cause(record.intake)
        record.audit_events.append({"event_id": f"{record.intake.intake_id}_classification", "action": "classify_case_cause_metadata", "metadata_only": True})
    return record


def _ensure_segments(record: RealClosedCaseTrainingIntakeRecord | None) -> RealClosedCaseTrainingIntakeRecord | None:
    if record is None:
        return None
    if not record.source_traces:
        record.source_traces = build_source_traces(record.intake.intake_id)
    if record.classification and not record.segments:
        record.segments = build_segments(record.classification, record.source_traces)
        record.ready_for_codex_training = True
        record.audit_events.append({"event_id": f"{record.intake.intake_id}_segments", "action": "segment_training_sample_metadata", "metadata_only": True})
    return record


def _segments_payload(record: RealClosedCaseTrainingIntakeRecord) -> dict:
    summary = summarize_segments(record.segments)
    return {
        "intake_id": record.intake.intake_id,
        "segments": [segment.model_dump() for segment in record.segments],
        "segment_summary": summary,
        **_flags(record),
    }


def _flags(record: RealClosedCaseTrainingIntakeRecord) -> dict[str, bool]:
    return intake_safety_flags(
        redaction_completed=bool(record.redaction_report and record.redaction_report.redaction_completed),
        ready_for_codex_training=bool(record.ready_for_codex_training),
    )


def _record_payload(record: RealClosedCaseTrainingIntakeRecord) -> dict:
    payload = record.model_dump()
    payload.update(_flags(record))
    return payload


def _read_record(intake_id: str) -> RealClosedCaseTrainingIntakeRecord | None:
    payload = read_payload(REAL_CLOSED_CASE_INTAKES_DIR, intake_id)
    if payload:
        return _record_from_payload(payload)
    for payload in read_payloads(REAL_CLOSED_CASE_INTAKES_DIR):
        record = _record_from_payload(payload)
        if record.intake.intake_id == intake_id:
            return record
    return None


def _record_from_payload(payload: dict) -> RealClosedCaseTrainingIntakeRecord:
    return RealClosedCaseTrainingIntakeRecord(**payload)


def _write_record(record: RealClosedCaseTrainingIntakeRecord) -> None:
    write_payload(REAL_CLOSED_CASE_INTAKES_DIR, record.intake.intake_id, record.model_dump())
