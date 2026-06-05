import re
from datetime import datetime, timezone
from uuid import uuid4

from fastapi import HTTPException

from personal_delivery_packet.audit_engine import record_audit_event
from personal_delivery_packet.packet_runtime import get_delivery_packet, list_delivery_packets, save_delivery_packet
from personal_delivery_packet.schemas import FinalLockActionRequest, FinalLockList, FinalLockRecord
from personal_delivery_packet.storage import FINAL_LOCKS_DIR, read_payloads, write_payload


ALLOWED_ACTIONS = {
    "lock_for_controlled_export": ("controlled_export_locked", True, "final_locked"),
    "request_revision": ("revision_requested", False, "revision_requested"),
    "reject": ("rejected", False, "rejected"),
    "mark_not_ready": ("not_ready", False, "not_ready"),
    "mark_low_confidence": ("low_confidence", False, "low_confidence"),
}
SAFE_REVIEWER_ID_PATTERN = re.compile(r"^[A-Za-z0-9_-]{1,64}$")


def build_final_lock_queue() -> dict:
    locks = [FinalLockRecord(**payload) for payload in read_payloads(FINAL_LOCKS_DIR)]
    locks = sorted(locks, key=lambda record: record.timestamp, reverse=True)
    queue = [packet for packet in list_delivery_packets() if not packet.final_locked]
    queue = sorted(queue, key=lambda record: record.created_at, reverse=True)
    return FinalLockList(
        final_locks=locks,
        final_lock_queue=queue,
        lock_count=len(locks),
        queue_count=len(queue),
        warnings=["最终锁定队列仅为 metadata，不触发真实导出、邮件或对外交付。"],
    ).model_dump()


def submit_final_lock_action(delivery_packet_id: str, request: FinalLockActionRequest) -> dict:
    packet = get_delivery_packet(delivery_packet_id)
    if packet is None:
        raise HTTPException(status_code=404, detail="delivery_packet_id 不存在")
    if request.action not in ALLOWED_ACTIONS:
        raise HTTPException(status_code=400, detail="action 不支持")
    if not SAFE_REVIEWER_ID_PATTERN.match(request.reviewer_id):
        raise HTTPException(status_code=400, detail="reviewer_id 不安全")
    if (
        not request.explicit_lawyer_confirmation
        or not request.explicit_final_lock_confirmation
        or not request.explicit_no_real_export_confirmation
        or not request.explicit_no_email_confirmation
        or not request.explicit_no_final_opinion_confirmation
        or not request.explicit_no_final_report_confirmation
        or not request.explicit_no_external_delivery_confirmation
    ):
        raise HTTPException(status_code=400, detail="confirmation 不完整")
    status, final_locked, packet_status = ALLOWED_ACTIONS[request.action]
    now = datetime.now(timezone.utc).isoformat()
    updated = packet.model_copy(update={"packet_status": packet_status, "final_locked": final_locked, "updated_at": now})
    save_delivery_packet(updated)
    final_lock_id = f"personal_final_lock_{uuid4().hex[:12]}"
    record = FinalLockRecord(
        final_lock_id=final_lock_id,
        delivery_packet_id=delivery_packet_id,
        action=request.action,
        final_lock_status=status,
        final_locked=final_locked,
        timestamp=now,
        warnings=["final lock 仅更新 metadata，不生成最终法律意见、最终报告、真实文件、邮件或对外交付。"],
    )
    write_payload(FINAL_LOCKS_DIR, final_lock_id, record.model_dump())
    record_audit_event(action="final_lock_action", actor=request.reviewer_id, object_type="delivery_packet", object_id=delivery_packet_id, timestamp=now)
    return record.model_dump()
