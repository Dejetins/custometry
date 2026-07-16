#!/usr/bin/env bash
set -euo pipefail

repo_root="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
node_version="$(tr -d '[:space:]' <"${repo_root}/.node-version")"
uv_version="$(tr -d '[:space:]' <"${repo_root}/.uv-version")"
pnpm_version="$(
  sed -nE 's/^[[:space:]]*"packageManager":[[:space:]]*"pnpm@([^"]+)".*/\1/p' \
    "${repo_root}/package.json"
)"

export NVM_DIR="${NVM_DIR:-${HOME}/.nvm}"
[[ -s "${NVM_DIR}/nvm.sh" ]] || {
  echo "nvm is required before bootstrapping the Custometry toolchain." >&2
  exit 1
}

# shellcheck disable=SC1090
. "${NVM_DIR}/nvm.sh"
nvm install "${node_version}"
nvm use "${node_version}"
corepack enable
corepack prepare "pnpm@${pnpm_version}" --activate

actual_uv="$(uv --version | awk '{print $2}')"
[[ "${actual_uv}" == "${uv_version}" ]] || {
  echo "uv ${actual_uv} is active; repository requires ${uv_version}." >&2
  echo "Install the pinned uv version, then rerun this script." >&2
  exit 1
}

cd "${repo_root}"
uv sync --locked --all-groups --all-packages
corepack pnpm install --frozen-lockfile

printf 'Toolchain bootstrap complete. Activate each shell with:\n'
printf '  source scripts/activate-toolchain.sh\n'
printf 'Repository Git hooks activate the same pins automatically.\n'
