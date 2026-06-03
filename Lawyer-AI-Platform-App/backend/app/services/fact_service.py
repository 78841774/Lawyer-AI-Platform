from pathlib import Path

from app.models.fact import Fact
from app.models.material import Material
from app.repositories.case_repository import CaseRepository
from app.repositories.fact_repository import FactRepository
from app.repositories.material_repository import MaterialRepository


class FactService:
    def __init__(
        self,
        *,
        fact_repository: FactRepository,
        material_repository: MaterialRepository,
        case_repository: CaseRepository
    ) -> None:
        self.fact_repository = fact_repository
        self.material_repository = material_repository
        self.case_repository = case_repository

    def extract_facts(self, case_id: str) -> list[Fact]:
        if self.case_repository.get_by_case_id(case_id) is None:
            raise ValueError("case not found")

        materials = self.material_repository.list_by_case_id(case_id)
        facts: list[Fact] = []

        for material in materials:
            facts.extend(self._extract_material_facts(material))

        return facts

    def list_facts(self, case_id: str) -> list[Fact]:
        if self.case_repository.get_by_case_id(case_id) is None:
            raise ValueError("case not found")
        return self.fact_repository.list_by_case_id(case_id)

    def _extract_material_facts(self, material: Material) -> list[Fact]:
        material_path = Path(material.storage_path)
        if not material_path.exists():
            return [
                self.fact_repository.create(
                    fact_id=self.fact_repository.next_fact_id(),
                    case_id=material.case_id,
                    material_id=material.material_id,
                    content=f"Material file not found: {material.filename}",
                    fact_type="material_file_missing",
                    confidence=0.0,
                    source_text=str(material_path),
                    status="skipped"
                )
            ]

        text = material_path.read_text(encoding="utf-8", errors="ignore").strip()
        if not text:
            return [
                self.fact_repository.create(
                    fact_id=self.fact_repository.next_fact_id(),
                    case_id=material.case_id,
                    material_id=material.material_id,
                    content=f"Material file is empty: {material.filename}",
                    fact_type="material_empty",
                    confidence=0.0,
                    source_text=str(material_path),
                    status="skipped"
                )
            ]

        statements = self._split_text_into_statements(text)
        return [
            self.fact_repository.create(
                fact_id=self.fact_repository.next_fact_id(),
                case_id=material.case_id,
                material_id=material.material_id,
                content=statement,
                fact_type="material_statement",
                confidence=0.8,
                source_text=statement,
                status="extracted"
            )
            for statement in statements
        ]

    def _split_text_into_statements(self, text: str) -> list[str]:
        lines = [line.strip() for line in text.splitlines() if line.strip()]
        if len(lines) > 1:
            return lines
        return [text]
