from personal_production.schemas import PersonalProductionMode, PersonalProductionStatus


def build_personal_production_status() -> dict:
    return PersonalProductionStatus(
        warnings=[
            "v7.0 establishes personal production and showcase foundation.",
            "v7.1 registers the AI Provider Gateway and Prompt Runtime.",
            "v7.2 registers controlled Material Parsing and PaddleOCR Runtime foundations.",
            "v7.3 registers legal and enterprise intelligence gateway foundations.",
            "v7.4 registers Experience Package Skill Studio foundations.",
            "v7.5 registers Real Case Production Workflow foundations.",
            "Real provider calls are not enabled in v7.5.",
            "External client delivery is not enabled.",
            "v7.30 registers Codex training scheme and multi-level case-cause artifact loader metadata; no fine-tune training or open-case training is executed.",
            "v7.31e registers internal training task and experience package metadata; no provider call, real training, or Skill publish is executed.",
            "v7.31f registers practice load review gate metadata; lawyer approval is required before future runtime loading.",
        ],
    ).model_dump()


def build_personal_production_mode() -> dict:
    return PersonalProductionMode().model_dump()
