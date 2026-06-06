from datetime import datetime, timezone
from uuid import uuid4

from personal_case_workspace.fact_preview_engine import get_fact_preview
from personal_case_workspace.schemas import (
    FactCorrectionList,
    FactCorrectionMockRequestV20,
    FactCorrectionRecord,
)


def _now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


FACT_CORRECTIONS: dict[str, FactCorrectionRecord] = {
    "fact_correction_mock_001": FactCorrectionRecord(
        correction_id="fact_correction_mock_001",
        fact_preview_id="fact_preview_mock_001",
        corrected_sections=["timeline_correction", "source_trace_correction"],
        correction_reason="用户本人补充时间线与来源追踪 metadata。",
        correction_type="timeline_correction",
        created_at="2026-06-06T10:26:00Z",
        updated_at="2026-06-06T10:26:00Z",
        warnings=["纠正稿仅属于当前案件，不进入训练集、不更新 Skill。"],
    )
}


def create_fact_correction_v20(fact_preview_id: str, request: FactCorrectionMockRequestV20) -> FactCorrectionRecord | None:
    if get_fact_preview(fact_preview_id) is None:
        return None
    confirmed = (
        request.explicit_owner_confirmation
        and request.explicit_no_training_data_confirmation
        and request.explicit_no_skill_update_confirmation
        and request.explicit_no_auto_legal_analysis_confirmation
    )
    correction_id = f"fact_correction_{uuid4().hex[:12]}"
    now = _now()
    record = FactCorrectionRecord(
        correction_id=correction_id,
        fact_preview_id=fact_preview_id,
        corrected_sections=request.corrected_sections,
        correction_reason="owner correction metadata accepted",
        correction_type=request.correction_type,
        correction_status="owner_correction_metadata_created" if confirmed else "blocked_until_owner_confirmations",
        created_at=now,
        updated_at=now,
        warnings=[
            "纠正内容只属于当前案件。",
            "不自动进入训练集，不自动更新或发布 Skill，不自动触发法律分析。",
        ],
    )
    FACT_CORRECTIONS[correction_id] = record
    return record


def list_fact_corrections(fact_preview_id: str) -> FactCorrectionList | None:
    if get_fact_preview(fact_preview_id) is None:
        return None
    corrections = [record for record in FACT_CORRECTIONS.values() if record.fact_preview_id == fact_preview_id]
    return FactCorrectionList(
        fact_preview_id=fact_preview_id,
        corrections=corrections,
        correction_count=len(corrections),
        warnings=["纠正历史只展示 metadata；不显示 raw content 或本地路径。"],
    )


def get_fact_correction(correction_id: str) -> FactCorrectionRecord | None:
    return FACT_CORRECTIONS.get(correction_id)
