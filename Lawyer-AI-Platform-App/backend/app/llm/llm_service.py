from app.core.config import settings
from app.llm.base import LLMClient, LLMResponse
from app.llm.mock_client import MockLLMClient
from app.llm.openai_client import OpenAILLMClient


def get_llm_client() -> LLMClient:
    provider = settings.llm_provider.lower().strip()
    if provider == "openai":
        return OpenAILLMClient(
            api_key=settings.openai_api_key,
            model=settings.openai_model
        )
    return MockLLMClient()


def generate_text(prompt: str, context: dict | None = None) -> LLMResponse:
    client = get_llm_client()
    return client.generate(prompt=prompt, context=context)


def get_llm_status() -> dict[str, object]:
    client = get_llm_client()
    configured = True
    if isinstance(client, OpenAILLMClient):
        configured = client.is_configured()

    return {
        "provider": client.provider,
        "model": client.model,
        "configured": configured
    }
