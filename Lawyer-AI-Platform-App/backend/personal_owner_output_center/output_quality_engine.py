from personal_owner_output_center.output_registry import get_registry_output
from personal_owner_output_center.schemas import OwnerOutputQuality


def build_output_quality(output_id: str) -> OwnerOutputQuality | None:
    output = get_registry_output(output_id)
    if output is None:
        return None
    return OwnerOutputQuality(
        output_id=output_id,
        quality_score=output.quality_score,
        dimension_scores=output.dimension_scores,
        optimization_suggestions=output.optimization_suggestions,
        warnings=["Quality score is reference-only and does not guarantee legal correctness or delivery readiness."],
    )
