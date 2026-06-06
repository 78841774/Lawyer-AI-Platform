from personal_production_pilot.schemas import ExportBoundary


def build_export_boundary() -> dict:
    return ExportBoundary(
        warnings=[
            "Owner download is allowed as controlled metadata.",
            "Public links, emails, third-party sharing, client auto-delivery, final legal opinion labeling, and formal report labeling remain disabled.",
        ],
    ).model_dump()
