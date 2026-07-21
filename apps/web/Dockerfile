# syntax=docker/dockerfile:1.11
FROM node:24.18.0-alpine3.23@sha256:595398b0081eacda8e1c4c5b97b76cd1020e4d58a8ebcb4843b9bca1e79e7436 AS web-build

WORKDIR /src
RUN corepack enable && corepack prepare pnpm@11.13.0 --activate
COPY package.json pnpm-lock.yaml pnpm-workspace.yaml ./
COPY apps/web/package.json apps/web/package.json
COPY packages/contracts/package.json packages/contracts/package.json
COPY packages/localization/package.json packages/localization/package.json
COPY packages/chart_compiler_ts/package.json packages/chart_compiler_ts/package.json
COPY packages/ui-foundation/package.json packages/ui-foundation/package.json
RUN pnpm install --frozen-lockfile
COPY apps/web apps/web
COPY packages/contracts packages/contracts
COPY packages/localization packages/localization
COPY packages/chart_compiler_ts packages/chart_compiler_ts
COPY packages/ui-foundation packages/ui-foundation
RUN pnpm --filter @custometry/web build

FROM ghcr.io/astral-sh/uv:0.9.26-python3.12-bookworm-slim@sha256:add251a8fbfa14ff5e115adf93cb113c7b58c57bc84f0992164f5b6631b3451f AS docs-build

WORKDIR /src
COPY pyproject.toml uv.lock README.md LICENSE mkdocs.yml ./
COPY apps/api/pyproject.toml apps/api/pyproject.toml
COPY docs-site/pyproject.toml docs-site/pyproject.toml
RUN uv sync --locked --no-dev --package custometry-docs
COPY docs-site/docs docs-site/docs
COPY docs-site/generate_csp.py docs-site/generate_csp.py
RUN uv run --frozen --package custometry-docs mkdocs build --strict --config-file mkdocs.yml \
    && python docs-site/generate_csp.py site /tmp/docs-csp.conf

FROM nginxinc/nginx-unprivileged:1.28.0-alpine3.21@sha256:c97ff0bf7cbae369953c6da1232ec14ad9f971d66360c5698db0856a4cd657a0 AS runtime

ARG CUSTOMETRY_VERSION=0.1.0-dev.0
LABEL org.opencontainers.image.title="Custometry Web" \
      org.opencontainers.image.version="${CUSTOMETRY_VERSION}" \
      org.opencontainers.image.licenses="Apache-2.0"

COPY --from=web-build --chown=101:101 /src/apps/web/dist /usr/share/nginx/html
COPY --from=docs-build --chown=101:101 /src/site /usr/share/nginx/html/docs
COPY --from=docs-build --chown=101:101 /tmp/docs-csp.conf /etc/nginx/docs-csp.conf
COPY --chown=101:101 apps/web/nginx.conf /etc/nginx/nginx.conf
COPY --chown=101:101 deploy/edge/nginx.conf /etc/nginx/edge.conf

USER 101:101
EXPOSE 8080
