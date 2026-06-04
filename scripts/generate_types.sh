#!/usr/bin/env bash
set -euo pipefail

ENV="${1:-prod}"

case "$ENV" in
  dev)
    SPEC_URL="https://dev.connect.crystalwatermonitor.app/docs/openapi.json"
    ;;
  prod)
    SPEC_URL="https://connect.crystalwatermonitor.app/docs/openapi.json"
    ;;
  *)
    echo "Usage: $0 [dev|prod]"
    exit 1
    ;;
esac

OUT="custom_components/crystal_water_monitor/connect-api"

if ! command -v openapi-generator &>/dev/null; then
  echo "openapi-generator not found. Install with: brew install openapi-generator"
  exit 1
fi

echo "Generating client from $SPEC_URL..."
rm -rf "$OUT"
openapi-generator generate \
  -i "$SPEC_URL" \
  -g python \
  --library asyncio \
  -o "$OUT" \
  --package-name connect_api \
  --additional-properties=generateSourceCodeOnly=true

rm -rf "$OUT/connect_api/docs" "$OUT/connect_api/test" "$OUT"/*.md

echo "Done. Review $OUT for any changes."
