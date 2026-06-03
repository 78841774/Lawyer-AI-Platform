from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    app_name: str = "Lawyer AI Platform API"
    app_version: str = "3.2.0"
    app_env: str = "local"
    database_url: str = "sqlite:///./local.db"
    storage_root: str = "../storage"
    llm_provider: str = "mock"
    openai_model: str = "gpt-4o-mini"
    openai_api_key: str = ""
    deepseek_api_key: str = ""
    deepseek_model: str = "deepseek-chat"
    deepseek_base_url: str = "https://api.deepseek.com"
    deepseek_timeout_seconds: int = 30
    local_dev_token: str = "dev-local-token"
    jwt_secret_key: str = "local-dev-secret-change-me"
    jwt_algorithm: str = "HS256"
    jwt_expiration_minutes: int = 120


settings = Settings()
