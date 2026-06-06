from personal_production_pilot.schemas import PilotSafetyStatus


SAFETY_CHECKLIST = [
    "用户本人可查看和下载",
    "系统不自动外发",
    "系统不自动邮件",
    "系统不自动公开链接",
    "系统不自动上传第三方",
    "系统不自动交付客户",
    "系统不自动定性最终法律意见",
    "系统不自动定性正式报告",
    "未结案件不自动进入训练集",
    "未结案件不自动更新 Skill",
    "未结案件不自动发布 Skill",
    "raw content 不进入 Git/docs/diagnostics/regression",
    "API key 不读取、不显示、不写入",
    "source trace required",
    "lawyer review required",
    "provider gated",
    "audit required",
]


SAFETY_FLAGS = {
    "owner_only": True,
    "downloadable_by_owner_only": True,
    "internal_case_analysis": True,
    "draft_output_allowed": True,
    "pdf_docx_generation_allowed_for_owner": True,
    "public_link_created": False,
    "email_sent": False,
    "external_delivery_triggered": False,
    "third_party_share_enabled": False,
    "client_auto_delivery": False,
    "final_legal_opinion_auto_generated": False,
    "final_report_auto_generated": False,
    "training_data_generated": False,
    "writes_to_training_set": False,
    "skill_updated": False,
    "skill_published": False,
    "source_trace_required": True,
    "lawyer_review_required": True,
    "final_lock_required": True,
    "provider_gated": True,
    "api_key_exposed": False,
    "raw_content_written_to_git": False,
    "raw_content_written_to_docs": False,
    "raw_content_written_to_diagnostics": False,
    "raw_content_written_to_regression_output": False,
}


def default_safety_flags() -> dict[str, bool]:
    return dict(SAFETY_FLAGS)


def build_safety_status() -> dict:
    return PilotSafetyStatus(
        safety_checklist=SAFETY_CHECKLIST,
        safety_flags=default_safety_flags(),
        warnings=["v7.17 pilot supports owner-only download metadata; no public link, email, external delivery, final legal opinion, or final report is auto-generated."],
    ).model_dump()
