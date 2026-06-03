from app.llm.base import LLMResponse


class MockLLMClient:
    provider = "mock"

    def __init__(self, model: str = "mock-legal-runtime") -> None:
        self.model = model

    def generate(self, prompt: str, context: dict | None = None) -> LLMResponse:
        output = self._build_output(prompt=prompt, context=context)
        return {
            "provider": self.provider,
            "model": self.model,
            "output": output,
            "usage": {
                "input_tokens": self._estimate_tokens(prompt),
                "output_tokens": self._estimate_tokens(output)
            },
            "status": "success"
        }

    def _build_output(self, *, prompt: str, context: dict | None) -> str:
        if context and context.get("runtime_metadata", {}).get("task") == "fact_extraction":
            material_content = str(context.get("material_content") or "").strip()
            first_line = next(
                (line.strip() for line in material_content.splitlines() if line.strip()),
                material_content
            )
            if first_line:
                return f"Extracted fact: {first_line[:240]}"

        if context and context.get("runtime_metadata", {}).get("task") == "legal_analysis":
            return (
                "Legal issue: 是否存在可分析的法律事实. "
                "Conclusion: 案件具备初步法律分析条件."
            )

        if context and context.get("runtime_metadata", {}).get("task") == "report_generation":
            skill = context.get("skill")
            skill_lines: list[str] = []
            if isinstance(skill, dict) and skill.get("skill_id"):
                package = context.get("package")
                package_id = package.get("package_id") if isinstance(package, dict) else None
                skill_lines = [
                    f"Skill Used: {skill.get('skill_name')}",
                    f"Skill ID: {skill.get('skill_id')}",
                    f"Package ID: {package_id}"
                ]
            return "\n".join(
                [
                    "# Preliminary Legal Report",
                    "",
                    *skill_lines,
                    "",
                    "## Executive Summary",
                    "The mock LLM generated a preliminary legal report from the available facts and legal analysis.",
                    "",
                    "## Facts Summary",
                    "The case facts were reviewed and summarized for legal analysis.",
                    "",
                    "## Legal Issues",
                    "是否存在可分析的法律事实",
                    "",
                    "## Legal Analysis",
                    "The configured LLM adapter evaluated facts, rules, reasoning, and the latest analysis record.",
                    "",
                    "## Preliminary Conclusion",
                    "案件具备初步法律分析条件."
                ]
            )

        clean_prompt = " ".join(prompt.strip().split())
        if not clean_prompt:
            return "Mock LLM response: no prompt provided."

        context_keys = sorted((context or {}).keys())
        context_note = ""
        if context_keys:
            context_note = f" Context keys: {', '.join(context_keys)}."

        return f"Mock LLM response for legal runtime: {clean_prompt[:240]}{context_note}"

    def _estimate_tokens(self, text: str) -> int:
        if not text:
            return 0
        return max(1, len(text.split()))
