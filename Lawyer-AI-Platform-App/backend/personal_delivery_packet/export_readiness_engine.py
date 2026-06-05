from personal_delivery_packet.audit_engine import record_audit_event
from personal_delivery_packet.packet_item_runtime import ALLOWED_ITEM_TYPES, list_packet_items_for_packet
from personal_delivery_packet.packet_runtime import get_delivery_packet, list_delivery_packets
from personal_delivery_packet.schemas import ExportReadiness, ExportReadinessList
from personal_delivery_packet.source_bundle_runtime import list_source_bundles_for_packet


REQUIRED_ITEM_TYPES = [
    "case_metadata_summary",
    "material_processing_summary",
    "ai_draft_summary",
    "intelligence_summary",
    "skill_studio_summary",
    "lawyer_review_summary",
    "source_trace_summary",
    "export_placeholder",
]


def build_export_readiness_list() -> dict:
    readiness = [build_export_readiness_record(packet.delivery_packet_id) for packet in list_delivery_packets()]
    return ExportReadinessList(
        readiness=[record for record in readiness if record is not None],
        readiness_count=len([record for record in readiness if record is not None]),
        warnings=["导出准备度仅为 metadata 检查，不生成真实交付文件。"],
    ).model_dump()


def build_export_readiness(delivery_packet_id: str) -> dict | None:
    record = build_export_readiness_record(delivery_packet_id)
    if record is None:
        return None
    from datetime import datetime, timezone

    record_audit_event(action="export_readiness_checked", actor="system", object_type="delivery_packet", object_id=delivery_packet_id, timestamp=datetime.now(timezone.utc).isoformat())
    return record.model_dump()


def build_export_readiness_record(delivery_packet_id: str) -> ExportReadiness | None:
    packet = get_delivery_packet(delivery_packet_id)
    if packet is None:
        return None
    item_types = {item.item_type for item in list_packet_items_for_packet(delivery_packet_id) if item.item_type in ALLOWED_ITEM_TYPES}
    missing = [item_type for item_type in REQUIRED_ITEM_TYPES if item_type not in item_types]
    source_trace_complete = bool(list_source_bundles_for_packet(delivery_packet_id))
    lawyer_review_complete = packet.packet_status in {"final_locked", "ready_for_controlled_export"}
    final_lock_ready = not missing and source_trace_complete
    status = "not_ready"
    if item_types or source_trace_complete:
        status = "in_progress"
    if final_lock_ready:
        status = "review_required"
    if final_lock_ready and lawyer_review_complete:
        status = "ready_for_final_lock"
    return ExportReadiness(
        delivery_packet_id=delivery_packet_id,
        export_readiness_status=status,
        required_item_count=len(REQUIRED_ITEM_TYPES),
        included_item_count=len(item_types),
        missing_item_types=missing,
        source_trace_complete=source_trace_complete,
        lawyer_review_complete=lawyer_review_complete,
        final_lock_ready=final_lock_ready,
        export_ready=False,
        external_delivery_ready=False,
        risk_flags=[] if final_lock_ready else ["仍有交付项、来源追踪或律师复核 metadata 未完成"],
        checklist=[
            "律师复核必需",
            "最终锁定必需",
            "来源追踪必需",
            "不生成最终法律意见",
            "不生成最终报告",
            "不自动对外交付",
            "不发送邮件",
            "不生成真实最终交付文件",
        ],
    )
