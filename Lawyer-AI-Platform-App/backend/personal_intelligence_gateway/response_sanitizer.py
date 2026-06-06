from personal_intelligence_gateway.schemas import PersonalIntelligenceLiveRunRecord


def sanitize_live_run(record: PersonalIntelligenceLiveRunRecord) -> PersonalIntelligenceLiveRunRecord:
    return record.model_copy(
        update={
            "live_call_executed": False,
            "api_key_exposed": False,
            "raw_content_exposed": False,
            "legal_raw_content_exposed": False,
            "enterprise_raw_content_exposed": False,
            "ai_prompt_injected": False,
            "fact_extraction_triggered": False,
            "legal_analysis_triggered": False,
            "citation_finalized": False,
            "final_legal_opinion_generated": False,
            "final_report_generated": False,
            "external_delivery_triggered": False,
            "source_trace_required": True,
            "lawyer_review_required": True,
            "review_required": True,
        }
    )
