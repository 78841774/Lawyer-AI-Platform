import re
import shutil
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path, PurePosixPath
from uuid import uuid4

from fastapi import UploadFile

from app.models.material import Material
from app.repositories.case_repository import CaseRepository
from app.repositories.material_repository import MaterialRepository


@dataclass(frozen=True)
class MaterialUploadItem:
    file: UploadFile
    relative_path: str | None = None
    material_type: str = "document"
    display_order: int = 0


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
        material_type: str = "document",
        relative_path: str | None = None,
        upload_batch_id: str | None = None
    ) -> Material:
        return self.save_materials_batch(
            case_id=case_id,
            items=[
                MaterialUploadItem(
                    file=file,
                    relative_path=relative_path,
                    material_type=material_type,
                    display_order=0
                )
            ],
            upload_batch_id=upload_batch_id
        )[0]

    def save_materials_batch(
        self,
        *,
        case_id: str,
        items: list[MaterialUploadItem],
        upload_batch_id: str | None = None
    ) -> list[Material]:
        if self.case_repository.get_by_case_id(case_id) is None:
            raise ValueError("case not found")
        if not items:
            raise ValueError("no files uploaded")

        resolved_batch_id = self._sanitize_batch_id(upload_batch_id)
        saved_materials: list[Material] = []
        for index, item in enumerate(items):
            saved_materials.append(
                self._save_one_material(
                    case_id=case_id,
                    item=item,
                    upload_batch_id=resolved_batch_id,
                    display_order=item.display_order if item.display_order >= 0 else index
                )
            )
        return saved_materials

    def list_materials(self, case_id: str) -> list[Material]:
        return self.material_repository.list_by_case_id(case_id)

    def _save_one_material(
        self,
        *,
        case_id: str,
        item: MaterialUploadItem,
        upload_batch_id: str,
        display_order: int
    ) -> Material:
        material_id = self.material_repository.next_material_id()
        fallback_filename = item.file.filename or f"{material_id}.bin"
        relative_path = self._sanitize_relative_path(
            item.relative_path or fallback_filename,
            fallback_filename=fallback_filename
        )
        path_parts = PurePosixPath(relative_path).parts
        original_filename = path_parts[-1]
        folder_path = "/".join(path_parts[:-1])
        file_ext = Path(original_filename).suffix.lower()[:40]

        batch_dir = self.storage_root / "original-files" / case_id / upload_batch_id
        target_path = self._build_safe_target_path(batch_dir, relative_path)
        target_path.parent.mkdir(parents=True, exist_ok=True)

        with target_path.open("wb") as output_file:
            shutil.copyfileobj(item.file.file, output_file)

        return self.material_repository.create(
            material_id=material_id,
            case_id=case_id,
            filename=original_filename,
            original_filename=original_filename,
            relative_path=relative_path,
            folder_path=folder_path,
            file_ext=file_ext,
            upload_batch_id=upload_batch_id,
            display_order=display_order,
            material_type=item.material_type,
            storage_path=str(target_path),
            status="uploaded"
        )

    def _sanitize_relative_path(self, value: str, *, fallback_filename: str) -> str:
        raw_value = value.replace("\\", "/").replace("\x00", "").strip()
        parts: list[str] = []
        for part in PurePosixPath(raw_value).parts:
            cleaned_part = part.strip()
            if cleaned_part in {"", ".", "..", "/"}:
                continue
            if cleaned_part.startswith("/"):
                continue
            parts.append(self._sanitize_path_part(cleaned_part))

        if not parts:
            parts = [self._sanitize_path_part(Path(fallback_filename).name or "material.bin")]
        return "/".join(parts)

    def _sanitize_path_part(self, value: str) -> str:
        cleaned = re.sub(r"[\x00-\x1f]", "", value).strip()
        cleaned = cleaned.replace("/", "_").replace("\\", "_")
        return cleaned or "unnamed"

    def _sanitize_batch_id(self, value: str | None) -> str:
        if value:
            cleaned = re.sub(r"[^A-Za-z0-9_.-]", "_", value.strip())[:80]
            if cleaned and cleaned not in {".", ".."}:
                return cleaned
        timestamp = datetime.utcnow().strftime("%Y%m%d%H%M%S")
        return f"batch_{timestamp}_{uuid4().hex[:8]}"

    def _build_safe_target_path(self, batch_dir: Path, relative_path: str) -> Path:
        base_dir = batch_dir.resolve()
        target_path = (batch_dir / relative_path).resolve()
        target_path.relative_to(base_dir)
        return target_path
