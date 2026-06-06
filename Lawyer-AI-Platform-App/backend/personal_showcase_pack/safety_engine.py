from personal_showcase_pack.schemas import ShowcaseSafetyStatus


FORBIDDEN_METADATA_PATTERNS = [
    "/Users",
    "/Volumes",
    "C:\\",
    "storage/runtime",
    "local.db",
    ".env",
    "sk-",
    "真实客户姓名",
    "真实案件名称",
    "真实判决原文",
]


def default_safety_flags() -> dict[str, bool]:
    return {
        "real_provider_called": False,
        "api_key_accessed": False,
        "real_case_data_included": False,
        "raw_content_included": False,
        "raw_content_returned": False,
        "final_legal_opinion_generated": False,
        "final_report_generated": False,
        "external_delivery_triggered": False,
        "email_sent": False,
        "final_file_generated": False,
        "requires_lawyer_review": True,
        "final_lock_required": True,
        "source_trace_required": True,
        "mock_metadata_only": True,
        "synthetic_demo_only": True,
    }


def build_safety_status() -> dict:
    checklist = [
        "未调用真实 provider",
        "未读取密钥值",
        "未读取真实案件材料",
        "未返回原始内容",
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
    return ShowcaseSafetyStatus(
        safety_checklist=checklist,
        safety_flags=default_safety_flags(),
        warnings=["v7.7 展示包仅使用 synthetic mock metadata，不包含真实客户、案件、材料或企业信息。"],
    ).model_dump()


def validate_mock_metadata_text(value: str, field_name: str) -> list[str]:
    blocked = []
    normalized = value.strip()
    if not normalized:
        blocked.append(f"{field_name} 不能为空")
        return blocked
    for pattern in FORBIDDEN_METADATA_PATTERNS:
        if pattern.lower() in normalized.lower():
            blocked.append(f"{field_name} 包含不允许进入展示 metadata 的敏感模式")
            break
    return blocked
