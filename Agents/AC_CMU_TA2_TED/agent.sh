#!/bin/bash
source ./settings.env

if [ "$1" = "up" ]; then
    echo "Bring up Agent: $AGENT_NAME"
    docker-compose --env-file settings.env up
    docker ps
elif [ "$1" = "upd" ]; then
    echo "Bring up Agent: $AGENT_NAME"
    docker-compose --env-file settings.env up -d
    docker ps
elif [ "$1" = "down" ]; then
    echo "Bring down Agent: $AGENT_NAME"
    docker-compose --env-file settings.env down --remove-orphans
    docker ps
elif [ "$1" = "build" ]; then
    echo "updating the Reference agent image for $AGENT_NAME"
    docker build -t $DOCKER_IMAGE_NAME_LOWERCASE .
elif [ "$1" = "export" ]; then
    echo "exporting the docker image for $AGENT_NAME"
    docker save -o $DOCKER_IMAGE_NAME_LOWERCASE.tar $DOCKER_IMAGE_NAME_LOWERCASE
else
    echo "Usage: ./agent.sh [up|upd|down|build|export]"
fi
