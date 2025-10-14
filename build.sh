#!/usr/bin/env bash
set -euo pipefail

IMAGE="docker.io/hugojosefson/scatter-svg"

echo "Building $IMAGE..."
docker build -t "$IMAGE" .

if [[ "${1:-}" == "--push" ]]; then
  echo "Pushing $IMAGE..."
  docker push "$IMAGE"
  echo "Successfully pushed $IMAGE"
fi

echo "Build complete: $IMAGE"
