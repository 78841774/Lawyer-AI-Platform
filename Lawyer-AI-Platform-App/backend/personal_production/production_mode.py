from personal_production.schemas import PersonalProductionMode, PersonalProductionStatus


def build_personal_production_status() -> dict:
    return PersonalProductionStatus(
        warnings=[
            "v7.0 establishes personal production and showcase foundation.",
            "Real provider calls are not enabled in v7.0.",
            "External client delivery is not enabled.",
        ],
    ).model_dump()


def build_personal_production_mode() -> dict:
    return PersonalProductionMode().model_dump()
