from personal_material_runtime.schemas import PersonalMaterialLiveRunRecord


def sanitize_live_run(record: PersonalMaterialLiveRunRecord) -> PersonalMaterialLiveRunRecord:
    return record.model_copy(
        update={
            "live_call_executed": False,
            "api_key_exposed": False,
            "raw_content_exposed": False,
            "raw_ocr_text_exposed": False,
            "ai_prompt_injected": False,
            "fact_extraction_triggered": False,
            "legal_analysis_triggered": False,
            "final_legal_opinion_generated": False,
            "final_report_generated": False,
            "external_delivery_triggered": False,
            "source_trace_required": True,
            "lawyer_review_required": True,
            "review_required": True,
        }
    )
