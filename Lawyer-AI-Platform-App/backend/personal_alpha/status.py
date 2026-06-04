from typing import Any

from personal_alpha.schemas import PersonalAlphaStatus


def get_personal_alpha_status() -> dict[str, Any]:
    return PersonalAlphaStatus(
        warnings=[
            "Personal Alpha is local-only.",
            "Real case material must stay outside Git.",
            "Dry-run does not read material content.",
            "Manual lawyer review is required.",
        ]
    ).model_dump()
