from personal_owner_output_center.schemas import OwnerOutputSafetyStatus


SAFETY_ITEMS = [
    "仅用户本人查看和下载",
    "全部输出保持草稿或 metadata",
    "不创建公开链接",
    "不发送邮件",
    "不自动对外交付",
    "不自动标记最终法律意见",
    "不自动标记正式律师报告",
    "不自动发布 Skill",
    "不写入训练集",
    "质量评分仅作参考",
    "门控不阻断下载",
    "来源追踪与审计必需",
]


def build_safety_status() -> dict:
    return OwnerOutputSafetyStatus(
        safety_checklist=SAFETY_ITEMS,
        safety_item_count=len(SAFETY_ITEMS),
        warnings=["Safety status is metadata-only and does not expose raw content or provider credentials."],
    ).model_dump()
