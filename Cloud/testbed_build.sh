#!/bin/bash
echo "Updating MalmoContainer container"
pushd ../MalmoContainer
docker build -t malmoserver --build-arg CACHE_BREAKER=foo .
popd

echo "updating MalmoControl container"
pushd ../MalmoControl
docker build -t malmocontrol --build-arg CACHE_BREAKER=foo .
popd

echo "updating the Reference agent container"
pushd ../ReferenceAgents/MQTTPythonReferenceAgent
docker build -t reference_agent --build-arg CACHE_BREAKER=foo .
popd

echo "updating the MQTT Message Validator container"
pushd ../MQTTValidationServiceContainer
docker build  -t mqttvalidationservice:lastest --build-arg CACHE_BREAKER=foo .
popd

echo "updating ELK container"
pushd ../ELK-Container
export MQTT_HOST=mosquitto
sysctl -w vm.max_map_count=262144
docker-compose -f setup.yml up
popd