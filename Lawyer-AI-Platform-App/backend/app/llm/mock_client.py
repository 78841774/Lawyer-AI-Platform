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
