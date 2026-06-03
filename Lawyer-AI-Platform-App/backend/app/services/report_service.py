import json
from pathlib import Path

from app.models.fact import Fact
from app.models.legal_analysis import LegalAnalysis
from app.models.report import Report
from app.repositories.case_repository import CaseRepository
from app.repositories.fact_repository import FactRepository
from app.repositories.legal_analysis_repository import LegalAnalysisRepository
from app.repositories.report_repository import ReportRepository
from app.services.skill_runtime_service import SkillRuntimeService


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

    def generate_report(self, case_id: str) -> Report:
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
        content = self._build_report_content(
            case_id=case_id,
            title=title,
            facts=facts,
            analysis=latest_analysis,
            runtime_context=runtime_context
        )
        storage_path = self._write_report_file(
            case_id=case_id,
            report_id=report_id,
            content=content
        )
        source_refs = {
            "fact_ids": [fact.fact_id for fact in facts],
            "analysis_id": latest_analysis.analysis_id
        }
        if runtime_context is not None:
            source_refs["skill_id"] = self._runtime_value(runtime_context, "skill_id")
            source_refs["package_id"] = self._runtime_value(runtime_context, "package_id")

        return self.report_repository.create(
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
            f"- Rule: {rule.get('rule', '')} Source: {rule.get('source', 'unknown')}"
            for rule in rules
        ] or ["- No rules were generated."]
        reasoning_lines = [f"- Reasoning: {item}" for item in reasoning] or ["- No reasoning was generated."]
        return "\n".join(rule_lines + reasoning_lines)

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
