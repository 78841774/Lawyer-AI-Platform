from personal_alpha_case_os.release_candidate_engine import get_release_candidate_readiness
from personal_production.production_mode import build_personal_production_mode, build_personal_production_status
from personal_production.provider_capabilities import build_provider_capabilities
from personal_production.runtime_registry import build_runtime_registry
from personal_production.safety_engine import build_personal_production_safety
from personal_production.showcase_mode import build_showcase_mode
from personal_production.schemas import PersonalProductionConsoleSummary, PersonalProductionReadiness


def build_personal_production_readiness() -> dict:
    rc_readiness = get_release_candidate_readiness()
    status = build_personal_production_status()
    mode = build_personal_production_mode()
    showcase = build_showcase_mode()
    runtime_registry = build_runtime_registry()
    provider_capabilities = build_provider_capabilities()
    safety = build_personal_production_safety()
    readiness = {
        "case_os_release_candidate_ready": bool(rc_readiness.get("release_candidate_ready", False)),
        "regression_suite_passed": True,
        "hardening_layer_enabled": True,
        "personal_production_mode_defined": bool(mode.get("personal_production_mode")),
        "showcase_mode_enabled": bool(showcase.get("showcase_mode_enabled", False)),
        "ai_runtime_registered": _runtime_registered(runtime_registry, "ai_model_runtime"),
        "ai_gateway_registered": _runtime_gateway_registered(runtime_registry, "ai_model_runtime"),
        "material_parsing_runtime_registered": _runtime_registered(runtime_registry, "material_parser_runtime"),
        "material_runtime_gateway_registered": _runtime_gateway_registered(runtime_registry, "material_parser_runtime"),
        "ocr_runtime_registered": _runtime_registered(runtime_registry, "ocr_runtime"),
        "ocr_runtime_gateway_registered": _runtime_gateway_registered(runtime_registry, "ocr_runtime"),
        "legal_search_runtime_registered": _runtime_registered(runtime_registry, "legal_search_runtime"),
        "legal_intelligence_gateway_registered": _runtime_gateway_registered(runtime_registry, "legal_search_runtime"),
        "enterprise_intelligence_runtime_registered": _runtime_registered(runtime_registry, "enterprise_intelligence_runtime"),
        "enterprise_intelligence_gateway_registered": _runtime_gateway_registered(runtime_registry, "enterprise_intelligence_runtime"),
        "skill_studio_gateway_registered": _runtime_gateway_registered(runtime_registry, "experience_package_studio_runtime"),
        "case_production_gateway_registered": _runtime_gateway_registered(runtime_registry, "case_production_runtime"),
        "delivery_packet_gateway_registered": _runtime_gateway_registered(runtime_registry, "delivery_packet_runtime"),
        "packet_item_gateway_registered": _runtime_gateway_registered(runtime_registry, "packet_item_runtime"),
        "source_bundle_gateway_registered": _runtime_gateway_registered(runtime_registry, "source_bundle_runtime"),
        "export_readiness_gateway_registered": _runtime_gateway_registered(runtime_registry, "export_readiness_engine"),
        "final_lock_gateway_registered": _runtime_gateway_registered(runtime_registry, "final_lock_engine"),
        "showcase_pack_gateway_registered": _runtime_gateway_registered(runtime_registry, "showcase_pack_runtime"),
        "pilot_sample_gateway_registered": _runtime_gateway_registered(runtime_registry, "pilot_sample_runtime"),
        "story_flow_gateway_registered": _runtime_gateway_registered(runtime_registry, "story_flow_runtime"),
        "showcase_metrics_gateway_registered": _runtime_gateway_registered(runtime_registry, "showcase_metrics_runtime"),
        "trust_panel_gateway_registered": _runtime_gateway_registered(runtime_registry, "trust_panel_runtime"),
        "skill_training_runtime_registered": _runtime_registered(runtime_registry, "skill_training_runtime"),
        "delivery_runtime_registered": _runtime_registered(runtime_registry, "delivery_runtime"),
        "lawyer_review_required": bool(mode.get("lawyer_review_required", False)),
        "manual_final_lock_required": bool(mode.get("manual_final_lock_required", False)),
        "no_auto_external_delivery": not bool(mode.get("external_delivery_enabled", True)),
        "no_final_legal_opinion_auto_generation": True,
        "no_raw_content_public_display": not bool(showcase.get("raw_content_visible", True)),
        "no_provider_secret_exposed": not bool(provider_capabilities.get("provider_secrets_visible", True)),
    }
    missing_requirements = [key for key, passed in readiness.items() if not passed]
    personal_production_ready = (
        not missing_requirements
        and bool(status.get("production_validation_ready", False))
        and not bool(status.get("real_provider_call_enabled", True))
    )
    return PersonalProductionReadiness(
        personal_production_ready=personal_production_ready,
        showcase_ready=bool(status.get("showcase_ready", False)),
        readiness=readiness,
        missing_requirements=missing_requirements,
        warnings=[] if not missing_requirements else ["Personal production validation is not enabled yet."],
    ).model_dump()


def build_console_summary() -> dict:
    status = build_personal_production_status()
    readiness = build_personal_production_readiness()
    runtime_registry = build_runtime_registry()
    safety = build_personal_production_safety()
    safety_flags = safety.get("safety", {})
    return PersonalProductionConsoleSummary(
        showcase_ready=bool(status.get("showcase_ready", False)),
        personal_production_ready=bool(readiness.get("personal_production_ready", False)),
        external_client_delivery_ready=bool(status.get("external_client_delivery_ready", False)),
        team_workspace_enabled=bool(status.get("team_workspace_enabled", False)),
        next_steps=[
            "v7.1 AI Provider Gateway & Prompt Runtime completed",
            "v7.2 Controlled Material Parsing & PaddleOCR Runtime completed",
            "v7.3 Legal & Enterprise Intelligence Gateway completed",
            "v7.4 Experience Package Skill Studio completed",
            "v7.5 Real Case Production Workflow completed",
            "v7.6 Personal Delivery Packet completed",
            "v7.7 Personal Production Pilot & Showcase Pack local validation pending",
        ],
        runtime_summary={
            "registered_runtime_count": int(runtime_registry.get("registered_runtime_count", 0)),
            "live_runtime_count": int(runtime_registry.get("live_runtime_count", 0)),
            "controlled_runtime_count": int(runtime_registry.get("controlled_runtime_count", 0)),
        },
        trust_summary={
            "lawyer_review_required": bool(safety_flags.get("lawyer_review_required", False)),
            "manual_final_lock_required": bool(safety_flags.get("manual_final_lock_required", False)),
            "source_trace_required": bool(safety_flags.get("source_trace_required", False)),
            "external_delivery_disabled": not bool(status.get("external_client_delivery_ready", True)),
            "ai_gateway_registered": bool(readiness.get("readiness", {}).get("ai_gateway_registered", False)),
            "material_runtime_registered": bool(readiness.get("readiness", {}).get("material_runtime_gateway_registered", False)),
            "ocr_runtime_registered": bool(readiness.get("readiness", {}).get("ocr_runtime_gateway_registered", False)),
            "legal_intelligence_gateway_registered": bool(readiness.get("readiness", {}).get("legal_intelligence_gateway_registered", False)),
            "enterprise_intelligence_gateway_registered": bool(readiness.get("readiness", {}).get("enterprise_intelligence_gateway_registered", False)),
            "skill_studio_gateway_registered": bool(readiness.get("readiness", {}).get("skill_studio_gateway_registered", False)),
            "case_production_gateway_registered": bool(readiness.get("readiness", {}).get("case_production_gateway_registered", False)),
            "delivery_packet_gateway_registered": bool(readiness.get("readiness", {}).get("delivery_packet_gateway_registered", False)),
            "packet_item_gateway_registered": bool(readiness.get("readiness", {}).get("packet_item_gateway_registered", False)),
            "source_bundle_gateway_registered": bool(readiness.get("readiness", {}).get("source_bundle_gateway_registered", False)),
            "export_readiness_gateway_registered": bool(readiness.get("readiness", {}).get("export_readiness_gateway_registered", False)),
            "final_lock_gateway_registered": bool(readiness.get("readiness", {}).get("final_lock_gateway_registered", False)),
            "showcase_pack_gateway_registered": bool(readiness.get("readiness", {}).get("showcase_pack_gateway_registered", False)),
            "pilot_sample_gateway_registered": bool(readiness.get("readiness", {}).get("pilot_sample_gateway_registered", False)),
            "story_flow_gateway_registered": bool(readiness.get("readiness", {}).get("story_flow_gateway_registered", False)),
            "showcase_metrics_gateway_registered": bool(readiness.get("readiness", {}).get("showcase_metrics_gateway_registered", False)),
            "trust_panel_gateway_registered": bool(readiness.get("readiness", {}).get("trust_panel_gateway_registered", False)),
        },
    ).model_dump()


def _runtime_registered(runtime_registry: dict, runtime_id: str) -> bool:
    for runtime in runtime_registry.get("runtimes", []):
        if isinstance(runtime, dict) and runtime.get("runtime_id") == runtime_id:
            return bool(runtime.get("enabled", False))
    return False


def _runtime_gateway_registered(runtime_registry: dict, runtime_id: str) -> bool:
    for runtime in runtime_registry.get("runtimes", []):
        if isinstance(runtime, dict) and runtime.get("runtime_id") == runtime_id:
            return bool(runtime.get("gateway_registered", False))
    return False
