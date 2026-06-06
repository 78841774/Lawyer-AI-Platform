from personal_production_pilot.schemas import PilotRuntime, PilotRuntimeList


RUNTIME_DEFINITIONS = [
    ("personal_production_console", "Personal Production Console", "console", "/personal-production"),
    ("ai_provider_live_gateway", "AI Provider Live Gateway", "ai", "/personal-ai-gateway"),
    ("ocr_document_provider_live_gateway", "OCR / Document Provider Live Gateway", "material", "/personal-material-runtime"),
    ("legal_enterprise_api_live_gateway", "Legal / Enterprise API Live Gateway", "intelligence", "/personal-intelligence"),
    ("skill_training_runtime", "Skill Training Runtime", "skill", "/personal-skill-studio"),
    ("training_artifact_loader_runtime", "Codex Training Artifact Loader", "skill", "/personal-skill-studio/training-artifacts"),
    ("codex_training_run_runtime", "Closed Case Codex Training Run", "skill", "/personal-skill-studio/training-artifacts"),
    ("real_closed_case_training_intake_runtime", "Real Closed-Case Training Intake", "skill", "/personal-skill-studio/training-artifacts"),
    ("training_experience_pipeline_runtime", "Controlled Training Experience Pipeline", "skill", "/personal-skill-studio/training-artifacts"),
    ("codex_skill_draft_builder_runtime", "Skill Experience Pool & Codex Skill Draft Builder", "skill", "/personal-skill-studio/training-artifacts"),
    ("controlled_case_analysis_runtime", "Controlled Case Analysis Runtime", "case_analysis", "/personal-case-analysis"),
    ("personal_delivery_packet_runtime", "Personal Delivery Packet", "delivery_packet", "/personal-delivery-packet"),
    ("owner_download_runtime", "Final Lock / Owner Download", "owner_download", "/personal-production-pilot"),
]


def list_runtimes() -> dict:
    runtimes = [
        PilotRuntime(
            runtime_id=runtime_id,
            display_name=display_name,
            category=category,
            target_route=target_route,
            warnings=["Connected in v7.17 pilot; live provider remains disabled unless explicitly confirmed."],
        )
        for runtime_id, display_name, category, target_route in RUNTIME_DEFINITIONS
    ]
    return PilotRuntimeList(
        runtimes=runtimes,
        runtime_count=len(runtimes),
        connected_count=sum(1 for runtime in runtimes if runtime.connected),
        live_enabled_count=sum(1 for runtime in runtimes if runtime.live_enabled),
        warnings=["Pilot connects the v7.10-v7.17 personal production stack as gated metadata."],
    ).model_dump()


def get_runtime_ids() -> list[str]:
    return [runtime_id for runtime_id, _, _, _ in RUNTIME_DEFINITIONS]
