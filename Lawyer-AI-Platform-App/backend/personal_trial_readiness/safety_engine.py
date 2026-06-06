from personal_trial_readiness.schemas import TrialReadinessStatus, TrialSafetyStatus


SAFETY_ITEMS = [
    "仅记录试运行 metadata",
    "未读取案件原始内容",
    "未调用真实 provider",
    "未读取 API key",
    "未生成最终法律意见",
    "未生成最终报告",
    "未训练未结案件",
    "未自动发布 Skill",
    "未创建公开链接",
    "未发送邮件",
    "未自动对外交付",
    "Developer Diagnostics 默认折叠且不含 raw content",
]


def build_status() -> dict:
    return TrialReadinessStatus(
        warnings=[
            "v7.25 仅准备个人版实战案件试运行 metadata。",
            "问题记录和质量评分只用于优化参考，不阻断下一步。",
        ]
    ).model_dump()


def build_safety_status() -> dict:
    return TrialSafetyStatus(safety_items=SAFETY_ITEMS, safety_item_count=len(SAFETY_ITEMS)).model_dump()
