from dataclasses import dataclass


@dataclass(frozen=True)
class MetricResult:
    name: str
    score: float
    reason: str


class EvaluationMetrics:
    def score_fact_pattern_quality(
        self,
        fact_patterns: list[dict[str, object]]
    ) -> MetricResult:
        if not fact_patterns:
            return MetricResult(
                "fact_pattern_quality",
                0.0,
                "No fact patterns are available."
            )

        has_inventory = any(
            pattern.get("pattern") == "case_fact_inventory"
            for pattern in fact_patterns
        )
        has_evidence_map = any(
            pattern.get("pattern") == "evidence_mapping"
            for pattern in fact_patterns
        )
        has_fact_count = any(
            int(pattern.get("fact_count", 0) or 0) > 0
            for pattern in fact_patterns
        )

        score = 0.4
        if has_inventory:
            score += 0.2
        if has_evidence_map:
            score += 0.1
        if has_fact_count:
            score += 0.1

        return MetricResult(
            "fact_pattern_quality",
            round(min(score, 0.8), 2),
            "Fact patterns include an inventory and evidence mapping."
        )

    def score_reasoning_quality(
        self,
        reasoning_patterns: list[dict[str, object]]
    ) -> MetricResult:
        if not reasoning_patterns:
            return MetricResult(
                "reasoning_quality",
                0.0,
                "No reasoning patterns are available."
            )

        has_issues = any(pattern.get("issues") for pattern in reasoning_patterns)
        has_rules = any(pattern.get("rules") for pattern in reasoning_patterns)
        has_steps = any(pattern.get("reasoning_steps") for pattern in reasoning_patterns)
        has_conclusion = any(pattern.get("conclusion") for pattern in reasoning_patterns)

        score = 0.35
        if has_issues:
            score += 0.15
        if has_rules:
            score += 0.15
        if has_steps:
            score += 0.1
        if has_conclusion:
            score += 0.1

        return MetricResult(
            "reasoning_quality",
            round(min(score, 0.85), 2),
            "Reasoning patterns include issues, rules, reasoning steps, and conclusion."
        )

    def score_prompt_quality(self, prompts: dict[str, str]) -> MetricResult:
        required = {"fact_prompt", "analysis_prompt", "report_prompt"}
        present = {key for key in required if prompts.get(key)}
        if not present:
            return MetricResult(
                "prompt_quality",
                0.0,
                "No required prompts are available."
            )

        prompt_text = "\n".join(prompts.values()).lower()
        score = 0.25 + (len(present) / len(required)) * 0.35
        if "do not invent" in prompt_text or "unsupported" in prompt_text:
            score += 0.1
        if "output" in prompt_text or "sections" in prompt_text:
            score += 0.1

        return MetricResult(
            "prompt_quality",
            round(min(score, 0.8), 2),
            "Required prompts exist and include guardrails for evidence and report structure."
        )

    def score_template_quality(self, templates: dict[str, str]) -> MetricResult:
        template = templates.get("report_template", "")
        if not template:
            return MetricResult(
                "template_quality",
                0.0,
                "No report template is available."
            )

        section_count = template.count("## ")
        score = 0.35
        if "# " in template:
            score += 0.1
        if section_count >= 4:
            score += 0.2
        if "Risk" in template or "风险" in template:
            score += 0.1

        return MetricResult(
            "template_quality",
            round(min(score, 0.75), 2),
            "Report template has a title, reusable sections, and risk assessment structure."
        )

    def score_legal_relevance(
        self,
        *,
        domain: str,
        reasoning_patterns: list[dict[str, object]]
    ) -> MetricResult:
        if not reasoning_patterns:
            return MetricResult(
                "legal_relevance",
                0.0,
                "No reasoning patterns are available for legal relevance scoring."
            )

        has_legal_issue = any(pattern.get("issues") for pattern in reasoning_patterns)
        has_rule = any(pattern.get("rules") for pattern in reasoning_patterns)
        has_risk = any(pattern.get("risk_level") for pattern in reasoning_patterns)

        score = 0.4
        if domain:
            score += 0.1
        if has_legal_issue:
            score += 0.15
        if has_rule:
            score += 0.1
        if has_risk:
            score += 0.1

        return MetricResult(
            "legal_relevance",
            round(min(score, 0.85), 2),
            "Skill remains tied to legal issues, rules, and risk assessment."
        )

    def score_report_reusability(
        self,
        templates: dict[str, str],
        prompts: dict[str, str]
    ) -> MetricResult:
        template = templates.get("report_template", "")
        report_prompt = prompts.get("report_prompt", "")
        if not template and not report_prompt:
            return MetricResult(
                "report_reusability",
                0.0,
                "No report template or report prompt is available."
            )

        reusable_sections = [
            "Executive Summary",
            "Fact Patterns",
            "Legal Issues",
            "Reasoning Patterns",
            "Risk Assessment"
        ]
        present_sections = sum(1 for section in reusable_sections if section in template)
        score = 0.35 + (present_sections / len(reusable_sections)) * 0.35
        if "lawyer-reviewable" in report_prompt or "professional" in report_prompt:
            score += 0.2

        return MetricResult(
            "report_reusability",
            round(min(score, 0.9), 2),
            "Report prompt and template can be reused across similar cases."
        )

