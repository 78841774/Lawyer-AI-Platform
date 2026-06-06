from datetime import datetime, timezone
from uuid import uuid4

from personal_case_workspace.fact_preview_engine import get_fact_preview
from personal_case_workspace.schemas import FactVersionList, FactVersionMockRequest, FactVersionRecord


def _now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


FACT_VERSIONS: dict[str, FactVersionRecord] = {
    "fact_version_ai_draft_001": FactVersionRecord(
        version_id="fact_version_ai_draft_001",
        fact_preview_id="fact_preview_mock_001",
        version_number=1,
        version_type="ai_draft_version",
        created_from="ai_draft_metadata",
        change_summary="AI 草稿事实预览 metadata。",
        created_at="2026-06-06T10:20:00Z",
        warnings=["AI 草稿版本不是最终事实认定。"],
    ),
    "fact_version_owner_corrected_001": FactVersionRecord(
        version_id="fact_version_owner_corrected_001",
        fact_preview_id="fact_preview_mock_001",
        version_number=2,
        version_type="owner_corrected_version",
        created_from="owner_correction",
        change_summary="用户本人纠正时间线与来源追踪 metadata。",
        owner_confirmed=True,
        created_at="2026-06-06T10:28:00Z",
        warnings=["纠正版本不进入训练集，不更新 Skill。"],
    ),
    "fact_version_owner_confirmed_001": FactVersionRecord(
        version_id="fact_version_owner_confirmed_001",
        fact_preview_id="fact_preview_mock_001",
        version_number=3,
        version_type="owner_confirmed_version",
        created_from="owner_confirmation",
        change_summary="用户本人确认可作为法律分析输入 metadata。",
        owner_confirmed=True,
        legal_analysis_input_ready=True,
        created_at="2026-06-06T10:32:00Z",
        warnings=["ready 状态不自动触发法律分析。"],
    ),
}


def list_fact_versions(fact_preview_id: str) -> FactVersionList | None:
    if get_fact_preview(fact_preview_id) is None:
        return None
    versions = [record for record in FACT_VERSIONS.values() if record.fact_preview_id == fact_preview_id]
    versions.sort(key=lambda record: record.version_number)
    return FactVersionList(
        fact_preview_id=fact_preview_id,
        versions=versions,
        version_count=len(versions),
        warnings=["版本历史区分 AI 草稿、用户纠正和用户确认版本。"],
    )


def create_fact_version(fact_preview_id: str, request: FactVersionMockRequest) -> FactVersionRecord | None:
    if get_fact_preview(fact_preview_id) is None:
        return None
    existing = [record for record in FACT_VERSIONS.values() if record.fact_preview_id == fact_preview_id]
    version_number = max([record.version_number for record in existing], default=0) + 1
    version_type = "owner_confirmed_version" if request.explicit_owner_confirmation else "owner_corrected_version"
    version = FactVersionRecord(
        version_id=f"fact_version_{uuid4().hex[:12]}",
        fact_preview_id=fact_preview_id,
        version_number=version_number,
        version_type=version_type,
        created_from=request.created_from,
        change_summary="owner fact version metadata created",
        owner_confirmed=bool(request.explicit_owner_confirmation),
        legal_analysis_input_ready=bool(request.explicit_owner_confirmation),
        created_at=_now(),
        warnings=[
            "事实版本仅服务当前案件。",
            "不会自动进入训练集、更新 Skill 或触发法律分析。",
        ],
    )
    FACT_VERSIONS[version.version_id] = version
    return version
