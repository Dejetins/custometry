#!/usr/bin/env bash
set -euo pipefail

profile="${CUSTOMETRY_DATA_PROFILE:-demo}"
case "${profile}" in
  smoke)
    store_count=4
    customer_count=100
    product_count=40
    promotion_count=6
    receipt_count=500
    items_per_receipt=2
    audience_member_count=20
    ;;
  demo)
    store_count=20
    customer_count=1000
    product_count=120
    promotion_count=12
    receipt_count=5000
    items_per_receipt=3
    audience_member_count=50
    ;;
  benchmark)
    if [[ "${CUSTOMETRY_ALLOW_BENCHMARK:-0}" != "1" ]]; then
      echo "benchmark profile requires CUSTOMETRY_ALLOW_BENCHMARK=1; it is never implicit" >&2
      exit 1
    fi
    store_count=1000
    customer_count=500000
    product_count=100000
    promotion_count=120
    receipt_count=10000000
    items_per_receipt=5
    audience_member_count=1000
    ;;
  *)
    echo "unsupported deterministic data profile: ${profile}" >&2
    exit 1
    ;;
esac

cat >/tmp/custometry-profile.psql <<EOF
\\set store_count ${store_count}
\\set customer_count ${customer_count}
\\set product_count ${product_count}
\\set promotion_count ${promotion_count}
\\set receipt_count ${receipt_count}
\\set items_per_receipt ${items_per_receipt}
\\set audience_member_count ${audience_member_count}
EOF

printf 'Deterministic retail profile: %s (customers=%s receipts=%s items=%s)\n' \
  "${profile}" "${customer_count}" "${receipt_count}" "$((receipt_count * items_per_receipt))"
