import json
from dataclasses import dataclass
from pathlib import Path

from app.llm.llm_service import generate_text
from app.llm.prompt_context import PromptContextBuilder
from app.models.case import Case
from app.models.fact import Fact
from app.models.legal_analysis import LegalAnalysis
from app.models.report import Report
from app.repositories.case_repository import CaseRepository
from app.repositories.fact_repository import FactRepository
from app.repositories.legal_analysis_repository import LegalAnalysisRepository
from app.repositories.report_repository import ReportRepository
from app.services.skill_runtime_service import SkillRuntimeService


@dataclass(frozen=True)
class ReportGenerationResult:
    report: Report
    skill_used: str | None = None
    package_used: str | None = None
    llm_provider: str | None = None
    llm_status: str | None = None


class ReportService:
    def __init__(
        self,
        *,
        report_repository: ReportRepository,
        fact_repository: FactRepository,
        legal_analysis_repository: LegalAnalysisRepository,
        case_repository: CaseRepository,
        storage_root: str,
        skill_runtime_service: SkillRuntimeService | None = None
    ) -> None:
        self.report_repository = report_repository
        self.fact_repository = fact_repository
        self.legal_analysis_repository = legal_analysis_repository
        self.case_repository = case_repository
        self.storage_root = Path(storage_root)
        self.skill_runtime_service = skill_runtime_service
        self.prompt_context_builder = PromptContextBuilder()

    def generate_report(self, case_id: str) -> Report:
        return self.generate_report_with_runtime(case_id).report

    def generate_report_with_runtime(self, case_id: str) -> ReportGenerationResult:
        case = self.case_repository.get_by_case_id(case_id)
        if case is None:
            raise ValueError("case not found")

        facts = self.fact_repository.list_by_case_id(case_id)
        if not facts:
            raise ValueError("facts required")

        analyses = self.legal_analysis_repository.list_by_case_id(case_id)
        if not analyses:
            raise ValueError("analysis required")

        runtime_context = self._get_runtime_context(case_id)
        latest_analysis = analyses[-1]
        report_id = self.report_repository.next_report_id()
        version = self.report_repository.next_version(case_id)
        title = f"Preliminary Legal Report - {case.title}"
        fallback_content = self._build_report_content(
            case_id=case_id,
            title=title,
            facts=facts,
            analysis=latest_analysis,
            runtime_context=runtime_context
        )
        llm_response = self._generate_llm_report(
            case=case,
            facts=facts,
            latest_analysis=latest_analysis,
            runtime_context=runtime_context
        )
        llm_output = str(llm_response.get("output") or "")
        content = self._finalize_llm_content(
            llm_output=llm_output,
            fallback_content=fallback_content,
            runtime_context=runtime_context
        )
        storage_path = self._write_report_file(
            case_id=case_id,
            report_id=report_id,
            content=content
        )
        llm_provider = self._response_value(llm_response, "provider")
        llm_status = self._response_value(llm_response, "status")
        source_refs = {
            "fact_ids": [fact.fact_id for fact in facts],
            "analysis_id": latest_analysis.analysis_id,
            "llm_provider": llm_provider,
            "llm_status": llm_status
        }
        if runtime_context is not None:
            source_refs["skill_id"] = self._runtime_value(runtime_context, "skill_id")
            source_refs["package_id"] = self._runtime_value(runtime_context, "package_id")

        report = self.report_repository.create(
            report_id=report_id,
            case_id=case_id,
            report_type="preliminary_legal_report",
            title=title,
            content=content,
            status="generated",
            version=version,
            storage_path=str(storage_path),
            source_refs=json.dumps(source_refs, ensure_ascii=False)
        )
        return ReportGenerationResult(
            report=report,
            skill_used=self._runtime_value(runtime_context, "skill_id"),
            package_used=self._runtime_value(runtime_context, "package_id"),
            llm_provider=llm_provider,
            llm_status=llm_status
        )

    def list_reports(self, case_id: str) -> list[Report]:
        if self.case_repository.get_by_case_id(case_id) is None:
            raise ValueError("case not found")
        return self.report_repository.list_by_case_id(case_id)

    def _write_report_file(self, *, case_id: str, report_id: str, content: str) -> Path:
        target_dir = self.storage_root / "reports" / case_id
        target_dir.mkdir(parents=True, exist_ok=True)
        target_path = target_dir / f"{report_id}.md"
        target_path.write_text(content, encoding="utf-8")
        return target_path

    def _build_report_content(
        self,
        *,
        case_id: str,
        title: str,
        facts: list[Fact],
        analysis: LegalAnalysis,
        runtime_context: dict[str, object] | None = None
    ) -> str:
        issues = json.loads(analysis.issues)
        rules = json.loads(analysis.rules)
        reasoning = json.loads(analysis.reasoning)
        extracted_facts = [fact for fact in facts if fact.status == "extracted"]

        return "\n".join(
            [
                f"# {title}",
                "",
                f"Case ID: {case_id}",
                f"Analysis ID: {analysis.analysis_id}",
                *self._format_skill_used(runtime_context),
                "",
                "## Executive Summary",
                f"The system generated a preliminary legal report from {len(extracted_facts)} extracted facts and the latest legal analysis.",
                f"Current conclusion: {analysis.conclusion}",
                f"Risk level: {analysis.risk_level}. Confidence: {analysis.confidence}.",
                "",
                "## Facts Summary",
                self._format_facts(extracted_facts),
                "",
                "## Legal Issues",
                self._format_issues(issues),
                "",
                "## Legal Analysis",
                self._format_rules_and_reasoning(rules, reasoning),
                "",
                "## Preliminary Conclusion",
                analysis.conclusion,
                ""
            ]
        )

    def _generate_llm_report(
        self,
        *,
        case: Case,
        facts: list[Fact],
        latest_analysis: LegalAnalysis,
        runtime_context: dict[str, object] | None
    ) -> dict[str, object]:
        prompt = self._build_report_prompt(
            case=case,
            facts=facts,
            latest_analysis=latest_analysis,
            runtime_context=runtime_context
        )
        context = self._build_llm_context(
            case=case,
            facts=facts,
            latest_analysis=latest_analysis,
            runtime_context=runtime_context
        )
        response = generate_text(prompt=prompt, context=context)
        if response.get("status") != "success":
            raise ValueError("llm generation failed")
        return response

    def _build_report_prompt(
        self,
        *,
        case: Case,
        facts: list[Fact],
        latest_analysis: LegalAnalysis,
        runtime_context: dict[str, object] | None
    ) -> str:
        report_prompt = self._get_prompt(runtime_context, "report")
        report_template = self._get_template(runtime_context, "report")
        if not report_prompt:
            report_prompt = (
                "Generate a preliminary legal report. Include Executive Summary, Facts Summary, "
                "Legal Issues, Legal Analysis, and Preliminary Conclusion sections."
            )

        fact_lines = [
            f"- {fact.fact_id}: {fact.content} (type: {fact.fact_type}, status: {fact.status})"
            for fact in facts
        ]
        return "\n".join(
            [
                report_prompt,
                "",
                "Case metadata:",
                f"- case_id: {case.case_id}",
                f"- title: {case.title}",
                f"- case_type: {case.case_type}",
                f"- objective: {case.objective or ''}",
                f"- skill_domain: {self._runtime_value(runtime_context, 'domain') or 'none'}",
                "",
                "Facts:",
                *fact_lines,
                "",
                "Latest legal analysis:",
                f"- analysis_id: {latest_analysis.analysis_id}",
                f"- conclusion: {latest_analysis.conclusion}",
                f"- risk_level: {latest_analysis.risk_level}",
                f"- confidence: {latest_analysis.confidence}",
                "",
                "Report template:",
                report_template or "Use the required report sections."
            ]
        )

    def _build_llm_context(
        self,
        *,
        case: Case,
        facts: list[Fact],
        latest_analysis: LegalAnalysis,
        runtime_context: dict[str, object] | None
    ) -> dict[str, object]:
        return self.prompt_context_builder.build(
            case=case,
            facts=facts,
            analysis=latest_analysis,
            skill=self._build_skill_context(runtime_context),
            package=self._build_package_context(runtime_context),
            runtime_metadata={
                "task": "report_generation",
                "skill_used": self._runtime_value(runtime_context, "skill_id"),
                "package_used": self._runtime_value(runtime_context, "package_id")
            }
        )

    def _finalize_llm_content(
        self,
        *,
        llm_output: str,
        fallback_content: str,
        runtime_context: dict[str, object] | None
    ) -> str:
        if not self._is_complete_report(llm_output):
            return fallback_content
        if runtime_context is not None and not self._has_skill_used_block(llm_output):
            return "\n".join(
                [
                    llm_output.rstrip(),
                    "",
                    *self._format_skill_used(runtime_context),
                    ""
                ]
            )
        return llm_output

    def _is_complete_report(self, content: str) -> bool:
        required_sections = [
            "## Executive Summary",
            "## Facts Summary",
            "## Legal Issues",
            "## Legal Analysis",
            "## Preliminary Conclusion"
        ]
        return all(section in content for section in required_sections)

    def _has_skill_used_block(self, content: str) -> bool:
        return (
            "Skill Used:" in content
            and "Skill ID:" in content
            and "Package ID:" in content
        )

    def _format_facts(self, facts: list[Fact]) -> str:
        if not facts:
            return "- No extracted facts are currently available."
        return "\n".join(f"- {fact.content}" for fact in facts)

    def _format_issues(self, issues: list[dict[str, object]]) -> str:
        if not issues:
            return "- No legal issues were identified."
        return "\n".join(
            f"- {issue.get('issue', 'Unspecified issue')} (confidence: {issue.get('confidence', 'n/a')})"
            for issue in issues
        )

    def _format_rules_and_reasoning(
        self,
        rules: list[dict[str, object]],
        reasoning: list[str]
    ) -> str:
        rule_lines = [
            f"- Rule: {self._format_rule_text(rule)} Source: {rule.get('source', 'unknown')}"
            for rule in rules
        ] or ["- No rules were generated."]
        reasoning_lines = [f"- Reasoning: {item}" for item in reasoning] or ["- No reasoning was generated."]
        return "\n".join(rule_lines + reasoning_lines)

    def _format_rule_text(self, rule: dict[str, object]) -> str:
        rule_text = str(rule.get("rule") or "").strip()
        if rule_text:
            return rule_text
        if rule.get("source") == "Experience Package":
            return "Skill package rule context loaded from Experience Package"
        return ""

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

    def _get_template(
        self,
        runtime_context: dict[str, object] | None,
        key: str
    ) -> str | None:
        if runtime_context is None:
            return None
        templates = runtime_context.get("templates")
        if not isinstance(templates, dict):
            return None
        template = templates.get(key)
        if template is None:
            return None
        return str(template)

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

    def _format_skill_used(self, runtime_context: dict[str, object] | None) -> list[str]:
        if runtime_context is None:
            return []
        skill_name = self._runtime_value(runtime_context, "skill_name")
        skill_id = self._runtime_value(runtime_context, "skill_id")
        package_id = self._runtime_value(runtime_context, "package_id")
        return [
            f"Skill Used: {skill_name}",
            f"Skill ID: {skill_id}",
            f"Package ID: {package_id}"
        ]
