import json
import os
import re
from typing import Any

from app.llm.base import LLMResponse


class DeepSeekLLMClient:
    provider = "deepseek"

    def __init__(
        self,
        *,
        api_key: str | None = None,
        model: str | None = None,
        base_url: str | None = None,
        timeout_seconds: int | float | str | None = None
    ) -> None:
        self.api_key = api_key if api_key is not None else os.getenv("DEEPSEEK_API_KEY")
        self.model = model or os.getenv("DEEPSEEK_MODEL") or "deepseek-chat"
        self.base_url = base_url or os.getenv("DEEPSEEK_BASE_URL") or "https://api.deepseek.com"
        self.timeout_seconds = self._coerce_timeout(
            timeout_seconds if timeout_seconds is not None else os.getenv("DEEPSEEK_TIMEOUT_SECONDS")
        )

    def generate(self, prompt: str, context: dict | None = None) -> LLMResponse:
        if not self.api_key:
            return self._error_response("DEEPSEEK_API_KEY not configured")

        try:
            from openai import OpenAI
        except ImportError:
            return self._error_response("OpenAI SDK not installed")

        try:
            client = OpenAI(
                api_key=self.api_key,
                base_url=self.base_url,
                timeout=self.timeout_seconds
            )
            response = client.chat.completions.create(
                model=self.model,
                messages=self._build_messages(prompt=prompt, context=context)
            )
            output = self._extract_output(response)
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

    def is_base_url_configured(self) -> bool:
        return bool(self.base_url)

    def _build_messages(self, *, prompt: str, context: dict | None) -> list[dict[str, str]]:
        user_content = prompt
        if context:
            user_content = (
                f"{prompt}\n\nContext:\n"
                f"{json.dumps(context, ensure_ascii=False, default=str)}"
            )

        return [
            {
                "role": "system",
                "content": "You are a legal AI assistant. Return concise, useful legal workflow output."
            },
            {
                "role": "user",
                "content": user_content
            }
        ]

    def _extract_output(self, response: Any) -> str:
        choices = self._get_value(response, "choices", [])
        if not choices:
            return ""

        first_choice = choices[0]
        message = self._get_value(first_choice, "message", None)
        content = self._get_value(message, "content", "")
        return content or ""

    def _extract_usage(self, response: Any) -> dict[str, int]:
        usage = self._get_value(response, "usage", None)
        if usage is None:
            return {"input_tokens": 0, "output_tokens": 0}

        input_tokens = self._get_value(usage, "prompt_tokens", 0) or 0
        output_tokens = self._get_value(usage, "completion_tokens", 0) or 0
        return {
            "input_tokens": int(input_tokens),
            "output_tokens": int(output_tokens)
        }

    def _get_value(self, target: Any, key: str, default: Any) -> Any:
        if isinstance(target, dict):
            return target.get(key, default)
        return getattr(target, key, default)

    def _coerce_timeout(self, timeout_seconds: int | float | str | None) -> float:
        if timeout_seconds in (None, ""):
            return 30.0

        try:
            timeout = float(timeout_seconds)
        except (TypeError, ValueError):
            return 30.0

        return timeout if timeout > 0 else 30.0

    def _error_response(self, message: str) -> LLMResponse:
        return {
            "provider": self.provider,
            "model": self.model,
            "output": "",
            "usage": {
                "input_tokens": 0,
                "output_tokens": 0
            },
            "status": "error",
            "error": self._sanitize_error(message)
        }

    def _sanitize_error(self, message: str) -> str:
        sanitized = message or "DeepSeek request failed"
        if self.api_key:
            sanitized = sanitized.replace(self.api_key, "[redacted]")

        sanitized = re.sub(
            r"(?i)(api[_-]?key|authorization|bearer)\s*[:=]\s*['\"]?[^'\"\s,]+",
            r"\1=[redacted]",
            sanitized
        )
        sanitized = re.sub(r"sk-[A-Za-z0-9_\-]{8,}", "[redacted]", sanitized)
        return sanitized
