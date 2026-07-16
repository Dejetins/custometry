# syntax=docker/dockerfile:1.11
FROM node:24.18.0-bookworm-slim@sha256:6f7b03f7c2c8e2e784dcf9295400527b9b1270fd37b7e9a7285cf83b6951452d AS pinned-node

FROM mcr.microsoft.com/playwright:v1.52.0-noble@sha256:a021500a801bab0611049217ffad6b9697d827205c15babb86a53bc1a61c02d5

LABEL org.opencontainers.image.title="Custometry browser acceptance runner" \
      org.opencontainers.image.description="Test-only Node 24 + Playwright runner; never shipped with Custometry"

COPY --from=pinned-node /usr/local/ /usr/local/

ENV CI=1 \
    COREPACK_HOME=/opt/corepack \
    PLAYWRIGHT_BROWSERS_PATH=/ms-playwright

WORKDIR /workspace

RUN corepack prepare pnpm@11.13.0 --activate \
    && test "$(node --version)" = "v24.18.0" \
    && test "$(corepack pnpm --version)" = "11.13.0"

COPY package.json pnpm-lock.yaml pnpm-workspace.yaml ./
COPY apps/web/package.json apps/web/package.json
COPY packages/chart_compiler_ts/package.json packages/chart_compiler_ts/package.json
COPY packages/contracts/package.json packages/contracts/package.json
COPY packages/localization/package.json packages/localization/package.json
RUN corepack pnpm install --frozen-lockfile

COPY tests/e2e tests/e2e

ENTRYPOINT ["corepack", "pnpm", "--filter", "@custometry/web", "test:e2e"]
