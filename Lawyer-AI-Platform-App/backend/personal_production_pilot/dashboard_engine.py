from typing import Any


SAFETY_ITEMS = [
    "未调用真实 provider",
    "未读取密钥值",
    "未读取真实案件材料",
    "仅返回 metadata",
    "输出仍为 draft",
    "下载仅限 owner-only",
    "未创建公开链接",
    "未发送邮件",
    "未自动对外交付",
    "未生成最终法律意见",
    "未生成最终报告",
    "来源追踪 / 律师复核 / 审计必需",
]


BASE_FLAGS: dict[str, Any] = {
    "owner_only": True,
    "owner_access_required": True,
    "downloadable_by_owner_only": True,
    "metadata_only": True,
    "draft_only": True,
    "provider_gated": True,
    "dry_run_default": True,
    "source_trace_required": True,
    "lawyer_review_required": True,
    "audit_required": True,
    "public_link_created": False,
    "email_sent": False,
    "external_delivery_triggered": False,
    "third_party_share_enabled": False,
    "client_auto_delivery": False,
    "final_legal_opinion_auto_generated": False,
    "final_report_auto_generated": False,
    "real_pdf_docx_generated": False,
    "training_data_generated": False,
    "writes_to_training_set": False,
    "skill_updated": False,
    "skill_published": False,
    "api_key_exposed": False,
    "raw_content_returned": False,
    "raw_content_written_to_git": False,
    "raw_content_written_to_docs": False,
    "raw_content_written_to_diagnostics": False,
    "raw_content_written_to_regression_output": False,
    "local_path_visible": False,
}


def _with_flags(payload: dict[str, Any]) -> dict[str, Any]:
    return {**BASE_FLAGS, **payload}


def build_dashboard_status() -> dict[str, Any]:
    return _with_flags(
        {
            "enabled": True,
            "mode": "personal_production_pilot_dashboard",
            "version": "v7.19",
            "runtime_label": "个人生产 Pilot Dashboard 增强",
            "dashboard_ready": True,
            "workflow_overview_ready": True,
            "quality_score_panels_ready": True,
            "optimization_suggestions_ready": True,
            "export_boundary_visible": True,
            "warnings": [
                "v7.19 仅增强个人生产 Pilot dashboard metadata 展示。",
                "评分、门控与优化建议为 synthetic mock metadata，不代表真实案件结论。",
            ],
        }
    )


def build_dashboard_metrics() -> dict[str, Any]:
    return _with_flags(
        {
            "runtime_readiness": {
                "ai_gateway": "mock_ready_live_disabled",
                "ocr_document_gateway": "mock_ready_live_disabled",
                "legal_enterprise_gateway": "mock_ready_live_disabled",
                "skill_training_runtime": "draft_metadata_ready",
                "case_analysis_runtime": "draft_metadata_ready",
                "delivery_packet_runtime": "metadata_ready",
                "case_workspace_runtime": "owner_only_metadata_ready",
                "owner_output_center_runtime": "owner_only_download_metadata_ready",
            },
            "workflow_status": [
                {"step": "材料工作台", "status": "owner_only_metadata"},
                {"step": "受控案件分析", "status": "draft_only"},
                {"step": "Skill 草案", "status": "draft_metadata"},
                {"step": "交付包草案", "status": "metadata_only"},
                {"step": "Owner 下载", "status": "gated_dry_run"},
                {"step": "产出下载中心", "status": "owner_only_metadata"},
            ],
            "review_queue": {"pending_count": 3, "low_confidence_count": 1, "revision_required_count": 2},
            "source_trace_summary": {"total": 14, "confirmed": 9, "unconfirmed": 5, "raw_content_returned": False},
            "export_boundary": {
                "owner_download_ready": True,
                "public_link_created": False,
                "email_sent": False,
                "external_delivery_triggered": False,
                "real_pdf_docx_generated": False,
                "owner_output_center_ready": True,
                "public_link_disabled": True,
                "email_sending_disabled": True,
                "external_delivery_disabled": True,
            },
            "warnings": ["metrics 为 dashboard 展示 metadata，不触发真实 provider、训练或交付。"],
        }
    )


def build_quality_items() -> dict[str, Any]:
    items = [
        {
            "output_id": "skill_final_draft_fact_extraction",
            "output_type": "skill_final_draft",
            "title": "事实提炼 Skill 草案",
            "quality_score": 86,
            "score_label": "较高，但仍需律师复核",
            "gate_status": "reference_pass",
            "gate_reference_only": True,
            "blocks_next_stage": False,
            "optimization_suggestions": ["补齐争议事实映射", "标注未确认来源", "保持样本脱敏后再进入训练评估"],
        },
        {
            "output_id": "skill_final_draft_legal_analysis",
            "output_type": "skill_final_draft",
            "title": "法律分析 Skill 草案",
            "quality_score": 81,
            "score_label": "可演示，需补充法律依据候选来源",
            "gate_status": "revision_recommended",
            "gate_reference_only": True,
            "blocks_next_stage": False,
            "optimization_suggestions": ["增加 Source Trace 候选", "分离事实判断与法律适用草稿", "避免最终法律意见措辞"],
        },
        {
            "output_id": "case_analysis_draft_open_case",
            "output_type": "case_analysis_draft",
            "title": "未结案件分析草稿 metadata",
            "quality_score": 78,
            "score_label": "可进入复核，不可标记最终",
            "gate_status": "lawyer_review_required",
            "gate_reference_only": True,
            "blocks_next_stage": False,
            "optimization_suggestions": ["补强事实时间线", "将低置信度结论移入复核队列", "确认所有引用均有 source trace"],
        },
    ]
    return _with_flags(
        {
            "quality_items": [_with_flags(item) for item in items],
            "item_count": len(items),
            "average_quality_score": round(sum(item["quality_score"] for item in items) / len(items), 1),
            "quality_gate_status": "reference_only_not_blocking",
            "warnings": ["评分仅用于本地 pilot dashboard 参考，不构成法律结论或最终报告质量承诺。"],
        }
    )


def build_dashboard_safety() -> dict[str, Any]:
    return _with_flags(
        {
            "safety_checklist": SAFETY_ITEMS,
            "safety_item_count": len(SAFETY_ITEMS),
            "all_safety_checks_passed": True,
            "warnings": ["Trust / Safety Panel 统一 12 项展示；Developer Diagnostics 必须默认折叠。"],
        }
    )
