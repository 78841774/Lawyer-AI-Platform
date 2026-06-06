from personal_skill_studio.schemas import SkillFinalDraftLineage
from personal_skill_studio.skill_baseline_discovery import build_baseline_discovery_metadata
from personal_skill_studio.skill_final_draft_engine import get_skill_final_draft


def build_skill_lineage(skill_id: str) -> SkillFinalDraftLineage | None:
    draft = get_skill_final_draft(skill_id)
    if draft is None:
        return None
    discovery = build_baseline_discovery_metadata()
    return SkillFinalDraftLineage(
        skill_id=draft.skill_id,
        source_skill_id=draft.source_skill_id,
        source_package_id=draft.source_package_id,
        derived_from=draft.derived_from,
        source_skill_files=discovery.source_skill_files,
        source_evaluation_files=discovery.source_evaluation_files,
        source_gate_files=discovery.source_gate_files,
        source_test_case_files=discovery.source_test_case_files,
        placeholder_lineage_used=not draft.baseline_complete,
        baseline_discovered=draft.baseline_discovered,
        baseline_complete=draft.baseline_complete,
        warnings=[
            "Lineage uses relative project file references and metadata identifiers only.",
            "No raw sample content, local absolute path, or API key is returned.",
        ],
    )
