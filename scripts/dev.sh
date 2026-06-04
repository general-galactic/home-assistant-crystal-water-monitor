#!/usr/bin/env bash
set -euo pipefail

CONTAINER_NAME="ha-dev"
PORT=8123

if docker ps -a --format '{{.Names}}' | grep -q "^${CONTAINER_NAME}$"; then
  echo "Container '$CONTAINER_NAME' already exists. Starting it..."
  docker start "$CONTAINER_NAME"
else
  echo "Starting Home Assistant dev container..."
  docker run -d \
    --name "$CONTAINER_NAME" \
    -p "${PORT}:8123" \
    -e HA_CRYSTAL_DEV=1 \
    -v "$(pwd)/custom_components:/config/custom_components" \
    ghcr.io/home-assistant/home-assistant:stable
fi

echo ""
echo "Home Assistant running at http://localhost:${PORT}"
echo ""
echo "Useful commands:"
echo "  docker logs -f ${CONTAINER_NAME}   # tail logs"
echo "  docker restart ${CONTAINER_NAME}   # restart after code changes"
echo "  docker stop ${CONTAINER_NAME}      # stop"
