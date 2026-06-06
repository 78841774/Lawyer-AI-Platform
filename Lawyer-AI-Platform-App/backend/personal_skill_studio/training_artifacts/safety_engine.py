from personal_skill_studio.training_artifacts.schemas import safety_flags


SAFETY_CHECKLIST = [
    "仅加载合成训练产物 metadata",
    "Codex 训练不等于模型微调",
    "只允许脱敏闭案样本 metadata",
    "未结案件不得进入训练产物",
    "不读取真实案件正文",
    "不读取 OCR 原文",
    "不读取或返回密钥值",
    "不调用真实 provider",
    "不写训练集",
    "不更新 Skill",
    "不自动发布 Skill",
    "不生成最终法律意见",
    "不生成正式报告",
    "不创建公开链接",
    "不发送邮件",
    "不自动对外交付",
    "案由匹配与 fallback 仅 dry-run",
    "Gate 仅作为参考",
]


def build_safety() -> dict:
    return {
        "safety_checklist": SAFETY_CHECKLIST,
        "safety": safety_flags(),
        "all_safety_checks_passed": True,
        **safety_flags(),
        "warnings": ["v7.30 training artifact loader is metadata-only and dry-run by default."],
    }

