#!/usr/bin/env bash
set -euo pipefail

step="${1:-}"
case "${step}" in upgrade_empty|upgrade_repeat|downgrade|reupgrade) ;; *) exit 2 ;; esac

script_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
repo_root="$(cd "${script_dir}/../.." && pwd)"
run_identity="${CUSTOMETRY_MIGRATION_RUN_ID:-${PPID}}"
runtime_root="${TMPDIR:-/tmp}/custometry-migration-${run_identity}"
runtime_env="${runtime_root}/runtime.env"
secrets_dir="${runtime_root}/secrets"
project="custometry-migration-${run_identity}"

cleanup() {
  docker compose -f "${repo_root}/compose.yaml" --env-file "${runtime_env}" \
    --profile migration down --volumes --remove-orphans >/dev/null 2>&1 || true
  rm -rf "${runtime_root}"
}
trap 'if [[ $? -ne 0 ]]; then cleanup; fi' EXIT

if [[ "${step}" == "upgrade_empty" ]]; then
  rm -rf "${runtime_root}"
  mkdir -p "${secrets_dir}"
  chmod 700 "${secrets_dir}"
  umask 077
  openssl rand -hex 32 >"${secrets_dir}/control_db_password"
  # Compose validates every declared secret even when the demo profile is inactive.
  openssl rand -hex 32 >"${secrets_dir}/demo_source_admin_password"
  openssl rand -hex 32 >"${secrets_dir}/demo_source_reader_password"
  cat >"${runtime_env}" <<EOF
COMPOSE_PROJECT_NAME=${project}
CUSTOMETRY_BIND_HOST=127.0.0.1
CUSTOMETRY_HTTP_PORT=0
CUSTOMETRY_VERSION=0.1.0-dev.0
CUSTOMETRY_ENVIRONMENT=test
CUSTOMETRY_SECRETS_DIR=${secrets_dir}
EOF
  docker compose -f "${repo_root}/compose.yaml" --env-file "${runtime_env}" build api
  docker compose -f "${repo_root}/compose.yaml" --env-file "${runtime_env}" up -d control-db
fi

[[ -f "${runtime_env}" ]] || { echo "migration lifecycle state is missing" >&2; exit 1; }
compose=(docker compose -f "${repo_root}/compose.yaml" --env-file "${runtime_env}")
for _ in {1..40}; do
  if "${compose[@]}" exec -T control-db pg_isready -U custometry -d custometry >/dev/null 2>&1; then break; fi
  sleep 1
done
"${compose[@]}" exec -T control-db pg_isready -U custometry -d custometry >/dev/null

case "${step}" in
  upgrade_empty|upgrade_repeat)
    "${compose[@]}" --profile migration run --rm migrate
    ;;
  downgrade)
    "${compose[@]}" --profile migration run --rm migrate \
      alembic -c /app/migrations/alembic.ini downgrade base
    ;;
  reupgrade)
    "${compose[@]}" --profile migration run --rm migrate
    cleanup
    trap - EXIT
    ;;
esac
