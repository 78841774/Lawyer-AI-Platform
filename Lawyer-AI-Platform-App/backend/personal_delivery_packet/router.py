from typing import Any

from fastapi import APIRouter, HTTPException

from personal_delivery_packet.audit_engine import build_audit_timeline
from personal_delivery_packet.export_readiness_engine import build_export_readiness, build_export_readiness_list
from personal_delivery_packet.final_lock_engine import build_final_lock_queue, submit_final_lock_action
from personal_delivery_packet.packet_item_runtime import build_packet_item_list, create_mock_packet_item, get_packet_item
from personal_delivery_packet.packet_runtime import build_delivery_packet_list, create_mock_delivery_packet, get_delivery_packet
from personal_delivery_packet.review_summary_engine import build_review_summary, build_review_summary_list
from personal_delivery_packet.runtime_registry import get_runtime, list_runtimes
from personal_delivery_packet.safety_engine import build_safety_status
from personal_delivery_packet.schemas import (
    DeliveryPacketMockRequest,
    FinalLockActionRequest,
    PacketItemMockRequest,
    PersonalDeliveryPacketStatus,
    SourceBundleMockRequest,
)
from personal_delivery_packet.source_bundle_runtime import build_source_bundle_list, create_mock_source_bundle, get_source_bundle


router = APIRouter(prefix="/personal-delivery-packet", tags=["personal-delivery-packet"])


@router.get("/status")
def status() -> dict[str, Any]:
    return PersonalDeliveryPacketStatus(
        warnings=["v7.6 当前仅为个人生产交付包 metadata 骨架，不会真实导出、发送邮件或对外交付。"],
    ).model_dump()


@router.get("/runtimes")
def runtimes() -> dict[str, Any]:
    return list_runtimes()


@router.get("/runtimes/{runtime_id}")
def runtime_detail(runtime_id: str) -> dict[str, Any]:
    runtime = get_runtime(runtime_id)
    if runtime is None:
        raise HTTPException(status_code=404, detail="runtime_id 不存在")
    return runtime.model_dump()


@router.post("/packets/mock")
def packet_mock(request: DeliveryPacketMockRequest) -> dict[str, Any]:
    return create_mock_delivery_packet(request)


@router.get("/packets")
def packets() -> dict[str, Any]:
    return build_delivery_packet_list()


@router.get("/packets/{delivery_packet_id}")
def packet_detail(delivery_packet_id: str) -> dict[str, Any]:
    record = get_delivery_packet(delivery_packet_id)
    if record is None:
        raise HTTPException(status_code=404, detail="delivery_packet_id 不存在")
    return record.model_dump()


@router.post("/packet-items/mock")
def packet_item_mock(request: PacketItemMockRequest) -> dict[str, Any]:
    return create_mock_packet_item(request)


@router.get("/packet-items")
def packet_items() -> dict[str, Any]:
    return build_packet_item_list()


@router.get("/packet-items/{packet_item_id}")
def packet_item_detail(packet_item_id: str) -> dict[str, Any]:
    record = get_packet_item(packet_item_id)
    if record is None:
        raise HTTPException(status_code=404, detail="packet_item_id 不存在")
    return record.model_dump()


@router.post("/source-bundles/mock")
def source_bundle_mock(request: SourceBundleMockRequest) -> dict[str, Any]:
    return create_mock_source_bundle(request)


@router.get("/source-bundles")
def source_bundles() -> dict[str, Any]:
    return build_source_bundle_list()


@router.get("/source-bundles/{source_bundle_id}")
def source_bundle_detail(source_bundle_id: str) -> dict[str, Any]:
    record = get_source_bundle(source_bundle_id)
    if record is None:
        raise HTTPException(status_code=404, detail="source_bundle_id 不存在")
    return record.model_dump()


@router.get("/export-readiness")
def export_readiness() -> dict[str, Any]:
    return build_export_readiness_list()


@router.get("/export-readiness/{delivery_packet_id}")
def export_readiness_detail(delivery_packet_id: str) -> dict[str, Any]:
    record = build_export_readiness(delivery_packet_id)
    if record is None:
        raise HTTPException(status_code=404, detail="delivery_packet_id 不存在")
    return record


@router.get("/final-locks")
def final_locks() -> dict[str, Any]:
    return build_final_lock_queue()


@router.post("/final-locks/{delivery_packet_id}/actions")
def final_lock_action(delivery_packet_id: str, request: FinalLockActionRequest) -> dict[str, Any]:
    return submit_final_lock_action(delivery_packet_id, request)


@router.get("/review-summaries")
def review_summaries() -> dict[str, Any]:
    return build_review_summary_list()


@router.get("/review-summaries/{delivery_packet_id}")
def review_summary_detail(delivery_packet_id: str) -> dict[str, Any]:
    record = build_review_summary(delivery_packet_id)
    if record is None:
        raise HTTPException(status_code=404, detail="delivery_packet_id 不存在")
    return record


@router.get("/audit")
def audit() -> dict[str, Any]:
    return build_audit_timeline()


@router.get("/safety")
def safety() -> dict[str, Any]:
    return build_safety_status()
