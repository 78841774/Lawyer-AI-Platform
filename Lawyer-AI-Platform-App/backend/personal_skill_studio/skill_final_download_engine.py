from datetime import datetime, timezone
from uuid import uuid4

from fastapi import HTTPException

from personal_skill_studio.audit_engine import record_audit_event
from personal_skill_studio.schemas import (
    SkillFinalOwnerDownloadList,
    SkillFinalOwnerDownloadRecord,
    SkillFinalOwnerDownloadRequest,
)
from personal_skill_studio.skill_final_draft_engine import get_skill_final_draft
from personal_skill_studio.source_trace_engine import create_source_trace
from personal_skill_studio.storage import SKILL_FINAL_DRAFT_DOWNLOADS_DIR, read_payload, read_payloads, write_payload


ALLOWED_FORMATS = {"Markdown", "JSON", "PDF draft metadata", "DOCX draft metadata"}


def _validate_request(request: SkillFinalOwnerDownloadRequest) -> list[str]:
    blocked: list[str] = []
    if request.requested_format not in ALLOWED_FORMATS:
        blocked.append("requested_format 仅支持 Markdown / JSON / PDF draft metadata / DOCX draft metadata")
    for field in [
        "explicit_owner_confirmation",
        "explicit_no_public_link_confirmation",
        "explicit_no_email_confirmation",
        "explicit_no_external_delivery_confirmation",
        "explicit_no_auto_publish_confirmation",
    ]:
        if not getattr(request, field):
            blocked.append(f"{field} 必须为 true")
    return blocked


def create_skill_final_owner_download(skill_id: str, request: SkillFinalOwnerDownloadRequest) -> dict:
    draft = get_skill_final_draft(skill_id)
    if draft is None:
        raise HTTPException(status_code=404, detail="skill_id 不存在")
    blocked = _validate_request(request)
    if blocked:
        raise HTTPException(status_code=400, detail={"message": "Skill final draft owner download 请求被阻断。", "blocked_reasons": blocked})
    created_at = datetime.now(timezone.utc).isoformat()
    download_id = f"skill_final_download_{uuid4().hex[:12]}"
    record = SkillFinalOwnerDownloadRecord(
        download_id=download_id,
        skill_id=skill_id,
        requested_format=request.requested_format,
        baseline_discovered=draft.baseline_discovered,
        baseline_complete=draft.baseline_complete,
        created_at=created_at,
        warnings=[
            "Owner download is metadata-only and draft-only.",
            "No public link, email, external delivery, Skill publish, or real file export is triggered.",
        ],
    )
    write_payload(SKILL_FINAL_DRAFT_DOWNLOADS_DIR, download_id, record.model_dump())
    create_source_trace(
        source_trace_id=f"skill_studio_source_trace_{download_id}_1",
        source_type="skill_final_draft_download_metadata",
        source_label="Skill final draft owner-only download metadata",
        linked_object_type="skill_final_draft_owner_download",
        linked_object_id=download_id,
        skill_candidate_id=skill_id,
        created_at=created_at,
    )
    record_audit_event(action="skill_final_draft_owner_download_mock_created", actor="system", object_type="skill_final_draft", object_id=skill_id, timestamp=created_at)
    return record.model_dump()


def get_skill_final_owner_download(download_id: str) -> SkillFinalOwnerDownloadRecord | None:
    payload = read_payload(SKILL_FINAL_DRAFT_DOWNLOADS_DIR, download_id)
    return SkillFinalOwnerDownloadRecord(**payload) if payload else None


def list_skill_final_owner_downloads() -> list[SkillFinalOwnerDownloadRecord]:
    return [SkillFinalOwnerDownloadRecord(**payload) for payload in read_payloads(SKILL_FINAL_DRAFT_DOWNLOADS_DIR)]


def build_skill_final_owner_download_list() -> dict:
    records = sorted(list_skill_final_owner_downloads(), key=lambda record: record.created_at, reverse=True)
    return SkillFinalOwnerDownloadList(
        owner_downloads=records,
        download_count=len(records),
        warnings=["Skill final draft downloads are owner-only metadata; no real PDF/DOCX or public link is created."],
    ).model_dump()
