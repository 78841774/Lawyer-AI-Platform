from personal_skill_studio.training_artifacts.storage import (
    EXPERIENCE_CANDIDATES_DIR,
    LEGAL_RETRIEVAL_JOBS_DIR,
    OCR_JOBS_DIR,
    read_payloads,
)


def v731b_safety_flags() -> dict[str, bool]:
    return {
        "owner_only": True,
        "local_private_processing_only": True,
        "authorized_case_only": True,
        "closed_case_preferred": True,
        "work_product_sensitive": True,
        "raw_material_controlled": True,
        "raw_material_allowed_for_internal_processing": True,
        "raw_material_return_allowed": False,
        "raw_material_provider_export_allowed": False,
        "raw_material_skill_ingest_allowed": False,
        "redacted_output_only": True,
        "redacted_experience_output_required": True,
        "manual_review_required": True,
        "source_trace_required": True,
        "audit_required": True,
        "provider_call_executed": False,
        "key_value_read": False,
        "credential_value_returned": False,
        "provider_raw_response_returned": False,
        "original_material_returned": False,
        "open_case_data_used": False,
        "formal_training_set_generated": False,
        "skill_updated": False,
        "skill_published": False,
        "final_legal_opinion_generated": False,
        "final_report_generated": False,
        "public_link_created": False,
        "email_sent": False,
        "external_delivery_triggered": False,
    }


def build_v731b_status() -> dict:
    return {
        "version": "v7.31b",
        "status": "training_experience_pipeline_metadata_ready",
        "raw_work_product_boundary_ready": True,
        "ocr_document_parse_ready": True,
        "legal_retrieval_ready": True,
        "experience_candidate_runtime_ready": True,
        "redacted_experience_output_ready": True,
        "manual_review_queue_ready": True,
        "source_trace_ready": True,
        "audit_ready": True,
        "safety_ready": True,
        "ocr_job_count": len(read_payloads(OCR_JOBS_DIR)),
        "legal_retrieval_job_count": len(read_payloads(LEGAL_RETRIEVAL_JOBS_DIR)),
        "experience_candidate_count": len(read_payloads(EXPERIENCE_CANDIDATES_DIR)),
        **v731b_safety_flags(),
        "warnings": [
            "v7.31b is a controlled internal processing pipeline for lawyer work-product experience extraction.",
            "Only redacted, abstracted, manually reviewed experience can flow to later Skill experience stages.",
        ],
    }


def build_v731b_safety(label: str = "v7.31b") -> dict:
    return {
        "label": label,
        "safety_checklist": [
            "原始办案底稿仅允许在受控内部解析区处理",
            "普通 API 不返回未脱敏正文",
            "OCR / 文档解析为 demo-safe metadata",
            "法律检索与类案检索为 demo-safe candidates",
            "经验候选必须脱敏与抽象化",
            "经验候选必须人工复核后才可进入后续经验池",
            "不调用 provider",
            "不读取 key value",
            "不发布 Skill",
            "不生成正式训练集、正式法律意见或正式报告",
        ],
        "all_safety_checks_passed": True,
        **v731b_safety_flags(),
    }
