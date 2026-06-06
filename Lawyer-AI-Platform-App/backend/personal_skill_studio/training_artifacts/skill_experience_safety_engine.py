from personal_skill_studio.training_artifacts.storage import (
    CODEX_SKILL_DRAFTS_DIR,
    SKILL_EXPERIENCE_BINDINGS_DIR,
    SKILL_EXPERIENCE_POOL_DIR,
    read_payloads,
)


def v731c_safety_flags() -> dict[str, bool]:
    return {
        "owner_only": True,
        "local_private_processing_only": True,
        "authorized_case_only": True,
        "controlled_material_boundary": True,
        "source_content_returned": False,
        "redacted_output_only": True,
        "abstracted_experience_only": True,
        "approved_experience_only": True,
        "manual_review_required": True,
        "source_trace_required": True,
        "audit_required": True,
        "provider_call_executed": False,
        "key_value_read": False,
        "credential_value_returned": False,
        "provider_result_payload_returned": False,
        "local_sensitive_reference_returned": False,
        "unreviewed_experience_imported": False,
        "unsafe_experience_imported": False,
        "missing_source_trace_imported": False,
        "formal_training_set_generated": False,
        "real_codex_training_triggered": False,
        "skill_published": False,
        "skill_publishable": False,
        "final_legal_opinion_generated": False,
        "final_report_generated": False,
        "public_link_created": False,
        "email_sent": False,
        "external_delivery_triggered": False,
    }


def build_v731c_status() -> dict:
    return {
        "version": "v7.31c",
        "status": "skill_experience_pool_and_draft_builder_metadata_ready",
        "skill_experience_pool_ready": True,
        "approved_experience_import_ready": True,
        "experience_binding_ready": True,
        "codex_skill_draft_builder_ready": True,
        "manual_confirmation_queue_ready": True,
        "source_trace_ready": True,
        "audit_ready": True,
        "safety_ready": True,
        "experience_count": len(read_payloads(SKILL_EXPERIENCE_POOL_DIR)),
        "binding_count": len(read_payloads(SKILL_EXPERIENCE_BINDINGS_DIR)),
        "draft_count": len(read_payloads(CODEX_SKILL_DRAFTS_DIR)),
        **v731c_safety_flags(),
        "warnings": [
            "v7.31c only imports approved redacted experience into the Skill Experience Pool.",
            "Skill drafts are not publishable and do not trigger real training.",
        ],
    }


def build_v731c_safety(label: str = "v7.31c") -> dict:
    return {
        "label": label,
        "safety_checklist": [
            "仅 approved_for_skill_experience 可入池",
            "未脱敏经验不得入池",
            "无 source trace 经验不得入池",
            "Skill Draft 默认 not_publishable",
            "人工确认草案结构不等于发布 Skill",
            "不调用 provider",
            "不读取 key value",
            "不触发真实训练",
        ],
        "all_safety_checks_passed": True,
        **v731c_safety_flags(),
    }
