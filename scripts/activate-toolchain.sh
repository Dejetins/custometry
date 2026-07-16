#!/usr/bin/env bash

custometry_source_path="${BASH_SOURCE[0]:-${0}}"

if [[ "${custometry_source_path}" == "${0}" && -n "${BASH_VERSION:-}" ]]; then
  echo "Source this file instead of executing it: source scripts/activate-toolchain.sh" >&2
  exit 2
fi

custometry_repo_root="$(cd "$(dirname "${custometry_source_path}")/.." && pwd)"
custometry_node_version="$(tr -d '[:space:]' <"${custometry_repo_root}/.node-version")"
custometry_uv_version="$(tr -d '[:space:]' <"${custometry_repo_root}/.uv-version")"
custometry_pnpm_version="$(
  sed -nE 's/^[[:space:]]*"packageManager":[[:space:]]*"pnpm@([^"]+)".*/\1/p' \
    "${custometry_repo_root}/package.json"
)"

if [[ -z "${custometry_pnpm_version}" ]]; then
  echo "package.json must contain an exact packageManager pnpm pin." >&2
  return 1
fi

export NVM_DIR="${NVM_DIR:-${HOME}/.nvm}"
if [[ ! -s "${NVM_DIR}/nvm.sh" ]]; then
  echo "nvm is required. Install nvm, then run scripts/bootstrap-toolchain.sh." >&2
  return 1
fi

# shellcheck disable=SC1090
. "${NVM_DIR}/nvm.sh"
if ! nvm use --silent "${custometry_node_version}" >/dev/null; then
  echo "Node ${custometry_node_version} is not installed. Run scripts/bootstrap-toolchain.sh." >&2
  return 1
fi

custometry_actual_node="$(node --version | sed 's/^v//')"
custometry_actual_pnpm="$(corepack pnpm --version)"
custometry_actual_uv="$(uv --version | awk '{print $2}')"

if [[ "${custometry_actual_node}" != "${custometry_node_version}" ]]; then
  echo "Node ${custometry_actual_node} is active; expected ${custometry_node_version}." >&2
  return 1
fi
if [[ "${custometry_actual_pnpm}" != "${custometry_pnpm_version}" ]]; then
  echo "pnpm ${custometry_actual_pnpm} is active; expected ${custometry_pnpm_version}." >&2
  echo "Run scripts/bootstrap-toolchain.sh to activate the pinned Corepack package manager." >&2
  return 1
fi
if [[ "${custometry_actual_uv}" != "${custometry_uv_version}" ]]; then
  echo "uv ${custometry_actual_uv} is active; expected ${custometry_uv_version}." >&2
  return 1
fi

export CUSTOMETRY_TOOLCHAIN_ACTIVE=1
export CUSTOMETRY_PNPM_COMMAND="corepack pnpm"

unset custometry_actual_node custometry_actual_pnpm custometry_actual_uv
unset custometry_node_version custometry_pnpm_version custometry_repo_root custometry_uv_version
unset custometry_source_path

printf 'Custometry toolchain active: Node %s, pnpm %s, uv %s\n' \
  "$(node --version | sed 's/^v//')" \
  "$(corepack pnpm --version)" \
  "$(uv --version | awk '{print $2}')"
