"""Foundation runtime configuration.

Secrets are resolved from files at the composition root. They are never included
in API responses or diagnostic messages.
"""

from pathlib import Path

from pydantic import Field, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Non-secret settings plus a reference to the database secret file."""

    model_config = SettingsConfigDict(env_prefix="CUSTOMETRY_", extra="ignore")

    version: str = "0.1.0-dev.0"
    environment: str = "development"
    database_host: str = "control-db"
    database_port: int = Field(default=5432, ge=1, le=65535)
    database_name: str = "custometry"
    database_user: str = "custometry"
    database_password_file: Path = Path("/run/secrets/control_db_password")
    database_connect_timeout_seconds: int = Field(default=2, ge=1, le=10)
    bootstrap_token_file: Path | None = None
    cors_allowed_origins: list[str] = ["http://127.0.0.1:5173"]
    identity_cookie_secure: bool = True
    identity_access_ttl_seconds: int = Field(default=900, ge=60, le=3600)
    identity_refresh_ttl_seconds: int = Field(default=2_592_000, ge=3600, le=7_776_000)
    identity_rate_limit_requests: int = Field(default=20, ge=1, le=1000)
    identity_rate_limit_window_seconds: int = Field(default=60, ge=1, le=3600)

    @field_validator("cors_allowed_origins")
    @classmethod
    def reject_credentialed_wildcard(cls, value: list[str]) -> list[str]:
        """Credentialed browser auth must never combine with a wildcard origin."""

        if "*" in value:
            raise ValueError("wildcard CORS origin is forbidden with credentials")
        return value

    def read_database_password(self) -> str:
        """Read the password just in time without retaining it in settings dumps."""

        password = self.database_password_file.read_text(encoding="utf-8").strip()
        if not password:
            raise ValueError("database password file is empty")
        return password

    def read_bootstrap_token(self) -> str | None:
        """Read the one-time deployment bootstrap token when explicitly configured."""

        if self.bootstrap_token_file is None:
            return None
        token = self.bootstrap_token_file.read_text(encoding="utf-8").strip()
        if not token:
            raise ValueError("bootstrap token file is empty")
        return token
