from personal_skill_studio.training_artifacts.case_cause_taxonomy import find_node_by_path
from personal_skill_studio.training_artifacts.schemas import CaseCauseClassification, RealClosedCaseTrainingIntake


def classify_case_cause(intake: RealClosedCaseTrainingIntake) -> CaseCauseClassification:
    path = intake.target_case_cause_path or ["civil", "contract_dispute", "sales_contract_dispute"]
    node = find_node_by_path(path)
    return CaseCauseClassification(
        classification_id=f"{intake.intake_id}_case_cause_classification",
        intake_id=intake.intake_id,
        case_domain=path[0] if path else "civil",
        case_cause_level_1=path[1] if len(path) > 1 else "civil",
        case_cause_level_2=path[2] if len(path) > 2 else "",
        case_cause_level_3=path[3] if len(path) > 3 else None,
        case_cause_name=node.case_cause_name if node else "待人工复核案由",
        case_cause_code=node.case_cause_code if node else "manual.review.required",
        case_cause_path=path,
        confidence_score=0.82 if node else 0.56,
        fallback_case_cause_path=path[:-1] or ["civil"],
        classification_notes=[
            "Classification uses metadata fields only.",
            "Manual review remains required before future real closed-case Codex training.",
        ],
    )
