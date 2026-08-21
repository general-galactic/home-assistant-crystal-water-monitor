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

GEN_DIR="$(mktemp -d)"
trap 'rm -rf "$GEN_DIR"' EXIT
PKG_DIR="custom_components/crystal_water_monitor/connect_api"

if ! command -v openapi-generator &>/dev/null; then
  echo "openapi-generator not found. Install with: brew install openapi-generator"
  exit 1
fi

echo "Generating client from $SPEC_URL..."
openapi-generator generate \
  -i "$SPEC_URL" \
  -g python \
  --library asyncio \
  -o "$GEN_DIR" \
  --package-name connect_api \
  --additional-properties=generateSourceCodeOnly=true

rm -rf "$GEN_DIR/connect_api/docs" "$GEN_DIR/connect_api/test"

echo "Rewriting absolute imports to relative..."
python3 "$(dirname "$0")/rewrite_relative_imports.py" "$GEN_DIR/connect_api"

rm -rf "$PKG_DIR"
mv "$GEN_DIR/connect_api" "$PKG_DIR"

echo "Done. Review $PKG_DIR for any changes."
