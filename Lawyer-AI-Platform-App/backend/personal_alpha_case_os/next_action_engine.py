from typing import Any

from personal_alpha_case_os.schemas import PersonalAlphaCaseOSNextAction
from personal_alpha_case_os.state_machine import derive_next_action


def build_next_action(case_id: str, context: dict[str, Any]) -> dict[str, Any]:
    action = derive_next_action(context)
    return PersonalAlphaCaseOSNextAction(
        case_id=case_id,
        current_stage=str(action.get("current_stage", "workspace_run_pending")),
        next_action=str(action.get("next_action", "create_workspace_run")),
        next_action_label=str(action.get("next_action_label", "Create Workspace Run")),
        target_route=str(action.get("target_route", "/personal-alpha-workspace")),
        target_id=action.get("target_id"),
        blocked=bool(action.get("blocked", False)),
        blocked_reasons=[str(item) for item in action.get("blocked_reasons", [])],
        mock_or_redacted_only=True,
        raw_content_included=False,
        warnings=[str(item) for item in action.get("warnings", [])],
    ).model_dump()
