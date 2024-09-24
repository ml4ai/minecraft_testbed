#!/bin/bash

echo "Bring up PyGL FoV Agent"
# Creates asist_net if it doesn't already exist.  Useful for local testing.
docker network inspect asist_net > /dev/null 2>&1 || docker network create asist_net

docker-compose --env-file settings.env up -d
docker ps
