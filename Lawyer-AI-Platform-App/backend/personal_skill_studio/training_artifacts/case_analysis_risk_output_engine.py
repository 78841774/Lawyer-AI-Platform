from personal_skill_studio.training_artifacts.schemas import CaseAnalysisRuntimeOutput


def count_risk_outputs(outputs: list[CaseAnalysisRuntimeOutput]) -> dict[str, int]:
    return {
        "risk_flagged_count": sum(1 for output in outputs if output.risk_level in {"medium", "high"}),
        "high_risk_count": sum(1 for output in outputs if output.risk_level == "high"),
    }
