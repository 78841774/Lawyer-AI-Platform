from collections import Counter

from personal_owner_output_center.output_registry import list_registry_outputs
from personal_owner_output_center.schemas import OwnerOutputList, OwnerOutputStatus


def build_status() -> dict:
    return OwnerOutputStatus(
        warnings=[
            "v7.23 aggregates owner-only draft metadata from Skill, fact, legal draft, Pilot, and delivery sources.",
            "Downloads are metadata actions only and do not create public links, email, formal reports, final opinions, or external delivery.",
        ],
    ).model_dump()


def build_output_list() -> dict:
    outputs = list_registry_outputs()
    counter = Counter(output.output_type for output in outputs)
    return OwnerOutputList(
        outputs=outputs,
        output_count=len(outputs),
        skill_final_draft_count=counter.get("skill_final_draft", 0),
        fact_output_count=sum(counter[key] for key in counter if key.startswith("fact_")),
        legal_draft_count=sum(counter[key] for key in counter if key.endswith("_draft") and not key.startswith("fact_")),
        pilot_delivery_count=sum(
            counter[key]
            for key in [
                "production_pilot_summary",
                "review_summary",
                "pilot_source_trace_summary",
                "delivery_packet_draft",
                "export_boundary_summary",
            ]
        ),
        warnings=["Output list is owner-only draft metadata and contains no raw material or generated final files."],
    ).model_dump()
