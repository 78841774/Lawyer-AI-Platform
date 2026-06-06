from personal_case_analysis.schemas import CaseAnalysisSafetyStatus


SAFETY_CHECKLIST = [
    "未结案件实战分析不产生训练数据",
    "训练阶段与实战阶段严格分离",
    "仅调用已有 Skill metadata",
    "不自动更新 Skill",
    "不自动发布 Skill",
    "不读取密钥值",
    "不读取真实未脱敏案件材料",
    "不展示原始正文",
    "不展示 raw OCR text",
    "不生成最终法律意见",
    "不生成最终报告",
    "法律分析草稿不等于最终法律意见",
    "法律分析草稿不等于正式报告",
    "不生成真实 PDF/DOCX",
    "不发送邮件",
    "不自动对外交付",
    "律师复核必需",
    "来源追踪必需",
    "evaluation / gate 仅作为质量评分参考",
]


SAFETY_FLAGS = {
    "open_case_runtime": True,
    "closed_case_training": False,
    "training_data_generated": False,
    "writes_to_training_set": False,
    "skill_updated": False,
    "skill_published": False,
    "source_trace_required": True,
    "audit_required": True,
    "lawyer_review_required": True,
    "legal_analysis_draft_only": True,
    "gate_reference_only": True,
    "blocks_next_stage": False,
    "raw_content_included": False,
    "raw_ocr_text_included": False,
    "raw_content_written_to_git": False,
    "raw_content_written_to_docs": False,
    "raw_content_written_to_diagnostics": False,
    "raw_content_written_to_regression_output": False,
    "ai_prompt_injected": False,
    "controlled_prompt_only": True,
    "api_key_accessed": False,
    "api_key_exposed": False,
    "final_fact_finding": False,
    "final_legal_opinion_generated": False,
    "final_report_generated": False,
    "public_link_created": False,
    "third_party_share_enabled": False,
    "client_auto_delivery": False,
    "external_delivery_triggered": False,
    "email_sent": False,
    "real_pdf_docx_generated": False,
}


def default_safety_flags() -> dict[str, bool]:
    return dict(SAFETY_FLAGS)


def build_safety_status() -> dict:
    return CaseAnalysisSafetyStatus(
        safety_checklist=SAFETY_CHECKLIST,
        safety_flags=default_safety_flags(),
        warnings=["v7.21 仅生成法律分析草稿 metadata，不产生训练数据，不生成最终法律意见或最终报告。"],
    ).model_dump()
