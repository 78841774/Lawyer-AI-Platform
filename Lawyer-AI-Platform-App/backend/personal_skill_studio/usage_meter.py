def build_skill_training_usage_metadata(*, sample_count: int = 0, test_case_count: int = 0) -> dict:
    return {
        "sample_count": sample_count,
        "test_case_count": test_case_count,
        "live_call_executed": False,
        "used_in_ai_prompt": False,
        "metadata_only": True,
        "draft_only": True,
        "final_skill_published": False,
        "source_trace_required": True,
        "lawyer_review_required": True,
    }
