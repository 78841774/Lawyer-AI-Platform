from personal_skill_studio.schemas import SkillFinalGateReport
from personal_skill_studio.skill_final_draft_engine import get_skill_final_draft


def build_skill_final_gate(skill_id: str) -> SkillFinalGateReport | None:
    draft = get_skill_final_draft(skill_id)
    if draft is None:
        return None
    missing = [] if draft.gate_status == "reference_ready" else [f"{skill_id} promotion gate metadata not complete"]
    return SkillFinalGateReport(
        skill_id=skill_id,
        gate_status=draft.gate_status,
        gate_fields={
            "gate_reference_only": True,
            "blocks_next_stage": False,
            "owner_only": True,
            "source_trace_required": True,
            "lawyer_review_required": True,
            "final_skill_published": False,
            "skill_auto_published": False,
            "training_data_generated": False,
            "writes_to_training_set": False,
        },
        missing_gate_files=missing,
        baseline_discovered=draft.baseline_discovered,
        baseline_complete=draft.baseline_complete,
        warnings=["Gate is a quality and optimization reference only; it does not publish Skill or block the next stage."],
    )
