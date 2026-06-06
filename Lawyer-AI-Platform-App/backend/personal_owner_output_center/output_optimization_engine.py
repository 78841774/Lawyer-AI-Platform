from personal_owner_output_center.output_registry import get_registry_output
from personal_owner_output_center.schemas import OwnerOutputOptimization


def build_output_optimization(output_id: str) -> OwnerOutputOptimization | None:
    output = get_registry_output(output_id)
    if output is None:
        return None
    return OwnerOutputOptimization(
        output_id=output_id,
        optimization_suggestions=output.optimization_suggestions,
        warnings=["Optimization suggestions are review metadata and do not trigger Skill publishing, training, or delivery."],
    )
