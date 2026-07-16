from dataclasses import dataclass
import json
from pathlib import Path

from fastapi.testclient import TestClient

from custometry_api.config import Settings
from custometry_api.main import create_app


@dataclass(frozen=True)
class StaticProbe:
    ready: bool

    def is_ready(self) -> bool:
        return self.ready


def test_liveness_does_not_depend_on_postgresql(tmp_path: Path) -> None:
    settings = Settings(
        version="test-version",
        database_password_file=tmp_path / "missing-secret",
    )
    with TestClient(create_app(settings=settings, readiness_probe=StaticProbe(False))) as client:
        response = client.get("/health/live")

    assert response.status_code == 200
    assert response.json() == {
        "status": "ok",
        "service": "api",
        "version": "test-version",
        "code": None,
    }
    assert response.headers["cache-control"] == "no-store"


def test_readiness_returns_stable_safe_failure() -> None:
    settings = Settings(version="test-version")
    with TestClient(create_app(settings=settings, readiness_probe=StaticProbe(False))) as client:
        response = client.get("/health/ready")

    assert response.status_code == 503
    assert response.json() == {
        "status": "not_ready",
        "service": "api",
        "version": "test-version",
        "code": "DEPENDENCY_UNAVAILABLE",
    }
    assert "postgres" not in response.text.lower()


def test_version_is_explicit() -> None:
    settings = Settings(version="2026.7.16-test")
    with TestClient(create_app(settings=settings, readiness_probe=StaticProbe(True))) as client:
        response = client.get("/version")

    assert response.status_code == 200
    assert response.json() == {"service": "api", "version": "2026.7.16-test"}


def test_openapi_provider_matches_committed_contract() -> None:
    repository_root = Path(__file__).resolve().parents[2]
    committed_path = repository_root / "packages/contracts/openapi/foundation.openapi.json"
    committed = json.loads(committed_path.read_text(encoding="utf-8"))
    generated = create_app(
        settings=Settings(version="0.1.0-dev.0"),
        readiness_probe=StaticProbe(True),
    ).openapi()

    assert generated == committed
