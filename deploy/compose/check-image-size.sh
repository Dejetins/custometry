#!/usr/bin/env bash
set -euo pipefail

# Historical Foundation engine statistic. S03/S04 unpacked caps additionally
# require delivery_image_size's OCI descriptor/DiffID-bound observation.
echo 'Legacy Docker engine Size check; this does not prove the S03/S04 unpacked layer cap.' >&2

api_image="${CUSTOMETRY_API_IMAGE:-custometry-api:dev}"
web_image="${CUSTOMETRY_WEB_IMAGE:-custometry-web:dev}"
api_limit_bytes="${CUSTOMETRY_API_IMAGE_MAX_BYTES:-367001600}"
web_limit_bytes="${CUSTOMETRY_WEB_IMAGE_MAX_BYTES:-104857600}"

check_image() {
  local image="$1"
  local limit="$2"
  local size
  size="$(docker image inspect --format '{{.Size}}' "${image}")"
  [[ "${size}" =~ ^[0-9]+$ ]] || { echo "Could not inspect ${image} size." >&2; exit 1; }
  if ((size > limit)); then
    echo "${image} is ${size} bytes, above the Foundation limit ${limit}." >&2
    exit 1
  fi
  printf '%s size: %s bytes (limit %s)\n' "${image}" "${size}" "${limit}"
}

check_image "${api_image}" "${api_limit_bytes}"
check_image "${web_image}" "${web_limit_bytes}"
