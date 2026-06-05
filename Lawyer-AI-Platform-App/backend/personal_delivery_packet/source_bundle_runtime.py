from datetime import datetime, timezone
from uuid import uuid4

from fastapi import HTTPException

from personal_delivery_packet.audit_engine import record_audit_event
from personal_delivery_packet.packet_runtime import ensure_packet_editable, get_delivery_packet
from personal_delivery_packet.schemas import SourceBundleList, SourceBundleMockRequest, SourceBundleRecord
from personal_delivery_packet.storage import SOURCE_BUNDLES_DIR, read_payload, read_payloads, write_payload


def create_mock_source_bundle(request: SourceBundleMockRequest) -> dict:
    ensure_packet_editable(request.delivery_packet_id)
    blocked = validate_request(request)
    if blocked:
        raise HTTPException(status_code=400, detail={"message": "来源追踪包请求被阻断。", "blocked_reasons": blocked})
    source_bundle_id = f"personal_source_bundle_{uuid4().hex[:12]}"
    created_at = datetime.now(timezone.utc).isoformat()
    source_trace_ids = list(dict.fromkeys(request.source_trace_ids))
    record = SourceBundleRecord(
        source_bundle_id=source_bundle_id,
        delivery_packet_id=request.delivery_packet_id,
        source_trace_ids=source_trace_ids,
        bundle_scope=request.bundle_scope,
        source_trace_count=len(source_trace_ids),
        confirmed_source_count=0,
        unconfirmed_source_count=len(source_trace_ids),
        created_at=created_at,
        warnings=["来源追踪包仅聚合 source trace id metadata，不返回 raw content。"],
    )
    write_payload(SOURCE_BUNDLES_DIR, source_bundle_id, record.model_dump())
    record_audit_event(action="source_bundle_mock_created", actor="system", object_type="source_bundle", object_id=source_bundle_id, timestamp=created_at)
    return record.model_dump()


def get_source_bundle(source_bundle_id: str) -> SourceBundleRecord | None:
    payload = read_payload(SOURCE_BUNDLES_DIR, source_bundle_id)
    return SourceBundleRecord(**payload) if payload else None


def list_source_bundles() -> list[SourceBundleRecord]:
    return [SourceBundleRecord(**payload) for payload in read_payloads(SOURCE_BUNDLES_DIR)]


def list_source_bundles_for_packet(delivery_packet_id: str) -> list[SourceBundleRecord]:
    return [bundle for bundle in list_source_bundles() if bundle.delivery_packet_id == delivery_packet_id]


def build_source_bundle_list() -> dict:
    records = sorted(list_source_bundles(), key=lambda record: record.created_at, reverse=True)
    return SourceBundleList(source_bundles=records, bundle_count=len(records), warnings=["来源追踪包列表仅包含 metadata。"]).model_dump()


def validate_request(request: SourceBundleMockRequest) -> list[str]:
    blocked: list[str] = []
    if get_delivery_packet(request.delivery_packet_id) is None:
        blocked.append("delivery_packet_id 不存在")
    for field in ["explicit_mock_confirmation", "explicit_source_trace_confirmation", "explicit_no_raw_content_confirmation"]:
        if not getattr(request, field):
            blocked.append(f"{field} 必须为 true")
    if not request.bundle_scope.strip():
        blocked.append("bundle_scope 不能为空")
    return blocked
