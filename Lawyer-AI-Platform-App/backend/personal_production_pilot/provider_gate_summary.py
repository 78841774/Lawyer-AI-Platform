from personal_production_pilot.schemas import ProviderGate, ProviderGateSummary


PROVIDER_GATES = [
    ("openai", "OpenAI Provider", "ai"),
    ("deepseek", "DeepSeek Provider", "ai"),
    ("paddleocr", "PaddleOCR / Baidu AI Studio", "ocr"),
    ("mineru", "MinerU File Parser", "document"),
    ("docling", "Docling File Parser", "document"),
    ("kuaicha365_lawskills_provider", "快查 365 LawSkills", "legal"),
    ("tianyancha_ai_provider", "天眼查 AI", "enterprise"),
]


def build_provider_gate_summary() -> dict:
    gates = [
        ProviderGate(
            provider_id=provider_id,
            display_name=display_name,
            category=category,
            warnings=[
                "Live mode is disabled by default.",
                "External provider use requires explicit confirmation.",
                "API key values are not read or returned by v7.17 pilot summary.",
            ],
        )
        for provider_id, display_name, category in PROVIDER_GATES
    ]
    return ProviderGateSummary(
        provider_gates=gates,
        provider_count=len(gates),
        live_enabled_count=sum(1 for gate in gates if gate.live_enabled),
        dry_run_ready_count=sum(1 for gate in gates if gate.dry_run_ready),
        warnings=["Provider gates are static v7.17 pilot metadata; no API key lookup or provider call is performed."],
    ).model_dump()
