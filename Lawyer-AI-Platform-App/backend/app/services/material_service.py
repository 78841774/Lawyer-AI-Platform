import shutil
from pathlib import Path

from fastapi import UploadFile

from app.models.material import Material
from app.repositories.case_repository import CaseRepository
from app.repositories.material_repository import MaterialRepository


class MaterialService:
    def __init__(
        self,
        *,
        material_repository: MaterialRepository,
        case_repository: CaseRepository,
        storage_root: str
    ) -> None:
        self.material_repository = material_repository
        self.case_repository = case_repository
        self.storage_root = Path(storage_root)

    def save_material(
        self,
        case_id: str,
        file: UploadFile,
        material_type: str = "document"
    ) -> Material:
        if self.case_repository.get_by_case_id(case_id) is None:
            raise ValueError("case not found")

        material_id = self.material_repository.next_material_id()
        filename = Path(file.filename or f"{material_id}.bin").name

        target_dir = self.storage_root / "original-files" / case_id
        target_dir.mkdir(parents=True, exist_ok=True)
        target_path = target_dir / filename

        with target_path.open("wb") as output_file:
            shutil.copyfileobj(file.file, output_file)

        return self.material_repository.create(
            material_id=material_id,
            case_id=case_id,
            filename=filename,
            material_type=material_type,
            storage_path=str(target_path),
            status="uploaded"
        )

    def list_materials(self, case_id: str) -> list[Material]:
        return self.material_repository.list_by_case_id(case_id)
