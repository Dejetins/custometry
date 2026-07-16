"""Alembic environment for the control-plane PostgreSQL schema."""

from logging.config import fileConfig

from alembic import context
from sqlalchemy import URL, create_engine, pool

from custometry_api.config import Settings

config = context.config
if config.config_file_name is not None:
    fileConfig(config.config_file_name)


def database_url(settings: Settings | None = None) -> URL:
    runtime_settings = settings or Settings()
    return URL.create(
        drivername="postgresql+psycopg",
        username=runtime_settings.database_user,
        password=runtime_settings.read_database_password(),
        host=runtime_settings.database_host,
        port=runtime_settings.database_port,
        database=runtime_settings.database_name,
    )


def run_migrations_offline() -> None:
    # Offline SQL generation does not need a credential-bearing URL.
    context.configure(
        url=database_url().render_as_string(hide_password=True),
        target_metadata=None,
        literal_binds=True,
    )
    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    connectable = create_engine(database_url(), poolclass=pool.NullPool)
    with connectable.connect() as connection:
        context.configure(connection=connection, target_metadata=None)
        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
