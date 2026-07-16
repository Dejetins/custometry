#!/usr/bin/env bash
set -euo pipefail

reader_password="$(tr -d '\r\n' </run/secrets/demo_source_reader_password)"
[[ "${reader_password}" =~ ^[a-f0-9]{64}$ ]] || {
  echo "demo source reader password has an invalid local-secret format" >&2
  exit 1
}

printf "CREATE ROLE demo_reader LOGIN PASSWORD '%s';\n" "${reader_password}" \
  | psql --set ON_ERROR_STOP=1 --username "${POSTGRES_USER}" --dbname "${POSTGRES_DB}"
unset reader_password
