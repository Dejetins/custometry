#!/usr/bin/env bash
set -euo pipefail

profile="${1:-}"
case "${profile}" in
  pre-commit | pre-push)
    ;;
  *)
    echo "Usage: scripts/run-hook-profile.sh <pre-commit|pre-push>" >&2
    exit 2
    ;;
esac

repo_root="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "${repo_root}"

# shellcheck disable=SC1091
source "${repo_root}/scripts/activate-toolchain.sh"

exec uv run --locked python -m tools.check --scope "${profile}"
