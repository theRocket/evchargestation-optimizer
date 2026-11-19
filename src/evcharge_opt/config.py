from pathlib import Path
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    nrel_api_key: str = "DEMO_KEY"
    default_h3_resolution: int = 7
    cross_border_buffer_km: float = 25.0
    data_dir: Path = Path("data")


settings = Settings()
