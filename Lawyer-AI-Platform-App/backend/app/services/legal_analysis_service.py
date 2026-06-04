from dataclasses import dataclass
import json

from app.llm.llm_service import generate_text
from app.llm.prompt_context import PromptContextBuilder
from app.models.fact import Fact
from app.models.case import Case
from app.models.legal_analysis import LegalAnalysis
from app.repositories.case_repository import CaseRepository
from app.repositories.fact_repository import FactRepository
from app.repositories.legal_analysis_repository import LegalAnalysisRepository
from app.services.skill_runtime_service import SkillRuntimeService


@dataclass(frozen=True)
class LegalAnalysisRunResult:
    analysis: LegalAnalysis
    skill_used: str | None = None
    package_used: str | None = None
    llm_provider: str | None = None
    llm_status: str | None = None
    facts_count: int = 0
    source_fact_ids: list[str] | None = None
    source_refs: list[dict[str, str | None]] | None = None


class LegalAnalysisService:
    def __init__(
        self,
        *,
        legal_analysis_repository: LegalAnalysisRepository,
        fact_repository: FactRepository,
        case_repository: CaseRepository,
        skill_runtime_service: SkillRuntimeService | None = None
    ) -> None:
        self.legal_analysis_repository = legal_analysis_repository
        self.fact_repository = fact_repository
        self.case_repository = case_repository
        self.skill_runtime_service = skill_runtime_service
        self.prompt_context_builder = PromptContextBuilder()

    def run_analysis(self, case_id: str) -> LegalAnalysis:
        return self.run_analysis_with_runtime(case_id).analysis

    def run_analysis_with_runtime(self, case_id: str) -> LegalAnalysisRunResult:
        case = self.case_repository.get_by_case_id(case_id)
        if case is None:
            raise ValueError("case not found")

        runtime_context = self._get_runtime_context(case_id)
        facts = self.fact_repository.list_by_case_id(case_id)
        if not facts:
            raise ValueError("facts required")

        prompt = self._build_analysis_prompt(
            case=case,
            facts=facts,
            runtime_context=runtime_context
        )
        context = self._build_llm_context(
            case=case,
            facts=facts,
            runtime_context=runtime_context
        )
        llm_response = generate_text(prompt=prompt, context=context)
        if llm_response.get("status") != "success":
            raise ValueError("llm generation failed")

        payload = self._build_llm_analysis_payload(
            facts=facts,
            runtime_context=runtime_context,
            llm_output=str(llm_response.get("output") or "")
        )
        analysis = self.legal_analysis_repository.create(
            analysis_id=self.legal_analysis_repository.next_analysis_id(),
            case_id=case_id,
            issues=json.dumps(payload["issues"], ensure_ascii=False),
            rules=json.dumps(payload["rules"], ensure_ascii=False),
            reasoning=json.dumps(payload["reasoning"], ensure_ascii=False),
            conclusion=payload["conclusion"],
            risk_level=payload["risk_level"],
            confidence=payload["confidence"],
            status="completed"
        )
        return LegalAnalysisRunResult(
            analysis=analysis,
            skill_used=self._runtime_value(runtime_context, "skill_id"),
            package_used=self._runtime_value(runtime_context, "package_id"),
            llm_provider=self._response_value(llm_response, "provider"),
            llm_status=self._response_value(llm_response, "status"),
            facts_count=len(facts),
            source_fact_ids=[fact.fact_id for fact in facts],
            source_refs=self._build_source_refs(facts)
        )

    def list_analyses(self, case_id: str) -> list[LegalAnalysis]:
        if self.case_repository.get_by_case_id(case_id) is None:
            raise ValueError("case not found")
        return self.legal_analysis_repository.list_by_case_id(case_id)

    def _build_analysis_prompt(
        self,
        *,
        case: Case,
        facts: list[Fact],
        runtime_context: dict[str, object] | None = None
    ) -> str:
        skill_domain = self._runtime_value(runtime_context, "domain")
        analysis_prompt = self._get_prompt(runtime_context, "analysis")
        if not analysis_prompt:
            analysis_prompt = (
                "Analyze the legal facts. Return a legal issue and conclusion. "
                "Use the format: Legal issue: ... Conclusion: ..."
            )

        fact_lines = [
            f"- {fact.fact_id}: {fact.content} (type: {fact.fact_type}, status: {fact.status})"
            for fact in facts
        ]
        return "\n".join(
            [
                analysis_prompt,
                "",
                "Case metadata:",
                f"- case_id: {case.case_id}",
                f"- title: {case.title}",
                f"- case_type: {case.case_type}",
                f"- objective: {case.objective or ''}",
                f"- skill_domain: {skill_domain or 'none'}",
                "",
                "Facts:",
                *fact_lines
            ]
        )

    def _build_source_refs(self, facts: list[Fact]) -> list[dict[str, str | None]]:
        return [
            {
                "fact_id": fact.fact_id,
                "material_id": fact.material_id,
                "fact_type": fact.fact_type,
                "status": fact.status
            }
            for fact in facts
        ]

    def _build_llm_context(
        self,
        *,
        case: Case,
        facts: list[Fact],
        runtime_context: dict[str, object] | None
    ) -> dict[str, object]:
        return self.prompt_context_builder.build(
            case=case,
            facts=facts,
            skill=self._build_skill_context(runtime_context),
            package=self._build_package_context(runtime_context),
            runtime_metadata={
                "task": "legal_analysis",
                "skill_used": self._runtime_value(runtime_context, "skill_id"),
                "package_used": self._runtime_value(runtime_context, "package_id")
            }
        )

    def _build_llm_analysis_payload(
        self,
        *,
        facts: list[Fact],
        runtime_context: dict[str, object] | None,
        llm_output: str
    ) -> dict[str, object]:
        extracted_facts = [fact for fact in facts if fact.status == "extracted"]
        issue = self._parse_between(
            text=llm_output,
            start_marker="Legal issue:",
            end_marker="Conclusion:"
        ) or "是否存在可分析的法律事实"
        conclusion = self._parse_after(
            text=llm_output,
            marker="Conclusion:"
        ) or "案件具备初步法律分析条件"

        rules = [
            {
                "source": "LLM Adapter",
                "rule": "Legal analysis generated through configured LLM provider"
            }
        ]
        if runtime_context is not None:
            rules.append(
                {
                    "source": "Experience Package",
                    "skill_id": self._runtime_value(runtime_context, "skill_id"),
                    "package_id": self._runtime_value(runtime_context, "package_id"),
                    "rule": "Skill package analysis context loaded from Experience Package"
                }
            )

        return {
            "issues": [
                {
                    "issue": issue.strip(" ."),
                    "confidence": 0.8 if extracted_facts else 0.4
                }
            ],
            "rules": rules,
            "reasoning": [
                f"LLM Adapter processed {len(facts)} case facts.",
                f"{len(extracted_facts)} extracted facts were available for legal analysis.",
                f"LLM output: {llm_output}"
            ],
            "conclusion": conclusion.strip(" ."),
            "risk_level": "medium",
            "confidence": 0.75
        }

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

    def _parse_between(
        self,
        *,
        text: str,
        start_marker: str,
        end_marker: str
    ) -> str | None:
        if start_marker not in text:
            return None
        start_index = text.index(start_marker) + len(start_marker)
        end_index = text.find(end_marker, start_index)
        if end_index == -1:
            return text[start_index:].strip()
        return text[start_index:end_index].strip()

    def _parse_after(self, *, text: str, marker: str) -> str | None:
        if marker not in text:
            return None
        return text.split(marker, 1)[1].strip()
