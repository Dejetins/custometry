#!/usr/bin/env bash
set -euo pipefail
# Select a Python 3.12 executable explicitly; never replace the host default.
: "${CUSTOMETRY_INSTALL_PYTHON:?Set CUSTOMETRY_INSTALL_PYTHON to a Python 3.12 executable}"
script_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
exec "${CUSTOMETRY_INSTALL_PYTHON}" -I "${script_dir}/../../tools/custometry_quality/installation.py" "$@"
