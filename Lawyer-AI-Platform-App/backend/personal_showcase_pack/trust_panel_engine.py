from datetime import datetime, timezone

from personal_showcase_pack.audit_engine import record_audit_event
from personal_showcase_pack.safety_engine import default_safety_flags
from personal_showcase_pack.schemas import TrustPanel


def build_trust_panel() -> dict:
    now = datetime.now(timezone.utc).isoformat()
    record_audit_event(action="trust_panel_viewed", actor="system", object_type="trust_panel", object_id="default", timestamp=now)
    trust_items = [
        "未调用真实 provider",
        "未读取 API key",
        "未读取真实案件材料",
        "未生成最终法律意见",
        "未生成最终报告",
        "未自动对外交付",
        "未发送邮件",
        "未生成真实 PDF/DOCX",
        "律师复核必需",
        "最终锁定必需",
        "来源追踪必需",
        "当前仅为 mock metadata 展示",
    ]
    return TrustPanel(
        trust_items=trust_items,
        flags=default_safety_flags(),
        warnings=["安全与信任面板仅展示 v7.7 mock metadata 边界。"],
    ).model_dump()
