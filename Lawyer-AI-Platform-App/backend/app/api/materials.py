from fastapi import APIRouter, File, Form, UploadFile

from app.core.config import settings
from app.models.material import Material
from app.services.material_service import MaterialService

router = APIRouter(prefix="/cases/{case_id}/materials", tags=["materials"])
material_service = MaterialService(storage_root=settings.storage_root)


@router.post("")
def upload_material(
    case_id: str,
    file: UploadFile = File(...),
    material_type: str = Form("document")
) -> Material:
    return material_service.save_material(
        case_id=case_id,
        file=file,
        material_type=material_type
    )


@router.get("")
def list_materials(case_id: str) -> list[Material]:
    return material_service.list_materials(case_id)
