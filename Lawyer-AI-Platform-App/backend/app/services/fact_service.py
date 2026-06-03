from dataclasses import dataclass
from pathlib import Path

from app.llm.llm_service import generate_text
from app.llm.prompt_context import PromptContextBuilder
from app.models.case import Case
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
    llm_provider: str | None = None
    llm_status: str | None = None


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
        self.prompt_context_builder = PromptContextBuilder()

    def extract_facts(self, case_id: str) -> list[Fact]:
        return self.extract_facts_with_runtime(case_id).facts

    def extract_facts_with_runtime(self, case_id: str) -> FactExtractionResult:
        case = self.case_repository.get_by_case_id(case_id)
        if case is None:
            raise ValueError("case not found")

        runtime_context = self._get_runtime_context(case_id)
        materials = self.material_repository.list_by_case_id(case_id)
        facts: list[Fact] = []
        llm_provider: str | None = None
        llm_status: str | None = None

        for material in materials:
            extracted_facts, llm_response = self._extract_material_facts(
                case=case,
                material=material,
                runtime_context=runtime_context
            )
            facts.extend(extracted_facts)
            if llm_response is not None:
                llm_provider = self._response_value(llm_response, "provider")
                llm_status = self._response_value(llm_response, "status")

        return FactExtractionResult(
            facts=facts,
            skill_used=self._runtime_value(runtime_context, "skill_id"),
            package_used=self._runtime_value(runtime_context, "package_id"),
            llm_provider=llm_provider,
            llm_status=llm_status
        )

    def list_facts(self, case_id: str) -> list[Fact]:
        if self.case_repository.get_by_case_id(case_id) is None:
            raise ValueError("case not found")
        return self.fact_repository.list_by_case_id(case_id)

    def _extract_material_facts(
        self,
        *,
        case: Case,
        material: Material,
        runtime_context: dict[str, object] | None = None
    ) -> tuple[list[Fact], dict[str, object] | None]:
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
            ], None

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
            ], None

        prompt = self._build_fact_prompt(
            case=case,
            material=material,
            material_content=text,
            runtime_context=runtime_context
        )
        context = self._build_llm_context(
            case=case,
            material=material,
            material_content=text,
            runtime_context=runtime_context
        )
        llm_response = generate_text(prompt=prompt, context=context)
        if llm_response.get("status") != "success":
            raise ValueError("llm generation failed")

        llm_output = str(llm_response.get("output") or "")
        statements = self._parse_llm_facts(llm_output)
        fact_type = self._build_fact_type(runtime_context)
        facts = [
            self.fact_repository.create(
                fact_id=self.fact_repository.next_fact_id(),
                case_id=material.case_id,
                material_id=material.material_id,
                content=statement,
                fact_type=fact_type,
                confidence=0.8,
                source_text=llm_output,
                status="extracted"
            )
            for statement in statements
        ]
        return facts, llm_response

    def _build_fact_prompt(
        self,
        *,
        case: Case,
        material: Material,
        material_content: str,
        runtime_context: dict[str, object] | None
    ) -> str:
        skill_domain = self._runtime_value(runtime_context, "domain")
        fact_prompt = self._get_prompt(runtime_context, "fact")
        if not fact_prompt:
            fact_prompt = (
                "Extract concise legal facts from the material. "
                "Return each fact as a line starting with 'Extracted fact:'."
            )

        return "\n".join(
            [
                fact_prompt,
                "",
                "Case metadata:",
                f"- case_id: {case.case_id}",
                f"- title: {case.title}",
                f"- case_type: {case.case_type}",
                f"- objective: {case.objective or ''}",
                f"- skill_domain: {skill_domain or 'none'}",
                "",
                "Material metadata:",
                f"- material_id: {material.material_id}",
                f"- filename: {material.filename}",
                "",
                "Material content:",
                material_content
            ]
        )

    def _build_llm_context(
        self,
        *,
        case: Case,
        material: Material,
        material_content: str,
        runtime_context: dict[str, object] | None
    ) -> dict[str, object]:
        context = self.prompt_context_builder.build(
            case=case,
            materials=[material],
            skill=self._build_skill_context(runtime_context),
            package=self._build_package_context(runtime_context),
            runtime_metadata={
                "task": "fact_extraction",
                "skill_used": self._runtime_value(runtime_context, "skill_id"),
                "package_used": self._runtime_value(runtime_context, "package_id")
            }
        )
        context["material_content"] = material_content
        return context

    def _parse_llm_facts(self, output: str) -> list[str]:
        facts: list[str] = []
        for line in output.splitlines():
            statement = line.strip()
            if not statement:
                continue
            if statement.lower().startswith("extracted fact:"):
                statement = statement.split(":", 1)[1].strip()
            if statement:
                facts.append(statement)

        if facts:
            return facts

        stripped_output = output.strip()
        if stripped_output:
            return [stripped_output]
        return ["No fact extracted from material."]

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

    def _response_value(self, response: dict[str, object], key: str) -> str | None:
        value = response.get(key)
        if value is None:
            return None
        return str(value)

    def _build_fact_type(self, runtime_context: dict[str, object] | None) -> str:
        domain = self._runtime_value(runtime_context, "domain")
        if domain:
            return f"{domain}_fact"
        return "material_statement"

    def _get_prompt(
        self,
        runtime_context: dict[str, object] | None,
        key: str
    ) -> str | None:
        if runtime_context is None:
            return None
        prompts = runtime_context.get("prompts")
        if not isinstance(prompts, dict):
            return None
        prompt = prompts.get(key)
        if prompt is None:
            return None
        return str(prompt)

    def _build_skill_context(
        self,
        runtime_context: dict[str, object] | None
    ) -> dict[str, object] | None:
        if runtime_context is None:
            return None
        return {
            "skill_id": self._runtime_value(runtime_context, "skill_id"),
            "skill_name": self._runtime_value(runtime_context, "skill_name"),
            "domain": self._runtime_value(runtime_context, "domain"),
            "version": self._runtime_value(runtime_context, "version")
        }

    def _build_package_context(
        self,
        runtime_context: dict[str, object] | None
    ) -> dict[str, object] | None:
        if runtime_context is None:
            return None
        return {
            "package_id": self._runtime_value(runtime_context, "package_id"),
            "domain": self._runtime_value(runtime_context, "domain"),
            "version": self._runtime_value(runtime_context, "version")
        }
