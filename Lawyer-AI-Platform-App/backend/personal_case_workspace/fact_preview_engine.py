from datetime import datetime, timezone
from uuid import uuid4

from personal_case_workspace.schemas import FactPreviewList, FactPreviewMockRequest, FactPreviewRecord
from personal_case_workspace.storage import get_case, list_materials


def _now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def _seed_preview() -> FactPreviewRecord:
    materials = list_materials("case_workspace_mock_001")
    material_ids = [material.material_id for material in materials[:3]]
    source_trace_ids = [trace_id for material in materials[:3] for trace_id in material.source_trace_ids]
    return FactPreviewRecord(
        fact_preview_id="fact_preview_mock_001",
        case_id="case_workspace_mock_001",
        material_ids=material_ids,
        ocr_job_ids=[f"ocr_status_{material_id}" for material_id in material_ids],
        source_trace_ids=source_trace_ids,
        fact_summary_draft="事实摘要 draft metadata：围绕合同履行、沟通记录和付款节点形成用户本人可核对的摘要。",
        evidence_mapping_draft="证据映射 draft metadata：材料、OCR 状态和来源追踪已建立映射，仍需人工确认。",
        timeline_draft="时间线 draft metadata：签署、履行、沟通、付款和争议形成时间节点草稿。",
        disputed_facts_draft="争议事实 draft metadata：履行范围、付款节点和通知义务仍需律师复核。",
        missing_facts_draft="缺失事实 draft metadata：需补充确认履行节点、对方反馈和付款凭证 metadata。",
        confidence_metadata={
            "overall": 0.82,
            "fact_summary": 0.84,
            "evidence_mapping": 0.8,
            "timeline": 0.78,
            "source_trace": 0.86,
        },
        preview_status="ai_draft_metadata_ready",
        created_at="2026-06-06T10:20:00Z",
        warnings=[
            "事实预览不是最终事实认定。",
            "可作为法律分析输入 metadata，但不会自动触发法律分析。",
        ],
    )


FACT_PREVIEWS: dict[str, FactPreviewRecord] = {
    "fact_preview_mock_001": _seed_preview(),
}


def list_fact_previews() -> FactPreviewList:
    previews = list(FACT_PREVIEWS.values())
    return FactPreviewList(
        fact_previews=previews,
        fact_preview_count=len(previews),
        warnings=["事实预览仅供用户本人核对、纠正和确认；不是最终事实认定。"],
    )


def get_fact_preview(fact_preview_id: str) -> FactPreviewRecord | None:
    return FACT_PREVIEWS.get(fact_preview_id)


def create_fact_preview(request: FactPreviewMockRequest) -> FactPreviewRecord:
    if get_case(request.case_id) is None:
        material_ids = request.material_ids or ["material_contract_metadata_001"]
    else:
        material_ids = request.material_ids or [material.material_id for material in list_materials(request.case_id)[:3]]
    source_trace_ids = [
        trace_id
        for material in list_materials(request.case_id)
        if material.material_id in material_ids
        for trace_id in material.source_trace_ids
    ]
    preview_id = f"fact_preview_{uuid4().hex[:12]}"
    preview = FactPreviewRecord(
        fact_preview_id=preview_id,
        case_id=request.case_id,
        material_ids=material_ids,
        ocr_job_ids=[f"ocr_status_{material_id}" for material_id in material_ids],
        source_trace_ids=source_trace_ids,
        confidence_metadata={
            "overall": 0.79,
            "fact_summary": 0.81,
            "evidence_mapping": 0.76,
            "timeline": 0.74,
            "source_trace": 0.83,
        },
        preview_status=(
            "owner_confirmed_fact_preview_metadata"
            if request.explicit_owner_confirmation
            else "ai_draft_metadata_ready"
        ),
        owner_confirmed=bool(request.explicit_owner_confirmation),
        created_at=_now(),
        warnings=[
            "mock fact preview metadata created.",
            "法律分析输入需用户本人确认；不会自动触发法律分析。",
        ],
    )
    FACT_PREVIEWS[preview_id] = preview
    return preview
