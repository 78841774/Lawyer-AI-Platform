from personal_delivery_packet.schemas import DeliveryPacketSafetyStatus


def default_safety_flags() -> dict[str, bool]:
    return {
        "raw_case_content_read": False,
        "live_provider_call_executed": False,
        "api_key_accessed": False,
        "final_legal_opinion_generated": False,
        "final_report_generated": False,
        "external_delivery_triggered": False,
        "email_sent": False,
        "final_file_generated": False,
        "requires_lawyer_review": True,
        "final_lock_required": True,
        "source_trace_required": True,
        "mock_metadata_only": True,
    }


def build_safety_status() -> dict:
    return DeliveryPacketSafetyStatus(
        safety_checklist=[
            "未读取案件正文",
            "未调用真实 provider",
            "未读取密钥值",
            "未生成最终法律意见",
            "未生成最终报告",
            "未自动对外交付",
            "未发送邮件",
            "未生成真实最终交付文件",
            "律师复核必需",
            "最终锁定必需",
            "来源追踪必需",
            "仅返回交付包 metadata",
        ],
        safety_flags=default_safety_flags(),
        warnings=["v7.6 仅提供交付包 metadata 骨架，不触发真实导出或对外交付。"],
    ).model_dump()
