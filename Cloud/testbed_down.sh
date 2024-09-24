#!/bin/bash

echo "Bring down ELK"
pushd ../ELK-Container
docker-compose down --remove-orphans
popd

echo "Bring down metadata server"
pushd ../metadata/metadata-docker
docker-compose down --remove-orphans
popd

echo "Bring down Minecraft"
pushd ../Local
docker-compose -f docker-compose.asistmod.yml down --remove-orphans
popd

echo "Stop the the rest of the containers"

docker container stop $(docker container ls -q )

docker ps
