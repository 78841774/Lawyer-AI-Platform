from personal_trial_readiness.schemas import TrialChecklist
from personal_trial_readiness.storage import read_json, write_json


def build_checklist(trial_id: str = "trial_mock_001") -> TrialChecklist:
    data = read_json("checklists", trial_id)
    if data:
        return TrialChecklist(**data)
    return TrialChecklist(
        trial_id=trial_id,
        warnings=["试运行清单只确认页面路径与安全边界，不表示案件质量结论。"],
    )


def create_mock_checklist(trial_id: str) -> dict:
    checklist = build_checklist(trial_id)
    write_json("checklists", trial_id, checklist.model_dump())
    return checklist.model_dump()

