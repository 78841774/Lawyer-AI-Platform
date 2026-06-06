from personal_live_connection.schemas import LiveConnectionRuntime, LiveConnectionRuntimeList


RUNTIMES = [
    ("personal_ai_gateway", "AI Provider Gateway", "ai", "/personal-ai-gateway"),
    ("personal_material_runtime", "OCR / Document Provider Gateway", "material", "/personal-material-runtime"),
    ("personal_intelligence_gateway", "Legal / Enterprise API Gateway", "intelligence", "/personal-intelligence"),
    ("personal_production_pilot", "Personal Production Pilot", "pilot", "/personal-production-pilot"),
]


def build_runtimes() -> dict:
    runtimes = [
        LiveConnectionRuntime(
            runtime_id=runtime_id,
            label=label,
            category=category,
            target_route=route,
            warnings=["Runtime participates in v7.28 controlled live connection metadata only."],
        )
        for runtime_id, label, category, route in RUNTIMES
    ]
    return LiveConnectionRuntimeList(
        runtimes=runtimes,
        runtime_count=len(runtimes),
        warnings=["All runtimes remain dry-run ready and live-disabled by default."],
    ).model_dump()

