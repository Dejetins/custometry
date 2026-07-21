# syntax=docker/dockerfile:1.11
FROM ghcr.io/astral-sh/uv:0.9.26-python3.12-bookworm-slim@sha256:add251a8fbfa14ff5e115adf93cb113c7b58c57bc84f0992164f5b6631b3451f AS build

WORKDIR /src
ENV UV_COMPILE_BYTECODE=1 \
    UV_LINK_MODE=copy \
    UV_PROJECT_ENVIRONMENT=/app/.venv

COPY pyproject.toml uv.lock README.md LICENSE ./
COPY apps/api/pyproject.toml apps/api/pyproject.toml
COPY docs-site/pyproject.toml docs-site/pyproject.toml
RUN uv sync --locked --no-dev --no-install-workspace --package custometry-api

COPY apps/api/src apps/api/src
RUN uv sync --locked --no-dev --no-editable --package custometry-api

FROM python:3.12.11-slim-bookworm@sha256:519591d6871b7bc437060736b9f7456b8731f1499a57e22e6c285135ae657bf7 AS runtime

ARG CUSTOMETRY_VERSION=0.1.0-dev.0
LABEL org.opencontainers.image.title="Custometry API" \
      org.opencontainers.image.version="${CUSTOMETRY_VERSION}" \
      org.opencontainers.image.licenses="Apache-2.0"

ENV PATH="/app/.venv/bin:${PATH}" \
    PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    CUSTOMETRY_VERSION="${CUSTOMETRY_VERSION}"

RUN groupadd --system --gid 10001 custometry \
    && useradd --system --uid 10001 --gid custometry --home-dir /nonexistent --shell /usr/sbin/nologin custometry

WORKDIR /app
COPY --from=build --chown=10001:10001 /app/.venv /app/.venv
COPY --chown=10001:10001 packages/identity_access /app/.venv/lib/python3.12/site-packages/packages/identity_access
COPY --chown=10001:10001 packages/contracts/identity /app/.venv/lib/python3.12/site-packages/packages/contracts/identity
COPY --chown=10001:10001 migrations /app/migrations

USER 10001:10001
EXPOSE 8000
CMD ["uvicorn", "custometry_api.main:app", "--host", "0.0.0.0", "--port", "8000", "--no-access-log"]
