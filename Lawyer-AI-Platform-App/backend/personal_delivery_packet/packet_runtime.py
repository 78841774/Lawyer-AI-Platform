from datetime import datetime, timezone
from uuid import uuid4

from fastapi import HTTPException

from personal_delivery_packet.audit_engine import record_audit_event
from personal_delivery_packet.safety_engine import default_safety_flags
from personal_delivery_packet.schemas import DeliveryPacketList, DeliveryPacketMockRequest, DeliveryPacketRecord
from personal_delivery_packet.storage import DELIVERY_PACKETS_DIR, read_payload, read_payloads, write_payload


def create_mock_delivery_packet(request: DeliveryPacketMockRequest) -> dict:
    blocked = validate_request(request)
    if blocked:
        raise HTTPException(status_code=400, detail={"message": "交付包草案请求被阻断。", "blocked_reasons": blocked})
    delivery_packet_id = f"personal_delivery_packet_{uuid4().hex[:12]}"
    created_at = datetime.now(timezone.utc).isoformat()
    record = DeliveryPacketRecord(
        delivery_packet_id=delivery_packet_id,
        production_case_id=request.production_case_id,
        workflow_run_id=request.workflow_run_id,
        packet_title=request.packet_title,
        packet_scope=request.packet_scope,
        client_alias=request.client_alias,
        delivery_purpose=request.delivery_purpose,
        safety_flags=default_safety_flags(),
        created_at=created_at,
        warnings=["当前仅为交付包 metadata 骨架，不生成最终法律意见、最终报告或真实交付文件。"],
    )
    write_payload(DELIVERY_PACKETS_DIR, delivery_packet_id, record.model_dump())
    record_audit_event(action="delivery_packet_mock_created", actor="system", object_type="delivery_packet", object_id=delivery_packet_id, timestamp=created_at)
    return record.model_dump()


def get_delivery_packet(delivery_packet_id: str) -> DeliveryPacketRecord | None:
    payload = read_payload(DELIVERY_PACKETS_DIR, delivery_packet_id)
    return DeliveryPacketRecord(**payload) if payload else None


def save_delivery_packet(record: DeliveryPacketRecord) -> None:
    write_payload(DELIVERY_PACKETS_DIR, record.delivery_packet_id, record.model_dump())


def list_delivery_packets() -> list[DeliveryPacketRecord]:
    return [DeliveryPacketRecord(**payload) for payload in read_payloads(DELIVERY_PACKETS_DIR)]


def build_delivery_packet_list() -> dict:
    records = sorted(list_delivery_packets(), key=lambda record: record.created_at, reverse=True)
    return DeliveryPacketList(delivery_packets=records, packet_count=len(records), warnings=["交付包列表仅包含 metadata。"]).model_dump()


def ensure_packet_editable(delivery_packet_id: str) -> DeliveryPacketRecord:
    record = get_delivery_packet(delivery_packet_id)
    if record is None:
        raise HTTPException(status_code=404, detail="delivery_packet_id 不存在")
    if record.final_locked:
        raise HTTPException(status_code=409, detail="delivery packet 已最终锁定，不允许继续修改 metadata")
    return record


def validate_request(request: DeliveryPacketMockRequest) -> list[str]:
    blocked: list[str] = []
    for field in [
        "explicit_mock_confirmation",
        "explicit_lawyer_review_confirmation",
        "explicit_no_raw_content_confirmation",
        "explicit_no_final_opinion_confirmation",
        "explicit_no_external_delivery_confirmation",
    ]:
        if not getattr(request, field):
            blocked.append(f"{field} 必须为 true")
    if not request.production_case_id.strip():
        blocked.append("production_case_id 不能为空")
    if not request.packet_title.strip():
        blocked.append("packet_title 不能为空")
    return blocked
