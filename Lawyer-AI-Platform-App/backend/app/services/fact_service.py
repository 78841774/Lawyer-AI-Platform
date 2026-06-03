from dataclasses import dataclass
from pathlib import Path

from app.models.fact import Fact
from app.models.material import Material
from app.repositories.case_repository import CaseRepository
from app.repositories.fact_repository import FactRepository
from app.repositories.material_repository import MaterialRepository
from app.services.skill_runtime_service import SkillRuntimeService


@dataclass(frozen=True)
class FactExtractionResult:
    facts: list[Fact]
    skill_used: str | None = None
    package_used: str | None = None


class FactService:
    def __init__(
        self,
        *,
        fact_repository: FactRepository,
        material_repository: MaterialRepository,
        case_repository: CaseRepository,
        skill_runtime_service: SkillRuntimeService | None = None
    ) -> None:
        self.fact_repository = fact_repository
        self.material_repository = material_repository
        self.case_repository = case_repository
        self.skill_runtime_service = skill_runtime_service

    def extract_facts(self, case_id: str) -> list[Fact]:
        return self.extract_facts_with_runtime(case_id).facts

    def extract_facts_with_runtime(self, case_id: str) -> FactExtractionResult:
        if self.case_repository.get_by_case_id(case_id) is None:
            raise ValueError("case not found")

        runtime_context = self._get_runtime_context(case_id)
        materials = self.material_repository.list_by_case_id(case_id)
        facts: list[Fact] = []

        for material in materials:
            facts.extend(
                self._extract_material_facts(
                    material=material,
                    runtime_context=runtime_context
                )
            )

        return FactExtractionResult(
            facts=facts,
            skill_used=self._runtime_value(runtime_context, "skill_id"),
            package_used=self._runtime_value(runtime_context, "package_id")
        )

    def list_facts(self, case_id: str) -> list[Fact]:
        if self.case_repository.get_by_case_id(case_id) is None:
            raise ValueError("case not found")
        return self.fact_repository.list_by_case_id(case_id)

    def _extract_material_facts(
        self,
        *,
        material: Material,
        runtime_context: dict[str, object] | None = None
    ) -> list[Fact]:
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
        fact_type = self._build_fact_type(runtime_context)
        return [
            self.fact_repository.create(
                fact_id=self.fact_repository.next_fact_id(),
                case_id=material.case_id,
                material_id=material.material_id,
                content=statement,
                fact_type=fact_type,
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

    def _get_runtime_context(self, case_id: str) -> dict[str, object] | None:
        if self.skill_runtime_service is None:
            return None
        return self.skill_runtime_service.get_case_runtime_context(case_id)

    def _runtime_value(
        self,
        runtime_context: dict[str, object] | None,
        key: str
    ) -> str | None:
        if runtime_context is None:
            return None
        value = runtime_context.get(key)
        if value is None:
            return None
        return str(value)

    def _build_fact_type(self, runtime_context: dict[str, object] | None) -> str:
        domain = self._runtime_value(runtime_context, "domain")
        if domain:
            return f"{domain}_fact"
        return "material_statement"
