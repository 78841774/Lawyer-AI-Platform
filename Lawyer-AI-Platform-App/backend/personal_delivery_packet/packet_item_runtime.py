from datetime import datetime, timezone
from uuid import uuid4

from fastapi import HTTPException

from personal_delivery_packet.audit_engine import record_audit_event
from personal_delivery_packet.packet_runtime import ensure_packet_editable, get_delivery_packet
from personal_delivery_packet.schemas import PacketItemList, PacketItemMockRequest, PacketItemRecord
from personal_delivery_packet.storage import PACKET_ITEMS_DIR, read_payload, read_payloads, write_payload


ALLOWED_ITEM_TYPES = {
    "case_metadata_summary",
    "material_processing_summary",
    "ai_draft_summary",
    "intelligence_summary",
    "skill_studio_summary",
    "lawyer_review_summary",
    "source_trace_summary",
    "export_placeholder",
}


def create_mock_packet_item(request: PacketItemMockRequest) -> dict:
    ensure_packet_editable(request.delivery_packet_id)
    blocked = validate_request(request)
    if blocked:
        raise HTTPException(status_code=400, detail={"message": "交付项草案请求被阻断。", "blocked_reasons": blocked})
    packet_item_id = f"personal_packet_item_{uuid4().hex[:12]}"
    created_at = datetime.now(timezone.utc).isoformat()
    record = PacketItemRecord(
        packet_item_id=packet_item_id,
        delivery_packet_id=request.delivery_packet_id,
        item_title=request.item_title,
        item_type=request.item_type,
        linked_object_type=request.linked_object_type,
        linked_object_id=request.linked_object_id,
        source_trace_ids=request.source_trace_ids,
        created_at=created_at,
        warnings=["交付项仅为草案 metadata，默认不纳入真实导出。"],
    )
    write_payload(PACKET_ITEMS_DIR, packet_item_id, record.model_dump())
    record_audit_event(action="packet_item_mock_created", actor="system", object_type="packet_item", object_id=packet_item_id, timestamp=created_at)
    return record.model_dump()


def get_packet_item(packet_item_id: str) -> PacketItemRecord | None:
    payload = read_payload(PACKET_ITEMS_DIR, packet_item_id)
    return PacketItemRecord(**payload) if payload else None


def list_packet_items() -> list[PacketItemRecord]:
    return [PacketItemRecord(**payload) for payload in read_payloads(PACKET_ITEMS_DIR)]


def list_packet_items_for_packet(delivery_packet_id: str) -> list[PacketItemRecord]:
    return [item for item in list_packet_items() if item.delivery_packet_id == delivery_packet_id]


def build_packet_item_list() -> dict:
    records = sorted(list_packet_items(), key=lambda record: record.created_at, reverse=True)
    return PacketItemList(packet_items=records, item_count=len(records), warnings=["交付项列表仅包含 metadata。"]).model_dump()


def validate_request(request: PacketItemMockRequest) -> list[str]:
    blocked: list[str] = []
    if get_delivery_packet(request.delivery_packet_id) is None:
        blocked.append("delivery_packet_id 不存在")
    for field in ["explicit_mock_confirmation", "explicit_no_raw_content_confirmation", "explicit_no_final_opinion_confirmation"]:
        if not getattr(request, field):
            blocked.append(f"{field} 必须为 true")
    if request.item_type not in ALLOWED_ITEM_TYPES:
        blocked.append("item_type 不支持")
    if not request.item_title.strip():
        blocked.append("item_title 不能为空")
    return blocked
