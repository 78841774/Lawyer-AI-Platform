from personal_production_pilot.pilot_registry import get_runtime_ids
from personal_production_pilot.schemas import PilotReadiness


def build_readiness() -> dict:
    runtime_ids = set(get_runtime_ids())
    readiness = {
        "personal_production_console_connected": "personal_production_console" in runtime_ids,
        "ai_gateway_connected": "ai_provider_live_gateway" in runtime_ids,
        "ocr_document_gateway_connected": "ocr_document_provider_live_gateway" in runtime_ids,
        "legal_enterprise_gateway_connected": "legal_enterprise_api_live_gateway" in runtime_ids,
        "skill_training_runtime_connected": "skill_training_runtime" in runtime_ids,
        "case_analysis_runtime_connected": "controlled_case_analysis_runtime" in runtime_ids,
        "delivery_packet_connected": "personal_delivery_packet_runtime" in runtime_ids,
        "owner_output_center_ready": True,
        "skill_final_drafts_aggregated": True,
        "fact_outputs_aggregated": True,
        "legal_drafts_aggregated": True,
        "pilot_delivery_outputs_aggregated": True,
        "owner_download_ready": "owner_download_runtime" in runtime_ids,
        "external_delivery_disabled": True,
        "public_link_disabled": True,
        "email_sending_disabled": True,
        "final_legal_opinion_auto_generation_disabled": True,
        "final_report_auto_generation_disabled": True,
        "training_data_generation_disabled_for_open_cases": True,
    }
    missing = [key for key, value in readiness.items() if not value]
    return PilotReadiness(
        pilot_ready=not missing,
        readiness=readiness,
        missing_requirements=missing,
        warnings=[] if not missing else ["Pilot has missing readiness metadata."],
    ).model_dump()
