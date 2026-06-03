from app.core.config import settings
from app.llm.base import LLMClient, LLMResponse
from app.llm.deepseek_client import DeepSeekLLMClient
from app.llm.mock_client import MockLLMClient
from app.llm.openai_client import OpenAILLMClient


def get_llm_client() -> LLMClient:
    provider = settings.llm_provider.lower().strip()
    if provider == "deepseek":
        return DeepSeekLLMClient(
            api_key=settings.deepseek_api_key,
            model=settings.deepseek_model,
            base_url=settings.deepseek_base_url,
            timeout_seconds=settings.deepseek_timeout_seconds
        )
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
    base_url_configured = False
    if isinstance(client, DeepSeekLLMClient):
        configured = client.is_configured()
        base_url_configured = client.is_base_url_configured()
    if isinstance(client, OpenAILLMClient):
        configured = client.is_configured()

    return {
        "provider": client.provider,
        "model": client.model,
        "configured": configured,
        "base_url_configured": base_url_configured
    }
