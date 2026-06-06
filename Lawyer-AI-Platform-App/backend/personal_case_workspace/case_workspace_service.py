from personal_case_workspace.schemas import CaseWorkspaceCase, CaseWorkspaceCaseList, CaseWorkspaceStatus
from personal_case_workspace.storage import get_case, list_cases


def build_status() -> CaseWorkspaceStatus:
    return CaseWorkspaceStatus(
        version="v7.20",
        runtime_label="个人案件与材料工作台 / 事实预览与输入纠正工作台",
        fact_input_correction_ready=True,
        warnings=[
            "v7.20 强化事实预览与输入纠正工作台。",
            "真实材料读取、真实 OCR、真实 provider 调用均未启用。",
            "owner raw view 是受控动作 metadata，不返回原文。",
            "事实预览可作为法律分析输入 metadata，但不会自动触发法律分析。",
        ]
    )


def build_case_list() -> CaseWorkspaceCaseList:
    cases = list_cases()
    return CaseWorkspaceCaseList(
        cases=cases,
        case_count=len(cases),
        warnings=["案件列表仅显示 synthetic mock metadata，不代表真实客户或真实案件。"],
    )


def build_case_detail(case_id: str) -> CaseWorkspaceCase | None:
    return get_case(case_id)
