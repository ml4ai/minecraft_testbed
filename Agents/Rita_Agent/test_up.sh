#!/usr/bin/env bash

echo "$PWD: Starting Rita Agent"
dte=$(date "+%B-%Y-%d")
log_dir="logs-${dte}"
export SERVICE_LOGS_DIR="$log_dir/"
echo "${SERVICE_LOGS_DIR} Log dirs for this instantiation of Rita"

docker-compose --env-file settings.env up