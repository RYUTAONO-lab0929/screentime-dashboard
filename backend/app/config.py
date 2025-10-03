from typing import List, Optional
from pydantic import Field, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "Screentime Dashboard API"
    environment: str = "development"
    database_url: str = "sqlite:///backend/dev.db"
    timezone: str = "Asia/Tokyo"
    cors_origins: List[str] = [
        "http://localhost:5173",
        "http://127.0.0.1:5173",
        "http://localhost",
        "http://127.0.0.1",
    ]

    # Ingest 認証
    hmac_secret: str = "change-me"
    ingest_tokens: List[str] = Field(default_factory=list)

    # OIDC/Magic Link（必要に応じて設定）
    oidc_issuer_url: Optional[str] = None
    oidc_client_id: Optional[str] = None
    oidc_audience: Optional[str] = None
    magic_link_enabled: bool = True

    access_log: bool = True

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    @field_validator("ingest_tokens", mode="before")
    @classmethod
    def _split_tokens(cls, v):
        if isinstance(v, str):
            return [t.strip() for t in v.split(",") if t.strip()]
        return v or []
