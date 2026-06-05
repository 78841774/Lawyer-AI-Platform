from personal_production.schemas import PersonalProductionRuntimeItem, PersonalProductionRuntimeRegistry


RUNTIME_DEFINITIONS = [
    {
        "runtime_id": "ai_model_runtime",
        "label": "AI Model Runtime",
        "category": "ai",
        "target_route": "/personal-ai-gateway",
        "gateway_registered": True,
        "warnings": ["AI Gateway registered in v7.1. Live provider calls remain disabled."],
    },
    {"runtime_id": "ocr_runtime", "label": "OCR Runtime", "category": "ocr"},
    {"runtime_id": "legal_search_runtime", "label": "Legal Search Runtime", "category": "legal_search"},
    {"runtime_id": "skill_training_runtime", "label": "Skill Training Runtime", "category": "skill_training"},
    {"runtime_id": "delivery_runtime", "label": "Delivery Runtime", "category": "delivery"},
    {"runtime_id": "regression_runtime", "label": "Regression Runtime", "category": "regression", "warnings": []},
    {"runtime_id": "safety_runtime", "label": "Safety Runtime", "category": "safety", "warnings": []},
]


def build_runtime_registry() -> dict:
    runtimes = [
        PersonalProductionRuntimeItem(
            runtime_id=definition["runtime_id"],
            label=definition["label"],
            category=definition["category"],
            target_route=definition.get("target_route", "/personal-production"),
            gateway_registered=bool(definition.get("gateway_registered", False)),
            warnings=definition.get(
                "warnings",
                ["Runtime is registered for controlled foundation use; live mode is disabled in v7.1."],
            ),
        )
        for definition in RUNTIME_DEFINITIONS
    ]
    return PersonalProductionRuntimeRegistry(
        runtimes=runtimes,
        registered_runtime_count=len(runtimes),
        live_runtime_count=sum(1 for runtime in runtimes if runtime.live_enabled),
        controlled_runtime_count=sum(1 for runtime in runtimes if runtime.controlled_available),
    ).model_dump()
