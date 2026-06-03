from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    app_name: str = "Lawyer AI Platform API"
    app_version: str = "2.5.0"
    database_url: str = "sqlite:///./local.db"
    storage_root: str = "../storage"


settings = Settings()
