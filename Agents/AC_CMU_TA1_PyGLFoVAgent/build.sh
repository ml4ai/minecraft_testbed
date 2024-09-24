#!/bin/bash
source ./settings.env

echo "updating the PyGL FoV container"
docker build -t ${DOCKER_IMAGE_NAME_LOWERCASE} --build-arg CACHE_BREAKER=$(date +%s) .
