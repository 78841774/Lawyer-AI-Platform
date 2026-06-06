from personal_ai_gateway.provider_config import list_live_provider_configs
from personal_intelligence_gateway.provider_config import list_live_provider_configs as list_intelligence_live_provider_configs
from personal_material_runtime.provider_config import list_live_provider_configs as list_material_live_provider_configs
from personal_production.schemas import (
    PersonalProductionProviderCapabilities,
    PersonalProductionProviderCapability,
)
from personal_case_analysis.skill_loader import build_skill_baseline_report


PROVIDER_DEFINITIONS = [
    ("openai_provider", "OpenAI / GPT Provider", "ai_model", "ai_gateway_registered_mock_first", "/personal-ai-gateway", True),
    ("deepseek_provider", "DeepSeek Provider", "ai_model", "ai_gateway_registered_mock_first", "/personal-ai-gateway", True),
    ("local_model_provider", "Local Model Provider", "ai_model", "ai_gateway_registered_mock_first", "/personal-ai-gateway", True),
    ("mineru_file_parser_provider", "MinerU File Parser", "file_parser", "material_runtime_registered_mock_first", "/personal-material-runtime", True),
    ("docling_file_parser_provider", "Docling File Parser", "file_parser", "material_runtime_registered_mock_first", "/personal-material-runtime", True),
    ("paddleocr_provider", "PaddleOCR / Baidu AI Studio", "ocr", "material_runtime_registered_mock_first", "/personal-material-runtime", True),
    ("ocr_provider", "OCR Provider", "ocr", "paddleocr_placeholder_registered_in_v7_2", "/personal-material-runtime", True),
    ("kuaicha365_lawskills_provider", "快查 365 LawSkills", "legal_search", "personal_intelligence_gateway_registered_mock_first", "/personal-intelligence", True),
    ("tianyancha_ai_provider", "天眼查 AI", "enterprise_intelligence", "personal_intelligence_gateway_registered_mock_first", "/personal-intelligence", True),
    ("qichacha_provider_placeholder", "企查查 Placeholder", "enterprise_intelligence", "reserved_optional_provider_placeholder", "/personal-intelligence", True),
    ("pkulaw_provider_placeholder", "北大法宝 Placeholder", "legal_search", "reserved_optional_provider_placeholder", "/personal-intelligence", True),
    ("national_law_database_provider_placeholder", "国家法律法规数据库 Placeholder", "legal_search", "reserved_optional_provider_placeholder", "/personal-intelligence", True),
    ("skill_training_provider", "Skill Training Provider", "skill_training", "skill_studio_registered_mock_first", "/personal-skill-studio", True),
    ("training_artifact_loader_provider", "Codex Training Artifact Loader", "skill_training", "training_artifact_loader_metadata_ready", "/personal-skill-studio/training-artifacts", True),
    ("codex_training_run_provider", "Closed Case Codex Training Run", "skill_training", "codex_training_run_metadata_ready", "/personal-skill-studio/training-artifacts", True),
    ("real_closed_case_training_intake_provider", "Real Closed-Case Training Intake", "skill_training", "real_closed_case_training_intake_metadata_ready", "/personal-skill-studio/training-artifacts", True),
    ("training_experience_pipeline_provider", "Controlled Training Experience Pipeline", "skill_training", "training_experience_pipeline_metadata_ready", "/personal-skill-studio/training-artifacts", True),
    ("codex_skill_draft_builder_provider", "Skill Experience Pool & Codex Skill Draft Builder", "skill_training", "codex_skill_draft_builder_metadata_ready", "/personal-skill-studio/training-artifacts", True),
]


def build_provider_capabilities() -> dict:
    live_config = list_live_provider_configs()
    material_live_config = list_material_live_provider_configs()
    intelligence_live_config = list_intelligence_live_provider_configs()
    case_analysis_baselines = build_skill_baseline_report()
    key_loaded_by_provider = {provider["provider_id"]: provider["key_loaded"] for provider in live_config["providers"]}
    live_enabled_by_provider = {provider["provider_id"]: provider["live_enabled"] for provider in live_config["providers"]}
    material_key_loaded_by_provider = {
        provider["provider_id"]: provider["key_loaded"] for provider in material_live_config["providers"]
    }
    material_live_enabled_by_provider = {
        provider["provider_id"]: provider["live_enabled"] for provider in material_live_config["providers"]
    }
    intelligence_key_loaded_by_provider = {
        provider["provider_id"]: provider["key_loaded"] for provider in intelligence_live_config["providers"]
    }
    intelligence_live_enabled_by_provider = {
        provider["provider_id"]: provider["live_enabled"] for provider in intelligence_live_config["providers"]
    }
    providers = [
        PersonalProductionProviderCapability(
            provider_id=provider_id,
            label=label,
            category=category,
            next_action=next_action,
            target_route=target_route,
            gateway_registered=gateway_registered,
            live_enabled=bool(
                live_enabled_by_provider.get(provider_id.replace("_provider", ""), False)
                or material_live_enabled_by_provider.get(_material_live_provider_id(provider_id), False)
                or intelligence_live_enabled_by_provider.get(provider_id, False)
            ),
            api_key_present=bool(
                key_loaded_by_provider.get(provider_id.replace("_provider", ""), False)
                or material_key_loaded_by_provider.get(_material_live_provider_id(provider_id), False)
                or intelligence_key_loaded_by_provider.get(provider_id, False)
            ),
        )
        for provider_id, label, category, next_action, target_route, gateway_registered in PROVIDER_DEFINITIONS
    ]
    key_loaded_count = (
        int(live_config["key_loaded_count"])
        + int(material_live_config["key_loaded_count"])
        + int(intelligence_live_config["key_loaded_count"])
    )
    return PersonalProductionProviderCapabilities(
        providers=providers,
        provider_count=len(providers),
        configured_provider_count=sum(1 for provider in providers if provider.configured),
        live_provider_count=sum(1 for provider in providers if provider.live_enabled),
        key_loaded_count=key_loaded_count,
        material_live_provider_count=int(material_live_config["live_provider_count"]),
        material_key_loaded_count=int(material_live_config["key_loaded_count"]),
        intelligence_live_provider_count=int(intelligence_live_config["live_provider_count"]),
        intelligence_key_loaded_count=int(intelligence_live_config["key_loaded_count"]),
        ai_live_gateway_status="planned_gated_disabled_by_default",
        ocr_document_live_gateway_status="planned_gated_disabled_by_default",
        legal_enterprise_live_gateway_status="planned_gated_disabled_by_default",
        controlled_case_analysis_runtime_status="planned_gated_draft_only",
        fact_skill_baseline_detected=_baseline_detected(case_analysis_baselines, "case_fact_extraction_skill"),
        legal_analysis_skill_baseline_detected=_baseline_detected(case_analysis_baselines, "case_legal_analysis_skill"),
        open_case_analysis_draft_ready=True,
        training_data_generation_disabled=True,
        skill_auto_update_disabled=True,
        evaluation_reference_only=True,
        personal_production_pilot_status="ready_gated_owner_download_only",
        personal_case_workspace_status="owner_only_metadata_ready",
        fact_preview_correction_workbench_status="fact_preview_correction_metadata_ready",
        legal_analysis_draft_workbench_status="legal_analysis_draft_metadata_ready",
        skill_final_draft_workbench_status="skill_final_draft_metadata_ready",
        owner_output_center_status="owner_output_center_metadata_ready",
        personal_trial_readiness_status="trial_readiness_metadata_ready",
        personal_provider_readiness_status="provider_readiness_metadata_ready",
        personal_material_live_connection_status="ocr_document_live_connection_metadata_ready",
        personal_live_connection_status="personal_live_connection_metadata_ready",
        personal_legal_enterprise_gateway_status="legal_enterprise_gateway_metadata_ready",
        training_artifact_loader_status="training_artifact_loader_metadata_ready",
        codex_training_run_status="codex_training_run_metadata_ready",
        real_closed_case_training_intake_status="real_closed_case_training_intake_metadata_ready",
        codex_skill_draft_builder_status="codex_skill_draft_builder_metadata_ready",
        personal_production_pilot_dashboard_status="dashboard_metadata_ready",
        pilot_ai_ocr_legal_enterprise_skill_case_analysis_connected=True,
        case_workspace_owner_raw_view_gated=True,
        fact_preview_owner_correction_ready=True,
        fact_preview_legal_analysis_input_ready=True,
        fact_preview_legal_analysis_auto_triggered=False,
        fact_preview_gate_reference_only=True,
        legal_analysis_draft_only=True,
        legal_analysis_draft_review_ready=True,
        legal_analysis_final_opinion_blocked=True,
        legal_analysis_final_report_blocked=True,
        legal_analysis_owner_download_metadata_ready=True,
        fact_skill_final_draft_ready=True,
        legal_analysis_skill_final_draft_ready=True,
        skill_final_draft_owner_download_ready=True,
        skill_final_draft_auto_publish_disabled=True,
        skill_final_draft_open_case_training_disabled=True,
        skill_final_draft_gate_reference_only=True,
        pilot_dashboard_quality_panels_ready=True,
        pilot_dashboard_optimization_suggestions_ready=True,
        owner_only_downloads_ready=True,
        owner_output_center_ready=True,
        owner_output_center_download_ready=True,
        trial_readiness_ready=True,
        trial_checklist_ready=True,
        trial_issue_log_ready=True,
        trial_quality_review_ready=True,
        trial_safety_confirmation_ready=True,
        trial_optimization_backlog_ready=True,
        trial_issue_log_reference_only=True,
        trial_quality_review_reference_only=True,
        provider_readiness_ready=True,
        provider_registry_ready=True,
        secret_boundary_ready=True,
        live_gate_ready=True,
        usage_cost_metadata_ready=True,
        dry_run_health_ready=True,
        real_provider_calls_still_disabled=True,
        material_live_connection_ready=True,
        material_live_provider_registry_ready=True,
        material_live_secret_boundary_ready=True,
        material_live_gate_ready=True,
        material_live_dry_run_health_ready=True,
        material_live_raw_content_blocked=True,
        material_live_ai_prompt_injection_blocked=True,
        personal_live_connection_ready=True,
        personal_live_connection_provider_registry_ready=True,
        personal_live_connection_secret_boundary_ready=True,
        personal_live_connection_gate_ready=True,
        personal_live_connection_usage_cost_ready=True,
        personal_live_connection_health_ready=True,
        personal_live_connection_audit_ready=True,
        legal_enterprise_gateway_ready=True,
        legal_provider_readiness_ready=True,
        enterprise_provider_readiness_ready=True,
        legal_source_trace_ready=True,
        enterprise_verification_ready=True,
        legal_enterprise_review_required=True,
        training_artifact_loader_ready=True,
        codex_training_scheme_ready=True,
        case_cause_taxonomy_ready=True,
        multi_level_case_cause_loader_ready=True,
        experience_package_manifest_ready=True,
        skill_manifest_loader_ready=True,
        case_cause_fallback_ready=True,
        skill_context_dry_run_ready=True,
        codex_fine_tune_training_disabled=True,
        training_artifact_open_case_training_disabled=True,
        training_artifact_skill_auto_publish_disabled=True,
        closed_case_training_run_ready=True,
        synthetic_closed_case_samples_ready=True,
        training_run_manifest_ready=True,
        generated_experience_packages_ready=True,
        generated_skill_manifests_ready=True,
        generated_evaluation_gate_test_cases_ready=True,
        generated_loading_manifest_ready=True,
        training_run_load_dry_run_ready=True,
        training_run_open_case_training_disabled=True,
        training_run_skill_auto_publish_disabled=True,
        training_run_fine_tune_disabled=True,
        training_run_real_case_material_read_disabled=True,
        real_closed_case_training_intake_ready=True,
        real_closed_case_redaction_pipeline_ready=True,
        real_closed_case_classification_ready=True,
        real_closed_case_training_sample_segmentation_ready=True,
        real_closed_case_source_trace_ready=True,
        real_closed_case_review_queue_ready=True,
        real_closed_case_open_case_training_disabled=True,
        real_closed_case_raw_content_blocked=True,
        real_closed_case_ready_for_codex_training=False,
        codex_skill_draft_builder_ready=True,
        codex_skill_draft_eligible_sample_selection_ready=True,
        codex_skill_draft_generation_ready=True,
        codex_skill_draft_manual_review_ready=True,
        codex_skill_draft_source_trace_ready=True,
        codex_skill_draft_audit_ready=True,
        codex_skill_draft_not_publishable=True,
        codex_skill_draft_provider_call_disabled=True,
        codex_skill_draft_raw_content_blocked=True,
        codex_skill_draft_api_key_read_disabled=True,
        external_delivery_disabled=True,
        public_link_disabled=True,
        email_sending_disabled=True,
        final_legal_opinion_auto_generation_disabled=True,
        final_report_auto_generation_disabled=True,
        open_case_training_data_generation_disabled=True,
        dry_run_ready=True,
        document_dry_run_ready=True,
        ocr_dry_run_ready=True,
        legal_dry_run_ready=True,
        enterprise_dry_run_ready=True,
        live_call_requires_confirmation=True,
        draft_only_output=True,
        raw_content_blocked_by_default=True,
        ai_prompt_injection_blocked_by_default=True,
        citation_finalization_blocked_by_default=True,
        warnings=[
            "AI、材料/OCR、法律与企业信息网关均为 mock-first 或 gated.",
            "AI Provider Live Gateway: planned / gated / disabled by default.",
            "OCR / Document Provider Live Gateway: planned / gated / disabled by default.",
            "Legal / Enterprise API Live Gateway: planned / gated / disabled by default.",
            "Controlled Case Analysis Runtime: open-case draft-only runtime; no training data generation or Skill auto update.",
            "Personal Production Pilot: connected / gated / owner-download-only; public link, email, external delivery, final opinion, and final report auto-generation disabled.",
            "Case Workspace: owner-only metadata ready; raw view gate does not return real content.",
            "Fact Preview Workbench: owner correction ready; legal analysis input ready is metadata only and does not auto-trigger analysis.",
            "Legal Analysis Draft Workbench: draft-only metadata ready; final legal opinion and final report generation are blocked.",
            "Skill Final Draft Workbench: two Skill final drafts are owner-only metadata; no auto publish or open-case training is triggered.",
            "Owner-only Output Center: output registry and owner download metadata ready; no real file, public link, email, or external delivery.",
            "Trial Readiness: trial sessions, checklist, observations, issue log, quality review, safety confirmation, and optimization backlog are metadata-only and reference-only.",
            "Provider Readiness: provider registry, secret boundary, live gates, usage/cost metadata, and dry-run health are ready; real provider calls remain disabled.",
            "OCR / Document Live Connection: provider registry, secret boundary, live gates, dry-run health, audit, and safety metadata are ready; no file upload or provider call is executed.",
            "Personal Live Connection: AI / OCR / Document / Legal / Enterprise readiness dashboard is metadata-only; no live network call is executed.",
            "Legal / Enterprise Gateway: legal search and enterprise lookup return source-traced review metadata only; no final citation or company finding is selected.",
            "Codex Training Artifact Loader: multi-level case-cause artifacts are metadata-only; no fine-tune training, open-case training, Skill update, or Skill publish is executed.",
            "Closed Case Codex Training Run: synthetic closed-case samples generate training run metadata and are validated by loader dry-run only.",
            "Real Closed-Case Training Intake: authorized closed-case materials are represented as redacted metadata only; no Codex training is executed in v7.31a.",
            "Training Experience Pipeline: v7.31b creates redacted, reviewed experience candidates only.",
            "Codex Skill Draft Builder: v7.31c imports approved experience metadata and creates review-only Skill draft metadata without publishing Skills.",
            "Pilot Dashboard: quality scores and suggestions are reference-only mock metadata.",
            f"key_loaded_count={key_loaded_count} only reports count, never key values.",
            "AI, document, OCR, legal, and enterprise dry-runs are ready; live calls require explicit confirmation.",
            "raw content, AI prompt injection, and citation finalization are blocked by default.",
        ],
    ).model_dump()


def _material_live_provider_id(provider_id: str) -> str:
    mapping = {
        "mineru_file_parser_provider": "mineru",
        "docling_file_parser_provider": "docling",
        "paddleocr_provider": "paddleocr",
        "ocr_provider": "paddleocr",
    }
    return mapping.get(provider_id, provider_id)


def _baseline_detected(report: dict, skill_key: str) -> bool:
    for baseline in report.get("baselines", []):
        if baseline.get("skill_key") == skill_key:
            return bool(baseline.get("baseline_detected"))
    return False
