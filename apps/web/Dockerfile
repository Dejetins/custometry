# syntax=docker/dockerfile:1.11@sha256:10c699f1b6c8bdc8f6b4ce8974855dd8542f1768c26eb240237b8f1c9c6c9976
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
COPY deploy/compose/collect-web-notices.mjs deploy/compose/collect-web-notices.mjs
COPY LICENSE LICENSE
RUN pnpm --filter @custometry/web build \
    && node deploy/compose/collect-web-notices.mjs \
    && cp LICENSE apps/web/dist/notices/Custometry-LICENSE

FROM ghcr.io/astral-sh/uv:0.9.26-python3.12-bookworm-slim@sha256:add251a8fbfa14ff5e115adf93cb113c7b58c57bc84f0992164f5b6631b3451f AS docs-build

WORKDIR /src
COPY pyproject.toml uv.lock README.md LICENSE mkdocs.yml ./
COPY apps/api/pyproject.toml apps/api/pyproject.toml
COPY docs-site/pyproject.toml docs-site/pyproject.toml
RUN uv sync --locked --no-dev --package custometry-docs
COPY docs-site/docs docs-site/docs
COPY docs-site/generate_csp.py docs-site/generate_csp.py
RUN uv run --frozen --package custometry-docs mkdocs build --strict --config-file mkdocs.yml \
    && python docs-site/generate_csp.py site /tmp/docs-csp.conf \
    && mkdir -p site/notices \
    && python -c 'import importlib.metadata as m, pathlib; p=pathlib.Path("site/notices/python-packages.txt"); p.write_text("\n\n".join(str(d.metadata["Name"])+"=="+d.version+"\n"+"\n".join(d.locate_file(f).read_text(errors="replace") for f in sorted(d.files or [], key=str) if "dist-info" in str(f) and ("license" in str(f).lower() or "notice" in str(f).lower())) for d in sorted(m.distributions(path=[".venv/lib/python3.12/site-packages"]), key=lambda d: (str(d.metadata["Name"]), d.version))))'

FROM nginxinc/nginx-unprivileged:1.30.4-alpine3.24-slim@sha256:3a4485bf084957d56674ee22db07d77d5a281418815c5852827419d6d629d440 AS runtime

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
