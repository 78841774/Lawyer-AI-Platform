from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    app_name: str = "Lawyer AI Platform API"
    app_version: str = "2.5.0"
    database_url: str = "sqlite:///./local.db"
    storage_root: str = "../storage"
    llm_provider: str = "mock"
    openai_model: str = "gpt-4o-mini"
    openai_api_key: str = ""


settings = Settings()
