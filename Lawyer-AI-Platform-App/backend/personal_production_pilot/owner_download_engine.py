from datetime import datetime, timezone
from uuid import uuid4

from fastapi import HTTPException

from personal_production_pilot.audit_engine import record_audit_event
from personal_production_pilot.document_output_engine import get_output
from personal_production_pilot.schemas import OwnerDownloadList, OwnerDownloadMockRequest, OwnerDownloadRecord
from personal_production_pilot.storage import OWNER_DOWNLOADS_DIR, read_payload, read_payloads, write_payload


def _validate_download_request(request: OwnerDownloadMockRequest) -> list[str]:
    blocked: list[str] = []
    for field in [
        "explicit_owner_confirmation",
        "explicit_no_public_link_confirmation",
        "explicit_no_email_confirmation",
        "explicit_no_external_delivery_confirmation",
    ]:
        if not getattr(request, field):
            blocked.append(f"{field} 必须为 true")
    if request.requested_format not in {"Markdown", "JSON", "PDF draft", "DOCX draft"}:
        blocked.append("requested_format 仅支持 Markdown / JSON / PDF draft / DOCX draft")
    return blocked


def create_owner_download(output_id: str, request: OwnerDownloadMockRequest) -> dict:
    if get_output(output_id) is None:
        raise HTTPException(status_code=404, detail="output_id 不存在")
    blocked = _validate_download_request(request)
    if blocked:
        raise HTTPException(status_code=400, detail={"message": "owner download 请求被阻断", "blocked_reasons": blocked})
    download_id = f"owner_download_{uuid4().hex[:12]}"
    created_at = datetime.now(timezone.utc).isoformat()
    record = OwnerDownloadRecord(
        download_id=download_id,
        output_id=output_id,
        requested_format=request.requested_format,
        created_at=created_at,
        warnings=[
            "Owner download is metadata only in v7.17.",
            "No file path is exposed.",
            "No public link, email, third-party share, or client delivery is triggered.",
        ],
    )
    write_payload(OWNER_DOWNLOADS_DIR, download_id, record.model_dump())
    record_audit_event(action="owner_download_mock_created", actor="system", object_type="owner_download", object_id=download_id, timestamp=created_at)
    return record.model_dump()


def get_owner_download(download_id: str) -> OwnerDownloadRecord | None:
    payload = read_payload(OWNER_DOWNLOADS_DIR, download_id)
    return OwnerDownloadRecord(**payload) if payload else None


def list_owner_downloads() -> list[OwnerDownloadRecord]:
    return [OwnerDownloadRecord(**payload) for payload in read_payloads(OWNER_DOWNLOADS_DIR)]


def build_owner_download_list() -> dict:
    downloads = sorted(list_owner_downloads(), key=lambda download: download.created_at, reverse=True)
    return OwnerDownloadList(
        owner_downloads=downloads,
        download_count=len(downloads),
        warnings=["Owner downloads are restricted to owner metadata; no public URL or external delivery is created."],
    ).model_dump()
