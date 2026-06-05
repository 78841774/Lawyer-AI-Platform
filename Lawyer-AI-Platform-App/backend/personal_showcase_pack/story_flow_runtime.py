from datetime import datetime, timezone
from uuid import uuid4

from fastapi import HTTPException

from personal_showcase_pack.audit_engine import record_audit_event
from personal_showcase_pack.pilot_sample_runtime import get_pilot_sample
from personal_showcase_pack.safety_engine import default_safety_flags, validate_mock_metadata_text
from personal_showcase_pack.schemas import StoryFlowList, StoryFlowMockRequest, StoryFlowRecord, StoryStageCard
from personal_showcase_pack.storage import STORY_FLOWS_DIR, read_payload, read_payloads, write_payload


STAGE_DEFINITIONS = {
    "case_intake": ("案件录入", "case_os", "试点样本的案件入口 metadata 已就绪"),
    "material_processing": ("材料处理", "personal_material_runtime", "材料处理与 OCR metadata 已就绪"),
    "ai_draft": ("AI 草稿", "personal_ai_gateway", "AI 草稿仅为 mock metadata，不是最终意见"),
    "legal_enterprise_check": ("法律/企业信息核验", "personal_intelligence_gateway", "法律与企业信息核验 metadata 已就绪"),
    "skill_studio": ("技能沉淀", "personal_skill_studio", "经验包与技能候选 metadata 已就绪"),
    "delivery_packet": ("交付包", "personal_delivery_packet", "交付包草案 metadata 已就绪"),
    "final_lock": ("最终锁定", "final_lock_engine", "最终锁定仅更新 metadata，不触发真实导出"),
}


def create_mock_story_flow(request: StoryFlowMockRequest) -> dict:
    blocked = validate_request(request)
    if blocked:
        raise HTTPException(status_code=400, detail={"message": "Story Flow 请求被阻断。", "blocked_reasons": blocked})
    story_flow_id = f"personal_story_flow_{uuid4().hex[:12]}"
    created_at = datetime.now(timezone.utc).isoformat()
    selected = request.selected_stage_ids or list(STAGE_DEFINITIONS.keys())
    record = StoryFlowRecord(
        story_flow_id=story_flow_id,
        pilot_sample_id=request.pilot_sample_id,
        story_title=request.story_title.strip(),
        story_scope=request.story_scope.strip(),
        selected_stage_ids=selected,
        stage_cards=build_stage_cards(selected),
        source_trace_summary={"source_trace_required": True, "coverage_rate": 100, "raw_content_returned": False},
        lawyer_review_summary={"requires_lawyer_review": True, "review_status": "lawyer_review_required"},
        final_lock_summary={"final_lock_required": True, "final_lock_status": "ready_for_controlled_demo"},
        trust_summary=default_safety_flags(),
        created_at=created_at,
        warnings=["Story Flow 仅为 mock metadata 展示，不包含真实客户、案件、判决或企业信息。"],
    )
    write_payload(STORY_FLOWS_DIR, story_flow_id, record.model_dump())
    record_audit_event(action="story_flow_mock_created", actor="system", object_type="story_flow", object_id=story_flow_id, timestamp=created_at)
    return record.model_dump()


def get_story_flow(story_flow_id: str) -> StoryFlowRecord | None:
    payload = read_payload(STORY_FLOWS_DIR, story_flow_id)
    return StoryFlowRecord(**payload) if payload else None


def list_story_flows() -> list[StoryFlowRecord]:
    return [StoryFlowRecord(**payload) for payload in read_payloads(STORY_FLOWS_DIR)]


def build_story_flow_list() -> dict:
    records = sorted(list_story_flows(), key=lambda record: record.created_at, reverse=True)
    return StoryFlowList(story_flows=records, story_flow_count=len(records), warnings=["Story Flow 列表仅包含 mock metadata。"]).model_dump()


def build_stage_cards(stage_ids: list[str]) -> list[StoryStageCard]:
    cards = []
    for stage_id in stage_ids:
        display_name, linked_runtime, summary = STAGE_DEFINITIONS[stage_id]
        cards.append(
            StoryStageCard(
                stage_id=stage_id,
                display_name=display_name,
                linked_runtime=linked_runtime,
                mock_metadata_summary=summary,
            )
        )
    return cards


def validate_request(request: StoryFlowMockRequest) -> list[str]:
    blocked = []
    for field in [
        "explicit_mock_confirmation",
        "explicit_no_real_case_confirmation",
        "explicit_no_final_opinion_confirmation",
        "explicit_no_external_delivery_confirmation",
    ]:
        if not getattr(request, field):
            blocked.append(f"{field} 必须为 true")
    if get_pilot_sample(request.pilot_sample_id) is None:
        blocked.append("pilot_sample_id 不存在")
    blocked.extend(validate_mock_metadata_text(request.story_title, "story_title"))
    blocked.extend(validate_mock_metadata_text(request.story_scope, "story_scope"))
    invalid = [stage_id for stage_id in request.selected_stage_ids if stage_id not in STAGE_DEFINITIONS]
    if invalid:
        blocked.append("selected_stage_ids 包含不支持的阶段")
    return blocked
