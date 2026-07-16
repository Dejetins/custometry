#!/usr/bin/env bash
set -euo pipefail

script_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
repo_root="$(cd "${script_dir}/../.." && pwd)"
runtime_root="$(mktemp -d "${TMPDIR:-/tmp}/custometry-ci.XXXXXX")"
export CUSTOMETRY_RUNTIME_ENV_FILE="${runtime_root}/runtime.env"
export CUSTOMETRY_SECRETS_DIR="${runtime_root}/secrets"
export COMPOSE_PROJECT_NAME="custometry-ci-${GITHUB_RUN_ID:-local}-$$"
bootstrap_mode="--build"
compose_files=(-f "${repo_root}/compose.yaml")
compose_env_files=(--env-file "${CUSTOMETRY_RUNTIME_ENV_FILE}")
if [[ -n "${CUSTOMETRY_RELEASE_ENV_FILE:-}" ]]; then
  [[ -f "${CUSTOMETRY_RELEASE_ENV_FILE}" ]] || {
    echo "CUSTOMETRY_RELEASE_ENV_FILE does not exist: ${CUSTOMETRY_RELEASE_ENV_FILE}" >&2
    exit 2
  }
  validated_release_env="${runtime_root}/release-manifest.env"
  python3 "${script_dir}/validate-release-manifest.py" \
    "${CUSTOMETRY_RELEASE_ENV_FILE}" "${validated_release_env}"
  bootstrap_mode="--release"
  compose_files+=(-f "${repo_root}/deploy/compose/compose.release.yaml")
  compose_env_files+=(--env-file "${validated_release_env}")
  while IFS="=" read -r key value; do
    case "${key}" in
      CUSTOMETRY_VERSION) export CUSTOMETRY_VERSION="${value}" ;;
      CUSTOMETRY_API_IMAGE) export CUSTOMETRY_API_IMAGE="${value}" ;;
      CUSTOMETRY_WEB_IMAGE) export CUSTOMETRY_WEB_IMAGE="${value}" ;;
    esac
  done <"${validated_release_env}"
fi

cleanup() {
  if [[ "${COMPOSE_PROJECT_NAME}" == custometry-ci-* ]]; then
    docker compose "${compose_files[@]}" "${compose_env_files[@]}" \
      --profile demo --profile migration down --volumes --remove-orphans >/dev/null 2>&1 || true
  fi
  rm -rf "${runtime_root}"
}
trap cleanup EXIT

"${script_dir}/bootstrap.sh" "${bootstrap_mode}" --with-demo
"${script_dir}/check-image-size.sh"

# shellcheck disable=SC1090
source "${CUSTOMETRY_RUNTIME_ENV_FILE}"
base_url="http://${CUSTOMETRY_BIND_HOST}:${CUSTOMETRY_HTTP_PORT}"
curl --fail --silent --show-error "${base_url}/" >/dev/null
curl --fail --silent --show-error "${base_url}/docs/" >/dev/null
curl --fail --silent --show-error "${base_url}/api/health/live" >/dev/null
curl --fail --silent --show-error "${base_url}/api/health/ready" >/dev/null
curl --fail --silent --show-error "${base_url}/api/version" >/dev/null

compose=(docker compose "${compose_files[@]}" "${compose_env_files[@]}")
"${compose[@]}" --profile migration run --rm migrate alembic -c /app/migrations/alembic.ini downgrade base
"${compose[@]}" --profile migration run --rm migrate alembic -c /app/migrations/alembic.ini upgrade head

for _ in {1..60}; do
  if "${compose[@]}" --profile demo exec -T demo-source-db \
    pg_isready -U demo_source_admin -d northwind_retail >/dev/null 2>&1; then
    break
  fi
  sleep 1
done
"${compose[@]}" --profile demo exec -T demo-source-db \
  pg_isready -U demo_source_admin -d northwind_retail >/dev/null

evidence="$("${compose[@]}" --profile demo exec -T demo-source-db \
  psql -U demo_source_admin -d northwind_retail -At \
  <"${repo_root}/tests/golden/retail-demo-evidence.sql")"
printf '%s\n' "${evidence}" | python3 "${repo_root}/tests/golden/verify_retail_demo.py" \
  "${repo_root}/tests/golden/retail-demo-manifest.json"

"${compose[@]}" exec -T api python -c \
  "import socket; socket.getaddrinfo('control-db', 5432)" >/dev/null
if "${compose[@]}" exec -T api python -c \
  "import socket; socket.create_connection(('1.1.1.1', 443), timeout=1)" >/dev/null 2>&1; then
  echo "API unexpectedly has general runtime internet egress." >&2
  exit 1
fi
"${compose[@]}" exec -T web wget --quiet --timeout=2 --spider \
  http://api:8000/health/live >/dev/null
if "${compose[@]}" exec -T web wget --quiet --timeout=2 --spider http://1.1.1.1 \
  >/dev/null 2>&1; then
  echo "Web unexpectedly has general runtime internet egress." >&2
  exit 1
fi
"${compose[@]}" exec -T edge wget --quiet --timeout=2 --spider \
  http://web:8080/health/live >/dev/null
if "${compose[@]}" exec -T edge wget --quiet --timeout=2 --spider \
  http://api:8000/health/live >/dev/null 2>&1; then
  echo "Edge unexpectedly reaches API directly instead of through Web." >&2
  exit 1
fi
control_db_container="$("${compose[@]}" ps -q control-db)"
[[ -n "${control_db_container}" ]] || {
  echo "control-db container could not be identified for the publication check." >&2
  exit 1
}
if docker port "${control_db_container}" 5432/tcp >/dev/null 2>&1; then
  echo "control-db unexpectedly publishes a host port." >&2
  exit 1
fi

curl --fail --silent --show-error "${base_url}/api/health/ready" >/dev/null

if [[ "${CUSTOMETRY_RUN_BROWSER:-0}" == "1" ]]; then
  browser_image="custometry-browser-acceptance:dev"
  docker build --file "${repo_root}/tests/e2e/Dockerfile" \
    --tag "${browser_image}" "${repo_root}"
  mkdir -p "${repo_root}/tests/e2e/playwright-report" "${repo_root}/tests/e2e/test-results"
  browser_run=(
    docker run --rm --ipc=host
    --user "$(id -u):$(id -g)"
    --env HOME=/tmp
    --env CUSTOMETRY_PLAYWRIGHT_EVIDENCE_ROOT=/evidence
    --volume "${repo_root}/tests/e2e:/evidence"
  )
  browser_base_url="${base_url}"
  if [[ "$(uname -s)" == "Linux" ]]; then
    browser_run+=(--network host)
  else
    browser_base_url="http://host.docker.internal:${CUSTOMETRY_HTTP_PORT}"
    browser_run+=(--add-host host.docker.internal:host-gateway)
  fi
  "${browser_run[@]}" --env CUSTOMETRY_BASE_URL="${browser_base_url}" "${browser_image}"
fi
printf 'Compose, migration lifecycle, API, docs and deterministic seed smoke passed.\n'
