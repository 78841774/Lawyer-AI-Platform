import os
from typing import Any

from app.llm.base import LLMResponse


class OpenAILLMClient:
    provider = "openai"

    def __init__(
        self,
        *,
        api_key: str | None = None,
        model: str | None = None
    ) -> None:
        self.api_key = api_key if api_key is not None else os.getenv("OPENAI_API_KEY")
        self.model = model or os.getenv("OPENAI_MODEL") or "gpt-4o-mini"

    def generate(self, prompt: str, context: dict | None = None) -> LLMResponse:
        if not self.api_key:
            return self._error_response("OPENAI_API_KEY not configured")

        try:
            from openai import OpenAI
        except ImportError:
            return self._error_response("OpenAI SDK not installed")

        try:
            client = OpenAI(api_key=self.api_key)
            response = client.responses.create(
                model=self.model,
                input=self._build_input(prompt=prompt, context=context)
            )
            output = getattr(response, "output_text", "")
            usage = self._extract_usage(response)
        except Exception as error:
            return self._error_response(str(error))

        return {
            "provider": self.provider,
            "model": self.model,
            "output": output,
            "usage": usage,
            "status": "success"
        }

    def is_configured(self) -> bool:
        return bool(self.api_key)

    def _build_input(self, *, prompt: str, context: dict | None) -> str:
        if not context:
            return prompt
        return f"{prompt}\n\nContext:\n{context}"

    def _extract_usage(self, response: Any) -> dict[str, int]:
        usage = getattr(response, "usage", None)
        if usage is None:
            return {"input_tokens": 0, "output_tokens": 0}

        input_tokens = getattr(usage, "input_tokens", 0) or 0
        output_tokens = getattr(usage, "output_tokens", 0) or 0
        return {
            "input_tokens": int(input_tokens),
            "output_tokens": int(output_tokens)
        }

    def _error_response(self, message: str) -> LLMResponse:
        return {
            "provider": self.provider,
            "model": self.model,
            "output": message,
            "usage": {
                "input_tokens": 0,
                "output_tokens": 0
            },
            "status": "error"
        }
