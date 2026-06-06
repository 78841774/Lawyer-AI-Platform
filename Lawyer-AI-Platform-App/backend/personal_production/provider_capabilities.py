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
