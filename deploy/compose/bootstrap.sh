#!/usr/bin/env bash
set -euo pipefail

script_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
repo_root="$(cd "${script_dir}/../.." && pwd)"
runtime_env="${CUSTOMETRY_RUNTIME_ENV_FILE:-${script_dir}/.runtime.env}"
release_env="${CUSTOMETRY_RELEASE_ENV_FILE:-${script_dir}/.release.env}"
release_manifest_validator="${script_dir}/validate-release-manifest.py"
secrets_dir="${CUSTOMETRY_SECRETS_DIR:-${script_dir}/.runtime-secrets}"
repo_hash="$(printf '%s' "${repo_root}" | shasum -a 256 | cut -c1-10)"
project_name="${COMPOSE_PROJECT_NAME:-custometry-${repo_hash}}"
mode="auto"
with_demo=false
action="up"
requested_port="${CUSTOMETRY_HTTP_PORT:-}"
data_profile="${CUSTOMETRY_DATA_PROFILE:-demo}"
allow_benchmark="${CUSTOMETRY_ALLOW_BENCHMARK:-0}"
data_profile_explicit=false
[[ "${CUSTOMETRY_DATA_PROFILE+x}" == "x" ]] && data_profile_explicit=true

usage() {
  cat <<'EOF'
Usage: deploy/compose/bootstrap.sh [--build|--release] [--with-demo]
                                   [--data-profile smoke|demo|benchmark]
                                   [--allow-large-data]
                                   [--down|--reset-demo-data|--print-url]

  --build       Build lean development images from this checkout.
  --release     Pull immutable images named by deploy/compose/.release.env.
  --with-demo   Start the isolated deterministic retail source database.
  --data-profile Select the deterministic source profile and imply --with-demo.
  --allow-large-data Permit the benchmark profile; never enabled implicitly.
  --down        Stop containers without deleting persistent volumes.
  --reset-demo-data Delete only the exact installation-owned demo-source volume.
  --print-url   Print the previously selected local URL.
EOF
}

while (($#)); do
  case "$1" in
    --build) mode="build" ;;
    --release) mode="release" ;;
    --with-demo) with_demo=true ;;
    --data-profile)
      [[ $# -ge 2 ]] || { echo "--data-profile requires a value" >&2; exit 2; }
      data_profile="$2"
      data_profile_explicit=true
      with_demo=true
      shift
      ;;
    --allow-large-data) allow_benchmark=1 ;;
    --down) action="down" ;;
    --reset-demo-data) action="reset-demo-data" ;;
    --print-url) action="print-url" ;;
    --help|-h) usage; exit 0 ;;
    *) echo "Unknown argument: $1" >&2; usage >&2; exit 2 ;;
  esac
  shift
done

if [[ "${mode}" == "auto" ]]; then
  if [[ -f "${release_env}" ]]; then mode="release"; else mode="build"; fi
fi

runtime_value() {
  local key="$1"
  awk -F= -v key="${key}" '
    $1 == key { sub(/^[^=]*=/, ""); print; found = 1; exit }
    END { if (!found) exit 1 }
  ' "${runtime_env}"
}

if [[ "${action}" == "print-url" ]]; then
  if [[ ! -f "${runtime_env}" ]]; then
    echo "Runtime environment has not been created yet." >&2
    exit 1
  fi
  # shellcheck disable=SC1090
  source "${runtime_env}"
  if [[ -n "${requested_port}" ]]; then CUSTOMETRY_HTTP_PORT="${requested_port}"; fi
  printf 'http://%s:%s\n' "${CUSTOMETRY_BIND_HOST}" "${CUSTOMETRY_HTTP_PORT}"
  exit 0
fi

if [[ "${action}" == "down" ]]; then
  if [[ ! -f "${runtime_env}" ]]; then
    printf 'No runtime state exists; nothing to stop.\n'
    exit 0
  fi
  command -v docker >/dev/null 2>&1 || { echo "docker is required" >&2; exit 1; }
  docker compose version >/dev/null 2>&1 || { echo "Docker Compose v2 is required" >&2; exit 1; }
  docker compose -f "${repo_root}/compose.yaml" --env-file "${runtime_env}" \
    --profile demo --profile migration down --remove-orphans
  exit 0
fi

if [[ "${action}" == "reset-demo-data" ]]; then
  if [[ ! -f "${runtime_env}" ]]; then
    printf 'No runtime state exists; no demo-source data can be owned by this installation.\n'
    exit 0
  fi
  command -v docker >/dev/null 2>&1 || { echo "docker is required" >&2; exit 1; }
  docker compose version >/dev/null 2>&1 || { echo "Docker Compose v2 is required" >&2; exit 1; }
  persisted_project="$(runtime_value COMPOSE_PROJECT_NAME)"
  [[ "${persisted_project}" =~ ^[a-z0-9][a-z0-9_.-]+$ ]] || {
    echo "Persisted COMPOSE_PROJECT_NAME is unsafe; refusing cleanup." >&2
    exit 1
  }
  demo_volume="${persisted_project}_demo_source_data"
  docker compose -f "${repo_root}/compose.yaml" --env-file "${runtime_env}" \
    --profile demo rm --stop --force demo-source-db >/dev/null 2>&1 || true
  if docker volume inspect "${demo_volume}" >/dev/null 2>&1; then
    owner_project="$(docker volume inspect --format '{{ index .Labels "com.docker.compose.project" }}' "${demo_volume}")"
    owner_volume="$(docker volume inspect --format '{{ index .Labels "com.docker.compose.volume" }}' "${demo_volume}")"
    [[ "${owner_project}" == "${persisted_project}" && "${owner_volume}" == "demo_source_data" ]] || {
      echo "Volume ${demo_volume} lacks exact Compose ownership labels; refusing cleanup." >&2
      exit 1
    }
    docker volume rm "${demo_volume}" >/dev/null
  fi
  printf 'Demo-source data reset for %s. Re-run bootstrap with the desired --data-profile.\n' "${persisted_project}"
  exit 0
fi

command -v python3 >/dev/null 2>&1 || { echo "python3 is required" >&2; exit 1; }
validated_release_env=""
if [[ "${mode}" == "release" ]]; then
  if [[ ! -f "${release_env}" ]]; then
    echo "Release mode requires ${release_env} with immutable image digests." >&2
    exit 1
  fi
  validated_release_env="${runtime_env}.release-manifest.env"
  python3 "${release_manifest_validator}" "${release_env}" "${validated_release_env}"
fi

command -v docker >/dev/null 2>&1 || { echo "docker is required" >&2; exit 1; }
docker compose version >/dev/null 2>&1 || { echo "Docker Compose v2 is required" >&2; exit 1; }
docker info >/dev/null 2>&1 || { echo "No reachable Docker engine. Start exactly one engine and retry." >&2; exit 1; }

choose_port() {
  python3 - <<'PY'
import socket
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server:
    server.bind(("127.0.0.1", 0))
    print(server.getsockname()[1])
PY
}

validate_port() {
  [[ "$1" =~ ^[0-9]+$ ]] && ((10#$1 >= 1024 && 10#$1 <= 65535))
}

write_runtime_env() {
  local port="$1"
  local temporary="${runtime_env}.tmp"
  umask 077
  cat >"${temporary}" <<EOF
COMPOSE_PROJECT_NAME=${project_name}
CUSTOMETRY_BIND_HOST=127.0.0.1
CUSTOMETRY_HTTP_PORT=${port}
CUSTOMETRY_VERSION=0.1.0-dev.0
CUSTOMETRY_ENVIRONMENT=development
CUSTOMETRY_SECRETS_DIR=${secrets_dir}
CUSTOMETRY_DATA_PROFILE=${data_profile}
CUSTOMETRY_ALLOW_BENCHMARK=${allow_benchmark}
EOF
  mv "${temporary}" "${runtime_env}"
  chmod 600 "${runtime_env}"
}

case "${data_profile}" in
  smoke|demo) ;;
  benchmark)
    [[ "${allow_benchmark}" == "1" ]] || {
      echo "benchmark profile requires --allow-large-data" >&2
      exit 2
    }
    ;;
  *) echo "Unknown data profile: ${data_profile}" >&2; exit 2 ;;
esac

if [[ -f "${runtime_env}" ]]; then
  persisted_project="$(runtime_value COMPOSE_PROJECT_NAME)"
  persisted_port="$(runtime_value CUSTOMETRY_HTTP_PORT)"
  persisted_profile="$(runtime_value CUSTOMETRY_DATA_PROFILE)"
  persisted_allow="$(runtime_value CUSTOMETRY_ALLOW_BENCHMARK)"
  persisted_secrets="$(runtime_value CUSTOMETRY_SECRETS_DIR)"
  if [[ "${COMPOSE_PROJECT_NAME+x}" == "x" && "${project_name}" != "${persisted_project}" ]]; then
    echo "Requested project ${project_name} differs from persisted ${persisted_project}." >&2
    exit 2
  fi
  project_name="${persisted_project}"
  secrets_dir="${persisted_secrets}"
  if [[ "${with_demo}" == true ]]; then
    if [[ "${data_profile_explicit}" == false ]]; then data_profile="${persisted_profile}"; fi
    case "${data_profile}" in
      smoke|demo) ;;
      benchmark)
        [[ "${allow_benchmark}" == "1" ]] || {
          echo "benchmark profile requires --allow-large-data" >&2
          exit 2
        }
        ;;
      *) echo "Persisted or requested data profile is invalid: ${data_profile}" >&2; exit 2 ;;
    esac
    if [[ "${data_profile}" != "${persisted_profile}" || "${allow_benchmark}" != "${persisted_allow}" ]]; then
      demo_volume="${persisted_project}_demo_source_data"
      if docker volume inspect "${demo_volume}" >/dev/null 2>&1; then
        echo "Requested demo profile/allow flag differs from persisted data (${persisted_profile}, allow=${persisted_allow})." >&2
        echo "Run deploy/compose/bootstrap.sh --reset-demo-data, then retry with the desired profile." >&2
        exit 2
      fi
      write_runtime_env "${persisted_port}"
    fi
  else
    data_profile="${persisted_profile}"
    allow_benchmark="${persisted_allow}"
  fi
fi

case "${data_profile}" in
  smoke|demo) ;;
  benchmark)
    [[ "${allow_benchmark}" == "1" ]] || {
      echo "benchmark profile requires --allow-large-data" >&2
      exit 2
    }
    ;;
  *) echo "Unknown data profile: ${data_profile}" >&2; exit 2 ;;
esac

mkdir -p "${secrets_dir}"
chmod 700 "${secrets_dir}"
for secret in control_db_password demo_source_admin_password demo_source_reader_password; do
  secret_path="${secrets_dir}/${secret}"
  if [[ ! -s "${secret_path}" ]]; then
    umask 077
    openssl rand -hex 32 >"${secret_path}"
  fi
  chmod 600 "${secret_path}"
done

if [[ -n "${requested_port}" ]]; then
  validate_port "${requested_port}" || {
    echo "CUSTOMETRY_HTTP_PORT must be an unprivileged port from 1024 to 65535." >&2
    exit 2
  }
  write_runtime_env "${requested_port}"
elif [[ ! -f "${runtime_env}" ]]; then
  write_runtime_env "$(choose_port)"
fi

compose_files=(-f "${repo_root}/compose.yaml")
env_files=(--env-file "${runtime_env}")
if [[ "${mode}" == "release" ]]; then
  compose_files+=(-f "${script_dir}/compose.release.yaml")
  env_files+=(--env-file "${validated_release_env}")
fi

compose() {
  docker compose "${compose_files[@]}" "${env_files[@]}" "$@"
}

cd "${repo_root}"
if [[ "${mode}" == "build" ]]; then
  compose build api web
else
  compose pull control-db api web edge
fi

compose up -d control-db
for _ in {1..40}; do
  if compose exec -T control-db pg_isready -U custometry -d custometry >/dev/null 2>&1; then break; fi
  sleep 1
done
compose exec -T control-db pg_isready -U custometry -d custometry >/dev/null

if [[ "${mode}" == "release" ]]; then
  compose_config="$(compose config --format json)"
  if printf '%s' "${compose_config}" | grep -q '"build"'; then
    echo "Release Compose still contains a build definition; refusing source build." >&2
    exit 1
  fi
fi

compose --profile migration run --rm migrate

web_started=false
for _ in {1..3}; do
  if [[ "${mode}" == "release" ]]; then
    up_result=0
    compose up -d --no-build api web edge || up_result=$?
  else
    up_result=0
    compose up -d api web edge || up_result=$?
  fi
  if ((up_result == 0)); then
    web_started=true
    break
  fi
  if [[ -n "${requested_port}" ]]; then
    echo "The explicitly requested port ${requested_port} could not be published." >&2
    exit 1
  fi
  write_runtime_env "$(choose_port)"
done
[[ "${web_started}" == true ]] || { echo "Could not publish a free loopback port." >&2; exit 1; }

if [[ "${with_demo}" == true ]]; then
  if [[ "${mode}" == "release" ]]; then compose --profile demo pull demo-source-db; fi
  if [[ "${mode}" == "release" ]]; then
    compose --profile demo up -d --no-build demo-source-db
  else
    compose --profile demo up -d demo-source-db
  fi
fi

# shellcheck disable=SC1090
source "${runtime_env}"
mapped_endpoint="$(compose port edge 8080)"
mapped_port="${mapped_endpoint##*:}"
validate_port "${mapped_port}" || { echo "Could not determine the factual Web port." >&2; exit 1; }
if [[ "${mapped_port}" != "${CUSTOMETRY_HTTP_PORT}" ]]; then
  write_runtime_env "${mapped_port}"
  CUSTOMETRY_HTTP_PORT="${mapped_port}"
fi
base_url="http://${CUSTOMETRY_BIND_HOST}:${CUSTOMETRY_HTTP_PORT}"
for _ in {1..60}; do
  if curl --fail --silent --show-error "${base_url}/api/health/ready" >/dev/null 2>&1; then
    printf 'Custometry Foundation is ready: %s\n' "${base_url}"
    printf 'Local documentation: %s/docs/\n' "${base_url}"
    exit 0
  fi
  sleep 1
done

echo "Foundation readiness did not become healthy at ${base_url}." >&2
compose ps >&2
exit 1
