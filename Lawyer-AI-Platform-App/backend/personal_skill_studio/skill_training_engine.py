from personal_skill_studio.skill_sample_registry import build_skill_sample_registry
from personal_skill_studio.usage_meter import build_skill_training_usage_metadata


def build_skill_training_status() -> dict:
    registry = build_skill_sample_registry()
    return {
        "runtime_id": "skill_training_runtime",
        "display_name": "受控 Skill Training Runtime",
        "status": "draft_metadata_ready",
        "sample_count": len(registry["skill_candidate_metadata"]),
        "test_case_count": len(registry["test_case_metadata"]),
        "evaluation_count": len(registry["evaluation_metadata"]),
        "training_samples_desensitized": True,
        "manual_confirmation_required": True,
        "lawyer_review_required": True,
        "source_trace_required": True,
        "provider_gated": True,
        "mock_first": True,
        "dry_run_ready": True,
        "metadata_only": True,
        "draft_only": True,
        "live_call_executed": False,
        "used_in_ai_prompt": False,
        "raw_content_included": False,
        "final_skill_published": False,
        "auto_publish_enabled": False,
        "external_delivery_triggered": False,
        "usage_metadata": build_skill_training_usage_metadata(
            sample_count=len(registry["skill_candidate_metadata"]),
            test_case_count=len(registry["test_case_metadata"]),
        ),
        "warnings": [
            "Skill Training Runtime is controlled metadata only.",
            "No real training, AI prompt injection, final Skill publish, or external delivery is triggered.",
        ],
    }
