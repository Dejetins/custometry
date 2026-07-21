from pathlib import Path

import pytest
from pydantic import ValidationError

from custometry_api.config import Settings
from packages.identity_access.application.service import token_hash


def test_token_hash_is_stable_and_never_contains_secret() -> None:
    raw = "one-time-secret-value"

    digest = token_hash(raw)

    assert len(digest) == 64
    assert raw not in digest
    assert digest == token_hash(raw)


def test_bootstrap_secret_is_optional_and_file_backed(tmp_path: Path) -> None:
    missing = Settings(bootstrap_token_file=None)
    assert missing.read_bootstrap_token() is None

    secret_file = tmp_path / "bootstrap-token"
    secret_file.write_text("local-one-time-token\n", encoding="utf-8")
    configured = Settings(bootstrap_token_file=secret_file)
    assert configured.read_bootstrap_token() == "local-one-time-token"


def test_credentialed_cors_rejects_wildcard() -> None:
    with pytest.raises(ValidationError, match="wildcard CORS origin"):
        Settings(cors_allowed_origins=["*"])
