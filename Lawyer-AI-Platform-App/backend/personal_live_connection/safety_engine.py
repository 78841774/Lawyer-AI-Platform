from personal_live_connection.schemas import LiveConnectionSafetyStatus


SAFETY_ITEMS = [
    "provider-gated",
    "live disabled by default",
    "dry-run 默认 true",
    "key_loaded boolean only",
    "metadata-only",
    "draft-only",
    "owner-only",
    "lawyer-review-required",
    "source-trace-required",
    "不生成最终法律意见",
    "不生成最终报告",
    "不生成真实 PDF/DOCX",
    "不发送邮件",
    "不创建公开链接",
    "不自动对外交付或发布 Skill",
    "不显示 raw content / local path / secret",
]


def build_safety_status() -> dict:
    return LiveConnectionSafetyStatus(
        safety_items=SAFETY_ITEMS,
        safety_item_count=len(SAFETY_ITEMS),
        warnings=["v7.28 unified live connection remains dry-run and metadata-only by default."],
    ).model_dump()

