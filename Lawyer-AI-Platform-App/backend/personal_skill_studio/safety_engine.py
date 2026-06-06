from personal_skill_studio.schemas import SkillStudioSafetyStatus


SAFETY_CHECKLIST = [
    "未读取案件正文",
    "未调用真实 AI provider",
    "未生成最终法律意见",
    "未生成最终报告",
    "未自动发布 Skill",
    "训练样本必须脱敏",
    "训练样本必须人工确认",
    "Skill 输出仅为 draft metadata",
    "未触发 AI Prompt",
    "未写入正式 Skill Registry",
    "律师复核必需",
    "人工确认必需",
    "来源追踪必需",
    "仅生成经验包草案和技能候选草案",
    "两个 Skill 最终稿仅用户本人下载",
    "不自动训练未结案件",
    "门控仅作为质量评分与优化方向",
]

SAFETY_FLAGS = {
    "raw_case_content_read": False,
    "live_ai_call_executed": False,
    "final_legal_opinion_generated": False,
    "final_report_generated": False,
    "auto_publish_enabled": False,
    "published_to_registry": False,
    "final_skill_published": False,
    "training_samples_desensitized": True,
    "training_samples_manual_confirmed": True,
    "used_in_ai_prompt": False,
    "metadata_only": True,
    "draft_only": True,
    "requires_lawyer_review": True,
    "requires_manual_confirmation": True,
    "source_trace_required": True,
    "audit_required": True,
    "mock_metadata_only": True,
    "owner_only": True,
    "downloadable_by_owner_only": True,
    "gate_reference_only": True,
    "blocks_next_stage": False,
    "quality_reference_only": True,
    "skill_auto_published": False,
    "training_data_generated": False,
    "writes_to_training_set": False,
    "open_case_data_used": False,
    "unresolved_case_data_used": False,
    "public_link_created": False,
    "email_sent": False,
    "external_delivery_triggered": False,
    "third_party_share_enabled": False,
    "client_auto_delivery": False,
    "api_key_exposed": False,
    "raw_content_written_to_git": False,
    "raw_content_written_to_docs": False,
    "raw_content_written_to_diagnostics": False,
    "raw_content_written_to_regression_output": False,
}


def default_safety_flags() -> dict[str, bool]:
    return dict(SAFETY_FLAGS)


def build_safety_status() -> dict:
    return SkillStudioSafetyStatus(
        safety_checklist=SAFETY_CHECKLIST,
        safety_flags=default_safety_flags(),
        warnings=["v7.22 仅生成受控 Skill Training 与 Skill Final Draft metadata，不读取原文、不触发 AI Prompt、不自动发布 Skill。"],
    ).model_dump()


def build_final_drafts_safety_status() -> dict:
    return SkillStudioSafetyStatus(
        safety_checklist=[
            "基于已有 Skill 和配套材料 metadata",
            "不凭空重写 Skill",
            "不覆盖旧 Skill",
            "不自动发布 Skill",
            "不自动训练未结案件",
            "不写入训练集",
            "仅用户本人下载",
            "不创建公开链接",
            "不发送邮件",
            "不自动对外交付",
            "不生成最终法律意见",
            "不生成正式报告",
            "不暴露密钥值、原始正文或本地路径",
            "Gate 仅作为质量评分与优化方向",
        ],
        safety_flags=default_safety_flags(),
        warnings=["Skill Final Draft safety is metadata-only, owner-only, and draft-only."],
    ).model_dump()
