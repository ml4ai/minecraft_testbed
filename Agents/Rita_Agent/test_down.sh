#!/usr/bin/env bash

echo "$PWD: Starting Rita Agent"
docker-compose --env-file settings.env down