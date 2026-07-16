import importlib.util
from pathlib import Path
from types import ModuleType

from custometry_api.config import Settings
from sqlalchemy import URL


def load_migration_environment() -> ModuleType:
    root = Path(__file__).resolve().parents[2]
    path = root / "migrations/env.py"
    spec = importlib.util.spec_from_file_location("custometry_migration_env", path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    # Importing an Alembic env outside its runner executes context methods, so expose
    # only the source-level URL factory through a small compile/exec boundary.
    source = path.read_text(encoding="utf-8")
    function_source = "def database_url" + source.split(
        "def database_url", maxsplit=1
    )[1].split("def run_migrations_offline", maxsplit=1)[0]
    module.__dict__.update(Settings=Settings, URL=URL)
    exec(compile(function_source, str(path), "exec"), module.__dict__)
    return module


def test_migration_url_is_redacted_by_default(tmp_path: Path) -> None:
    secret = "foundation-secret-must-not-leak"
    password_file = tmp_path / "control-password"
    password_file.write_text(secret, encoding="utf-8")
    settings = Settings(
        database_host="db.invalid",
        database_password_file=password_file,
    )
    module = load_migration_environment()
    url = module.database_url(settings)

    assert isinstance(url, URL)
    assert secret not in str(url)
    assert "***" in str(url)
