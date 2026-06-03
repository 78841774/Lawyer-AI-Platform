from typing import Any

from fastapi import APIRouter, Depends, File, Form, HTTPException, UploadFile
from sqlalchemy.orm import Session

from app.core.config import settings
from app.core.database import get_db
from app.models.material import Material
from app.repositories.case_repository import CaseRepository
from app.repositories.material_repository import MaterialRepository
from app.services.material_service import MaterialService

router = APIRouter(prefix="/cases/{case_id}/materials", tags=["materials"])


def get_material_service(db: Session) -> MaterialService:
    return MaterialService(
        material_repository=MaterialRepository(db),
        case_repository=CaseRepository(db),
        storage_root=settings.storage_root
    )


def serialize_material(material: Material) -> dict[str, Any]:
    return {
        "material_id": material.material_id,
        "case_id": material.case_id,
        "filename": material.filename,
        "material_type": material.material_type,
        "storage_path": material.storage_path,
        "status": material.status,
        "created_at": material.created_at
    }


@router.post("")
def upload_material(
    case_id: str,
    file: UploadFile = File(...),
    material_type: str = Form("document"),
    db: Session = Depends(get_db)
) -> dict[str, Any]:
    service = get_material_service(db)
    try:
        material = service.save_material(
            case_id=case_id,
            file=file,
            material_type=material_type
        )
    except ValueError as error:
        raise HTTPException(status_code=404, detail=str(error)) from error
    return serialize_material(material)


@router.get("")
def list_materials(
    case_id: str,
    db: Session = Depends(get_db)
) -> list[dict[str, Any]]:
    service = get_material_service(db)
    return [serialize_material(material) for material in service.list_materials(case_id)]
