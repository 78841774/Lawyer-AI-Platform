from datetime import datetime, timezone
from uuid import uuid4

from fastapi import HTTPException

from personal_case_analysis.skill_loader import build_skill_baseline_report
from personal_production_pilot.audit_engine import record_audit_event
from personal_production_pilot.review_queue import create_review_item
from personal_production_pilot.schemas import (
    PilotOutputList,
    PilotOutputMockRequest,
    PilotOutputRecord,
    SkillFinalDraft,
    SkillFinalDraftList,
)
from personal_production_pilot.source_trace_engine import create_source_trace
from personal_production_pilot.storage import OUTPUTS_DIR, read_payload, read_payloads, write_payload


def build_skill_final_drafts() -> dict:
    baseline_report = build_skill_baseline_report()
    drafts: list[SkillFinalDraft] = []
    for baseline in baseline_report.get("baselines", []):
        title = "案件事实提炼 Skill 最终稿" if baseline.get("skill_key") == "case_fact_extraction_skill" else "案件法律分析 Skill 最终稿"
        draft_id = f"pilot_skill_final_draft_{baseline.get('skill_key')}"
        drafts.append(
            SkillFinalDraft(
                draft_id=draft_id,
                skill_key=str(baseline.get("skill_key")),
                title=title,
                source_skill_id=str(baseline.get("source_skill_id")),
                source_package_id=baseline.get("source_package_id"),
                warnings=[
                    "Skill final draft is owner-download metadata only.",
                    "No Skill is published automatically.",
                    "No open-case material is written to the training set.",
                ],
            )
        )
    return SkillFinalDraftList(
        skill_final_drafts=drafts,
        draft_count=len(drafts),
        warnings=["Two Skill final drafts are available as owner-only download metadata; no public link or publishing action is created."],
    ).model_dump()


def _validate_output_request(request: PilotOutputMockRequest) -> list[str]:
    blocked: list[str] = []
    for field in [
        "explicit_owner_confirmation",
        "explicit_no_external_delivery_confirmation",
        "explicit_no_final_opinion_confirmation",
    ]:
        if not getattr(request, field):
            blocked.append(f"{field} 必须为 true")
    if request.format not in {"Markdown", "JSON", "PDF draft", "DOCX draft"}:
        blocked.append("format 仅支持 Markdown / JSON / PDF draft / DOCX draft")
    return blocked


def create_mock_output(request: PilotOutputMockRequest) -> dict:
    blocked = _validate_output_request(request)
    if blocked:
        raise HTTPException(status_code=400, detail={"message": "pilot output 请求被阻断", "blocked_reasons": blocked})
    output_id = f"pilot_output_{uuid4().hex[:12]}"
    created_at = datetime.now(timezone.utc).isoformat()
    record = PilotOutputRecord(
        output_id=output_id,
        run_id=request.run_id,
        output_type=request.output_type,
        title=request.title,
        format=request.format,
        created_at=created_at,
        warnings=[
            "Output is owner-only draft metadata.",
            "It is not a final legal opinion or formal lawyer report.",
            "No public link, email, third-party upload, or external delivery is triggered.",
        ],
    )
    write_payload(OUTPUTS_DIR, output_id, record.model_dump())
    create_source_trace(
        source_trace_id=f"pilot_source_trace_{output_id}_1",
        source_type="pilot_output_metadata",
        source_label="Pilot output metadata",
        linked_object_type="pilot_output",
        linked_object_id=output_id,
        run_id=request.run_id,
        created_at=created_at,
    )
    create_review_item(linked_object_type="pilot_output", linked_object_id=output_id, created_at=created_at)
    record_audit_event(action="pilot_output_mock_created", actor="system", object_type="pilot_output", object_id=output_id, timestamp=created_at)
    return record.model_dump()


def get_output(output_id: str) -> PilotOutputRecord | None:
    payload = read_payload(OUTPUTS_DIR, output_id)
    return PilotOutputRecord(**payload) if payload else None


def list_outputs() -> list[PilotOutputRecord]:
    return [PilotOutputRecord(**payload) for payload in read_payloads(OUTPUTS_DIR)]


def build_output_list() -> dict:
    outputs = sorted(list_outputs(), key=lambda output: output.created_at, reverse=True)
    return PilotOutputList(
        outputs=outputs,
        output_count=len(outputs),
        warnings=["Pilot outputs are owner-only draft metadata; no generated document is auto-sent or public."],
    ).model_dump()
