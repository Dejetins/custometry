# syntax=docker/dockerfile:1.11@sha256:10c699f1b6c8bdc8f6b4ce8974855dd8542f1768c26eb240237b8f1c9c6c9976
FROM ghcr.io/astral-sh/uv:0.9.26-python3.12-bookworm-slim@sha256:add251a8fbfa14ff5e115adf93cb113c7b58c57bc84f0992164f5b6631b3451f AS build

WORKDIR /src
ENV UV_COMPILE_BYTECODE=0 \
    UV_LINK_MODE=copy \
    UV_PROJECT_ENVIRONMENT=/app/.venv

COPY pyproject.toml uv.lock README.md LICENSE ./
COPY apps/api/pyproject.toml apps/api/pyproject.toml
COPY docs-site/pyproject.toml docs-site/pyproject.toml
RUN uv sync --locked --no-dev --no-install-workspace --package custometry-api

COPY apps/api/src apps/api/src
RUN uv sync --locked --no-dev --no-editable --package custometry-api

FROM python:3.12.14-slim-trixie@sha256:78387bc3881b8273120a12ebe6c1ab22b018ccc2c9adf565ae1ac9b536e184ea AS runtime-closure

RUN groupadd --system --gid 10001 custometry \
    && useradd --system --uid 10001 --gid custometry --home-dir /nonexistent --shell /usr/sbin/nologin custometry

WORKDIR /app
COPY --from=build --chown=10001:10001 /app/.venv /app/.venv
COPY --chown=10001:10001 packages/identity_access /app/.venv/lib/python3.12/site-packages/packages/identity_access
COPY --chown=10001:10001 packages/presentation /app/.venv/lib/python3.12/site-packages/packages/presentation
COPY --chown=10001:10001 packages/connection_catalog /app/.venv/lib/python3.12/site-packages/packages/connection_catalog
COPY --chown=10001:10001 packages/data_documentation /app/.venv/lib/python3.12/site-packages/packages/data_documentation
COPY --chown=10001:10001 packages/analytics_core /app/.venv/lib/python3.12/site-packages/packages/analytics_core
COPY --chown=10001:10001 packages/execution /app/.venv/lib/python3.12/site-packages/packages/execution
COPY --chown=10001:10001 packages/notifications /app/.venv/lib/python3.12/site-packages/packages/notifications
COPY --chown=10001:10001 packages/contracts/analytics /app/.venv/lib/python3.12/site-packages/packages/contracts/analytics
COPY --chown=10001:10001 packages/contracts/data_pipeline /app/.venv/lib/python3.12/site-packages/packages/contracts/data_pipeline
COPY --chown=10001:10001 packages/contracts/execution /app/.venv/lib/python3.12/site-packages/packages/contracts/execution
COPY --chown=10001:10001 packages/contracts/identity /app/.venv/lib/python3.12/site-packages/packages/contracts/identity
COPY --chown=10001:10001 packages/contracts/notifications /app/.venv/lib/python3.12/site-packages/packages/contracts/notifications
COPY --chown=10001:10001 packages/contracts/organization /app/.venv/lib/python3.12/site-packages/packages/contracts/organization
COPY --chown=10001:10001 packages/contracts/people /app/.venv/lib/python3.12/site-packages/packages/contracts/people
COPY --chown=10001:10001 packages/contracts/source_intake /app/.venv/lib/python3.12/site-packages/packages/contracts/source_intake
COPY --chown=10001:10001 plugins/connector_files /app/.venv/lib/python3.12/site-packages/plugins/connector_files
COPY --chown=10001:10001 plugins/connector_postgresql /app/.venv/lib/python3.12/site-packages/plugins/connector_postgresql
COPY --chown=10001:10001 migrations /app/migrations
COPY --chown=10001:10001 LICENSE /app/notices/Custometry-LICENSE
COPY deploy/compose/collect-python-runtime.py /tmp/collect-python-runtime.py
RUN python /tmp/collect-python-runtime.py

FROM scratch AS runtime
ARG CUSTOMETRY_VERSION=0.1.0-dev.0
LABEL org.opencontainers.image.title="Custometry API" \
      org.opencontainers.image.version="${CUSTOMETRY_VERSION}" \
      org.opencontainers.image.licenses="Apache-2.0"
ENV PATH="/app/.venv/bin:/usr/local/bin:/usr/local/sbin:/usr/bin:/bin" \
    PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    CUSTOMETRY_VERSION="${CUSTOMETRY_VERSION}"
COPY --from=runtime-closure /runtime/ /
WORKDIR /app

USER 10001:10001
EXPOSE 8000
CMD ["uvicorn", "custometry_api.main:app", "--host", "0.0.0.0", "--port", "8000", "--no-access-log"]
