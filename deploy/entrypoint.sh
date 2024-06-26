#!/bin/bash
set -e

dind $(dockerd) &

while (! docker info > /dev/null 2>&1); do
    echo "==> Waiting for the Docker daemon to come online..."
    sleep 1
done

exec "$@"
