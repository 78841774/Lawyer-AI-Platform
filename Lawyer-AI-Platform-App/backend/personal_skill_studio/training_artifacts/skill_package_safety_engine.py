from personal_skill_studio.training_artifacts.storage import SKILL_PACKAGES_DIR, read_payloads


def v731d_safety_flags() -> dict[str, bool | str]:
    return {
        "owner_only": True,
        "local_private_processing_only": True,
        "approved_experience_only": True,
        "redacted_output_only": True,
        "abstracted_experience_only": True,
        "system_validation_required": True,
        "system_validation_only": True,
        "final_review_status": "not_applicable",
        "practice_load_review_required_later": True,
        "source_trace_required": True,
        "audit_required": True,
        "provider_call_executed": False,
        "key_value_read": False,
        "credential_value_returned": False,
        "provider_result_payload_returned": False,
        "source_content_returned": False,
        "source_material_returned": False,
        "unreviewed_experience_packaged": False,
        "unsafe_experience_packaged": False,
        "missing_source_trace_packaged": False,
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


def build_v731d_status() -> dict:
    packages = read_payloads(SKILL_PACKAGES_DIR)
    return {
        "version": "v7.31d",
        "status": "skill_package_versioning_system_validation_metadata_ready",
        "skill_package_registry_ready": True,
        "skill_package_builder_ready": True,
        "manifest_ready": True,
        "source_trace_bundle_ready": True,
        "audit_bundle_ready": True,
        "system_validation_gate_ready": True,
        "package_count": len(packages),
        "system_validated_count": sum(
            1 for package in packages if package.get("pre_publish_gate_status") == "system_validated"
        ),
        **v731d_safety_flags(),
        "warnings": [
            "v7.31d packages confirmed draft metadata only.",
            "Training output manual review is not applicable; practice load review is deferred to v7.31f.",
        ],
    }
