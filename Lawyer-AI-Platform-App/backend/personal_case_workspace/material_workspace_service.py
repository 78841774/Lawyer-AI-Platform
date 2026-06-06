from personal_case_workspace.schemas import CaseWorkspaceMaterial, CaseWorkspaceMaterialList
from personal_case_workspace.storage import get_material, list_materials


def build_material_list(case_id: str) -> CaseWorkspaceMaterialList:
    materials = list_materials(case_id)
    return CaseWorkspaceMaterialList(
        case_id=case_id,
        materials=materials,
        material_count=len(materials),
        warnings=["材料列表只展示 metadata；不显示原文、OCR 全文、本地路径或密钥值。"],
    )


def build_material_detail(material_id: str) -> CaseWorkspaceMaterial | None:
    return get_material(material_id)
