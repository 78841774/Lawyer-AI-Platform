from personal_production.schemas import PersonalProductionSafety


def build_personal_production_safety() -> dict:
    return PersonalProductionSafety(
        safety={
            "controlled_first": True,
            "mock_first_by_default": True,
            "provider_gated": True,
            "lawyer_review_required": True,
            "manual_final_lock_required": True,
            "draft_first": True,
            "source_trace_required": True,
            "no_automatic_final_legal_opinion": True,
            "no_automatic_final_report": True,
            "no_automatic_external_delivery": True,
            "no_automatic_skill_publish": True,
            "no_uncontrolled_raw_content_exposure": True,
        }
    ).model_dump()
