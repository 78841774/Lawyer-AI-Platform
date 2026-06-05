from datetime import datetime, timezone

from personal_delivery_packet.audit_engine import record_audit_event
from personal_delivery_packet.packet_runtime import get_delivery_packet, list_delivery_packets
from personal_delivery_packet.schemas import ReviewSummary, ReviewSummaryList
from personal_delivery_packet.storage import REVIEW_SUMMARIES_DIR, read_payload, write_payload


def build_review_summary_list() -> dict:
    summaries = [build_review_summary_record(packet.delivery_packet_id) for packet in list_delivery_packets()]
    return ReviewSummaryList(review_summaries=summaries, summary_count=len(summaries), warnings=["审核摘要仅为 metadata。"]).model_dump()


def build_review_summary(delivery_packet_id: str) -> dict | None:
    if get_delivery_packet(delivery_packet_id) is None:
        return None
    summary = build_review_summary_record(delivery_packet_id)
    now = datetime.now(timezone.utc).isoformat()
    write_payload(REVIEW_SUMMARIES_DIR, delivery_packet_id, summary.model_dump())
    record_audit_event(action="review_summary_viewed", actor="system", object_type="delivery_packet", object_id=delivery_packet_id, timestamp=now)
    return summary.model_dump()


def build_review_summary_record(delivery_packet_id: str) -> ReviewSummary:
    packet = get_delivery_packet(delivery_packet_id)
    payload = read_payload(REVIEW_SUMMARIES_DIR, delivery_packet_id)
    if payload:
        existing = ReviewSummary(**payload)
    else:
        existing = None
    status = "pending_lawyer_review"
    revision_required = False
    risk_flags = ["律师复核尚未完成", "最终锁定尚未完成"]
    final_lock_ready = False
    if packet and packet.packet_status in {"revision_requested", "not_ready", "low_confidence"}:
        status = packet.packet_status
        revision_required = True
        risk_flags = ["需要修订或补充复核 metadata"]
    if packet and packet.final_locked:
        status = "final_locked_metadata"
        risk_flags = []
        final_lock_ready = True
    return ReviewSummary(
        delivery_packet_id=delivery_packet_id,
        lawyer_review_status=status,
        reviewer_id=existing.reviewer_id if existing else None,
        review_summary_placeholder="律师复核摘要 placeholder，仅记录 metadata，不包含最终法律意见或最终报告内容。",
        revision_required=revision_required,
        risk_flags=risk_flags,
        final_lock_ready=final_lock_ready,
    )
