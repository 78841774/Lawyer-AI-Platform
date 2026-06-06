from personal_case_workspace.schemas import CaseWorkspaceCase, CaseWorkspaceMaterial


CASES = [
    CaseWorkspaceCase(
        case_id="case_workspace_mock_001",
        case_alias="个人本地试点案件 metadata",
        material_count=3,
        source_trace_count=4,
        warnings=["仅为 synthetic mock metadata；未读取真实案件材料。"],
    ),
    CaseWorkspaceCase(
        case_id="case_workspace_mock_002",
        case_alias="材料复核路径样本 metadata",
        material_count=2,
        source_trace_count=3,
        warnings=["用于展示 owner-only material workspace，不代表真实案件。"],
    ),
]

MATERIALS = [
    CaseWorkspaceMaterial(
        material_id="material_contract_metadata_001",
        case_id="case_workspace_mock_001",
        material_title="合同类材料 metadata",
        material_type="contract_metadata",
        source_trace_ids=["cw_source_trace_001", "cw_source_trace_002"],
        warnings=["不展示材料正文；owner raw view 仅返回受控占位 metadata。"],
    ),
    CaseWorkspaceMaterial(
        material_id="material_chat_metadata_001",
        case_id="case_workspace_mock_001",
        material_title="沟通记录材料 metadata",
        material_type="communication_metadata",
        source_trace_ids=["cw_source_trace_003"],
        warnings=["不展示沟通正文；不写入 AI prompt。"],
    ),
    CaseWorkspaceMaterial(
        material_id="material_payment_metadata_001",
        case_id="case_workspace_mock_001",
        material_title="付款凭证材料 metadata",
        material_type="payment_metadata",
        source_trace_ids=["cw_source_trace_004"],
        warnings=["仅显示凭证 metadata，不返回本地路径或图片原文。"],
    ),
    CaseWorkspaceMaterial(
        material_id="material_review_metadata_001",
        case_id="case_workspace_mock_002",
        material_title="复核样本材料 metadata",
        material_type="review_metadata",
        source_trace_ids=["cw_source_trace_005"],
        warnings=["仅用于本地 pilot 路径展示。"],
    ),
    CaseWorkspaceMaterial(
        material_id="material_ocr_metadata_001",
        case_id="case_workspace_mock_002",
        material_title="OCR 状态样本 metadata",
        material_type="ocr_metadata",
        source_trace_ids=["cw_source_trace_006", "cw_source_trace_007"],
        warnings=["OCR 原文默认不显示，不注入 AI prompt。"],
    ),
]


def list_cases() -> list[CaseWorkspaceCase]:
    return CASES


def get_case(case_id: str) -> CaseWorkspaceCase | None:
    return next((case for case in CASES if case.case_id == case_id), None)


def list_materials(case_id: str | None = None) -> list[CaseWorkspaceMaterial]:
    if case_id is None:
        return MATERIALS
    return [material for material in MATERIALS if material.case_id == case_id]


def get_material(material_id: str) -> CaseWorkspaceMaterial | None:
    return next((material for material in MATERIALS if material.material_id == material_id), None)
