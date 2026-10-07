from pydantic_settings import BaseSettings, SettingsConfigDict
class Settings(BaseSettings):
    app_name: str = "LabLedger API"
    app_version: str = "1.0.0"
    database_url: str = "sqlite:///./labledger.db"
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")
settings = Settings()
