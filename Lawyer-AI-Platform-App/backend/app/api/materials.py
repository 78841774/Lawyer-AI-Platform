from typing import Any

from fastapi import APIRouter, Depends, File, Form, HTTPException, UploadFile
from sqlalchemy.orm import Session

from app.core.config import settings
from app.core.database import get_db
from app.models.material import Material
from app.repositories.case_repository import CaseRepository
from app.repositories.material_repository import MaterialRepository
from app.services.material_service import MaterialService, MaterialUploadItem

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
        "original_filename": material.original_filename or material.filename,
        "relative_path": material.relative_path or material.filename,
        "folder_path": material.folder_path or "",
        "file_ext": material.file_ext or "",
        "material_type": material.material_type,
        "upload_batch_id": material.upload_batch_id,
        "display_order": material.display_order or 0,
        "storage_path": material.storage_path,
        "status": material.status,
        "created_at": material.created_at
    }


@router.post("")
def upload_material(
    case_id: str,
    file: UploadFile = File(...),
    material_type: str = Form("document"),
    relative_path: str | None = Form(None),
    upload_batch_id: str | None = Form(None),
    db: Session = Depends(get_db)
) -> dict[str, Any]:
    service = get_material_service(db)
    try:
        material = service.save_material(
            case_id=case_id,
            file=file,
            material_type=material_type,
            relative_path=relative_path,
            upload_batch_id=upload_batch_id
        )
    except ValueError as error:
        raise HTTPException(status_code=404, detail=str(error)) from error
    return serialize_material(material)


@router.post("/batch")
def upload_materials_batch(
    case_id: str,
    files: list[UploadFile] = File(...),
    relative_paths: list[str] = Form(default=[]),
    material_types: list[str] = Form(default=[]),
    upload_batch_id: str | None = Form(None),
    db: Session = Depends(get_db)
) -> list[dict[str, Any]]:
    service = get_material_service(db)
    items = [
        MaterialUploadItem(
            file=file,
            relative_path=relative_paths[index] if index < len(relative_paths) else file.filename,
            material_type=material_types[index] if index < len(material_types) else "document",
            display_order=index
        )
        for index, file in enumerate(files)
    ]
    try:
        materials = service.save_materials_batch(
            case_id=case_id,
            items=items,
            upload_batch_id=upload_batch_id
        )
    except ValueError as error:
        status_code = 404 if "case not found" in str(error) else 400
        raise HTTPException(status_code=status_code, detail=str(error)) from error
    return [serialize_material(material) for material in materials]


@router.get("")
def list_materials(
    case_id: str,
    db: Session = Depends(get_db)
) -> list[dict[str, Any]]:
    service = get_material_service(db)
    return [serialize_material(material) for material in service.list_materials(case_id)]
