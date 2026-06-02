import shutil
from pathlib import Path

from fastapi import UploadFile

from app.models.material import Material


class MaterialService:
    def __init__(self, storage_root: str) -> None:
        self.storage_root = Path(storage_root)
        self._materials: dict[str, list[Material]] = {}
        self._counter = 0

    def save_material(
        self,
        case_id: str,
        file: UploadFile,
        material_type: str = "document"
    ) -> Material:
        self._counter += 1
        material_id = f"material_{self._counter:03d}"
        filename = Path(file.filename or f"{material_id}.bin").name

        target_dir = self.storage_root / "original-files" / case_id
        target_dir.mkdir(parents=True, exist_ok=True)
        target_path = target_dir / filename

        with target_path.open("wb") as output_file:
            shutil.copyfileobj(file.file, output_file)

        material = Material(
            material_id=material_id,
            case_id=case_id,
            filename=filename,
            material_type=material_type,
            storage_path=str(target_path),
            status="uploaded"
        )
        self._materials.setdefault(case_id, []).append(material)
        return material

    def list_materials(self, case_id: str) -> list[Material]:
        return self._materials.get(case_id, [])
