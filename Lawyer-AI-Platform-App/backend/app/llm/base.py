from typing import Protocol


LLMResponse = dict[str, object]


class LLMClient(Protocol):
    provider: str
    model: str

    def generate(self, prompt: str, context: dict | None = None) -> LLMResponse:
        ...
