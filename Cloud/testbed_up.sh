#!/bin/bash

echo "Bring up ELK"
pushd ../ELK-Container
export MQTT_HOST=mosquitto
echo $PWD
echo $MQTT_HOST
docker-compose up -d
sleep 10
popd

echo "Bring up metadata server"
pushd ../metadata/metadata-docker
docker-compose up --build -d
popd

echo "Bring up Minecraft"
pushd ../Local
docker network create malmonet
sudo chmod -R 777 ./CLEAN_MAPS
sudo chmod -R 777 ./MinecraftServer
sudo docker-compose -f docker-compose.asistmod.yml up 
popd

docker ps
