from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.experience_package import ExperiencePackage


class ExperiencePackageRepository:
    def __init__(self, db: Session) -> None:
        self.db = db

    def next_package_id(self) -> str:
        index = self.db.query(ExperiencePackage).count() + 1
        while self.get_by_package_id(f"ep_{index:03d}") is not None:
            index += 1
        return f"ep_{index:03d}"

    def create(
        self,
        *,
        package_id: str,
        skill_id: str,
        name: str,
        domain: str,
        version: str,
        status: str,
        manifest_json: str,
        package_path: str
    ) -> ExperiencePackage:
        package = ExperiencePackage(
            package_id=package_id,
            skill_id=skill_id,
            name=name,
            domain=domain,
            version=version,
            status=status,
            manifest_json=manifest_json,
            package_path=package_path
        )
        self.db.add(package)
        self.db.commit()
        self.db.refresh(package)
        return package

    def get_by_package_id(self, package_id: str) -> ExperiencePackage | None:
        return self.db.execute(
            select(ExperiencePackage).where(
                ExperiencePackage.package_id == package_id
            )
        ).scalar_one_or_none()

    def list_all(self) -> list[ExperiencePackage]:
        return list(
            self.db.execute(
                select(ExperiencePackage)
                .order_by(ExperiencePackage.created_at.asc(), ExperiencePackage.id.asc())
            ).scalars()
        )

    def count_all(self) -> int:
        return self.db.query(ExperiencePackage).count()

