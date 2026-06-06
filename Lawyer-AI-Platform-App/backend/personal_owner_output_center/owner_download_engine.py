from datetime import datetime, timezone
from uuid import uuid4

from fastapi import HTTPException

from personal_owner_output_center.audit_engine import record_audit_event
from personal_owner_output_center.output_registry import get_registry_output
from personal_owner_output_center.schemas import OwnerDownloadList, OwnerDownloadMockRequest, OwnerDownloadRecord


ALLOWED_FORMATS = {"markdown", "json", "pdf_draft_metadata", "docx_draft_metadata"}
DOWNLOADS: dict[str, OwnerDownloadRecord] = {}


def _now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def _validate_request(request: OwnerDownloadMockRequest) -> list[str]:
    blocked: list[str] = []
    for field in [
        "explicit_owner_confirmation",
        "explicit_no_public_link_confirmation",
        "explicit_no_email_confirmation",
        "explicit_no_external_delivery_confirmation",
    ]:
        if not getattr(request, field):
            blocked.append(f"{field} must be true")
    if request.requested_format not in ALLOWED_FORMATS:
        blocked.append("requested_format must be markdown, json, pdf_draft_metadata, or docx_draft_metadata")
    return blocked


def create_owner_download(output_id: str, request: OwnerDownloadMockRequest) -> dict:
    if get_registry_output(output_id) is None:
        raise HTTPException(status_code=404, detail="output_id 不存在")
    blocked = _validate_request(request)
    if blocked:
        raise HTTPException(status_code=400, detail={"message": "owner download blocked", "blocked_reasons": blocked})
    download_id = f"owner_output_download_{uuid4().hex[:12]}"
    record = OwnerDownloadRecord(
        download_id=download_id,
        output_id=output_id,
        owner_user_id=request.owner_user_id,
        requested_format=request.requested_format,
        created_at=_now(),
        warnings=[
            "Owner download action creates metadata only.",
            "No file, public link, email, third-party upload, formal report, final opinion, or external delivery is created.",
        ],
    )
    DOWNLOADS[download_id] = record
    record_audit_event("owner_download_metadata_created", "owner_download", download_id)
    return record.model_dump()


def list_owner_downloads() -> dict:
    downloads = sorted(DOWNLOADS.values(), key=lambda download: download.created_at, reverse=True)
    return OwnerDownloadList(
        owner_downloads=downloads,
        download_count=len(downloads),
        warnings=["Downloads are owner-only metadata records and never expose local paths."],
    ).model_dump()


def get_owner_download(download_id: str) -> OwnerDownloadRecord | None:
    return DOWNLOADS.get(download_id)
