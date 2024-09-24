@echo on
::echo "Updating MalmoContainer container"
::pushd ..\MalmoContainer
::docker build -t malmoserver --build-arg CACHE_BREAKER=foo .
::popd

echo "updating MalmoControl container"
pushd ..\MalmoControl
docker build -t malmocontrol --build-arg CACHE_BREAKER=foo .
popd

echo "The reference agent is no longer built or used"
::echo "updating the Reference agent container"
::pushd ..\ReferenceAgents\MQTTPythonReferenceAgent
::docker build -t reference_agent --build-arg CACHE_BREAKER=foo .
::popd

@REM echo "Update the test agent container"
@REM pushd ..\ReferenceAgents\TestAgent
@REM docker build -t test_agent --build-arg CACHE_BREAKER=foo .
@REM popd

echo "Update the client map"
pushd ..\ClientMapSystem
docker build -t client_map --build-arg CACHE_BREAKER=foo .
popd

echo "updating the MQTT Message Validator container"
pushd ..\MQTTValidationServiceContainer
docker build  -t mqttvalidationservice:latest --build-arg CACHE_BREAKER=foo .
popd

echo "updating the ASIST Data Ingester container"
pushd ..\AsistDataIngesterContainer
docker build  -t asistdataingester:latest --build-arg CACHE_BREAKER=foo .
popd

echo "updating ELK container is not built at this time anymore"

echo "List the Docker containers"
docker ps
