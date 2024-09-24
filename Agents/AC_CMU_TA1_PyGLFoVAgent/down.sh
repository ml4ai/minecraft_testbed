#!/bin/bash

echo "Bring down PyGL FoV Agent"
docker-compose --env-file settings.env down --remove-orphans
docker ps
