"""Foundation runtime configuration.

Secrets are resolved from files at the composition root. They are never included
in API responses or diagnostic messages.
"""

from pathlib import Path

from pydantic import Field
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

    def read_database_password(self) -> str:
        """Read the password just in time without retaining it in settings dumps."""

        password = self.database_password_file.read_text(encoding="utf-8").strip()
        if not password:
            raise ValueError("database password file is empty")
        return password
