from personal_owner_output_center.output_registry import get_registry_output
from personal_owner_output_center.schemas import OwnerOutputGate


def build_output_gate(output_id: str) -> OwnerOutputGate | None:
    output = get_registry_output(output_id)
    if output is None:
        return None
    flags = ["lawyer_review_pending"] if "review" in output.gate_status else []
    return OwnerOutputGate(
        output_id=output_id,
        gate_status=output.gate_status,
        gate_score=max(60, output.quality_score - 2),
        low_confidence_flags=flags,
        warnings=["Gate is a quality reference only and never blocks owner-only download in v7.23."],
    )
