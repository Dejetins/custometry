FROM ghcr.io/astral-sh/uv:0.9.26 AS uv
FROM python:3.12.12-slim-bookworm
COPY --from=uv /uv /usr/local/bin/uv
WORKDIR /opt/custometry
COPY pyproject.toml uv.lock ./
COPY apps/api/pyproject.toml apps/api/pyproject.toml
COPY docs-site/pyproject.toml docs-site/pyproject.toml
RUN uv sync --locked --no-dev --package custometry-api --no-install-workspace
ENV PATH="/opt/custometry/.venv/bin:${PATH}"
ENV PYTHONPATH="/workspace/apps/api/src:/workspace:/workspace/scripts"
WORKDIR /workspace
