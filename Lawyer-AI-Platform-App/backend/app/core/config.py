from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    app_name: str = "Lawyer AI Platform API"
    app_version: str = "0.5.0"
    database_url: str = "postgresql://lawyer_ai:lawyer_ai@localhost:5432/lawyer_ai"
    storage_root: str = "../storage"


settings = Settings()
