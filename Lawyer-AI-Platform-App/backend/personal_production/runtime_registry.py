from personal_production.schemas import PersonalProductionRuntimeItem, PersonalProductionRuntimeRegistry


RUNTIME_DEFINITIONS = [
    ("ai_model_runtime", "AI Model Runtime", "ai"),
    ("ocr_runtime", "OCR Runtime", "ocr"),
    ("legal_search_runtime", "Legal Search Runtime", "legal_search"),
    ("skill_training_runtime", "Skill Training Runtime", "skill_training"),
    ("delivery_runtime", "Delivery Runtime", "delivery"),
    ("regression_runtime", "Regression Runtime", "regression"),
    ("safety_runtime", "Safety Runtime", "safety"),
]


def build_runtime_registry() -> dict:
    runtimes = [
        PersonalProductionRuntimeItem(
            runtime_id=runtime_id,
            label=label,
            category=category,
            warnings=[] if category in {"regression", "safety"} else ["Runtime is registered for controlled foundation use; live mode is disabled in v7.0."],
        )
        for runtime_id, label, category in RUNTIME_DEFINITIONS
    ]
    return PersonalProductionRuntimeRegistry(
        runtimes=runtimes,
        registered_runtime_count=len(runtimes),
        live_runtime_count=sum(1 for runtime in runtimes if runtime.live_enabled),
        controlled_runtime_count=sum(1 for runtime in runtimes if runtime.controlled_available),
    ).model_dump()
