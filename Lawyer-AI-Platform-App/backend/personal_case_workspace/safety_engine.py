from personal_case_workspace.schemas import CaseWorkspaceSafetyStatus


SAFETY_CHECKLIST = [
    "未调用真实 provider",
    "未读取 API key",
    "未读取真实案件材料",
    "未返回 raw content",
    "未显示本地路径",
    "未生成最终法律意见",
    "未生成最终报告",
    "未生成真实 PDF/DOCX",
    "未发送邮件",
    "未自动对外交付",
    "用户本人访问必需",
    "来源追踪与审计必需",
]


def build_safety_status() -> CaseWorkspaceSafetyStatus:
    return CaseWorkspaceSafetyStatus(
        safety_checklist=SAFETY_CHECKLIST,
        safety_flags={
            "owner_only": True,
            "owner_access_required": True,
            "metadata_only": True,
            "draft_only": True,
            "provider_gated": True,
            "source_trace_required": True,
            "audit_required": True,
            "raw_content_returned": False,
            "local_path_visible": False,
            "api_key_exposed": False,
            "external_delivery_triggered": False,
            "email_sent": False,
        },
        warnings=["v7.18 仅加固个人案件与材料工作台 metadata，不接入真实材料读取。"],
    )


def build_fact_safety_status() -> CaseWorkspaceSafetyStatus:
    checklist = [
        "用户本人可查看事实预览",
        "用户本人可纠正事实",
        "用户本人可下载留存 metadata",
        "事实部分可作为法律分析输入",
        "不自动触发法律分析",
        "不自动训练未结案件",
        "不自动更新 Skill",
        "不自动发布 Skill",
        "不自动生成最终事实认定",
        "不自动生成最终法律意见",
        "不自动生成正式报告",
        "不自动对外交付",
    ]
    return CaseWorkspaceSafetyStatus(
        safety_checklist=checklist,
        safety_flags={
            "owner_only": True,
            "correction_allowed": True,
            "legal_analysis_input_allowed": True,
            "legal_analysis_auto_triggered": False,
            "training_data_generated": False,
            "writes_to_training_set": False,
            "skill_updated": False,
            "skill_published": False,
            "gate_reference_only": True,
            "blocks_next_stage": False,
            "final_fact_finding": False,
            "final_legal_opinion_generated": False,
            "final_report_generated": False,
            "public_link_created": False,
            "email_sent": False,
            "external_delivery_triggered": False,
        },
        warnings=["v7.20 事实预览与纠正只处理事实层，不进入法律分析 runtime。"],
    )
