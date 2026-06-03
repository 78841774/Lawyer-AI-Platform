from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.material import Material


class MaterialRepository:
    def __init__(self, db: Session) -> None:
        self.db = db

    def next_material_id(self) -> str:
        index = self.db.query(Material).count() + 1
        while self.get_by_material_id(f"material_{index:03d}") is not None:
            index += 1
        return f"material_{index:03d}"

    def create(
        self,
        *,
        material_id: str,
        case_id: str,
        filename: str,
        material_type: str,
        storage_path: str,
        status: str
    ) -> Material:
        material = Material(
            material_id=material_id,
            case_id=case_id,
            filename=filename,
            material_type=material_type,
            storage_path=storage_path,
            status=status
        )
        self.db.add(material)
        self.db.commit()
        self.db.refresh(material)
        return material

    def get_by_material_id(self, material_id: str) -> Material | None:
        return self.db.execute(
            select(Material).where(Material.material_id == material_id)
        ).scalar_one_or_none()

    def list_by_case_id(self, case_id: str) -> list[Material]:
        return list(
            self.db.execute(
                select(Material)
                .where(Material.case_id == case_id)
                .order_by(Material.created_at.asc())
            ).scalars()
        )
