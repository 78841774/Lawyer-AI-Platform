from personal_production.schemas import PersonalProductionShowcase


def build_showcase_mode() -> dict:
    return PersonalProductionShowcase(
        trust_badges=[
            "AI-assisted draft",
            "Lawyer review required",
            "Source-traced",
            "Controlled runtime",
            "Manual final lock",
        ],
    ).model_dump()
