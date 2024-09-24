#!/bin/bash

set -u

# Script to automatically build the testbed on Linux and macOS systems.
# Usage: ./testbed_build_ci.sh

# If you want to disable building the Malmo container (which can take a long
# time to build and is not necessary if you are using the ASIST mod), you can
# set the environment variable BUILD_MALMO to 0, e.g.:
#
# BUILD_MALMO=0 ./testbed_build_ci.sh


# Get the top-level ASIST testbed repo directory. The pushd/popd commands use
# this directory, so that this script can be safely executed from any
# directory.
export root_dir="$( cd "$(dirname "${BASH_SOURCE[0]}" )/../" >/dev/null 2>&1 && pwd)"

PATCH=latest
MINOR=latest
MAJOR=latest
LATEST=latest
BUILD=latest

echo "$BUILD"

if [ ! -z "${APTIMADOCKERREGPW:-}" ] ; then
    echo "Logging into gitlab"
    docker login gitlab.asist.aptima.com:5050 --username=dhoward --password=${APTIMADOCKERREGPW}
else 
    echo "Docker login not found"
fi

echo "Updating MalmoControl container"
pushd "$root_dir"/MalmoControl
    if [ ! $BUILD == "latest" ]
    then
        sed -i "s/\"system_version\": \"NOT SET\"/\"system_version\": \"${BUILD}\"/" ../Local/appsettings.Production.json
    fi
    docker build -t malmocontrol:${BUILD} --build-arg CACHE_BREAKER=$(date +%s) .
    if [[ $? -ne 0 ]]; then
        echo "Failed to build MalmoControl container, exiting now."
        exit 1
    fi
popd

echo "Building/updating the Test Agent container"
pushd "$root_dir"/ReferenceAgents/TestAgent
   docker build -t test_agent --build-arg CACHE_BREAKER=$(date +%s) .
   if [[ $? -ne 0 ]]; then
       echo "Failed to build test_agent container, exiting now."
       exit 1
   fi
popd

echo "Building/updating the ClientMap container"
pushd "$root_dir"/ClientMapSystem
    #docker build -t client_map:${BUILD} --build-arg CACHE_BREAKER=$(date +%s) .
    docker build -t client_map --build-arg CACHE_BREAKER=$(date +%s) .
    if [[ $? -ne 0 ]]; then
        echo "Failed to build client_map container, exiting now."
        exit 1
    fi
popd

echo "Building/updating AC_Aptima_TA3_measures"
pushd "$root_dir"/Agents/AC_Aptima_TA3_measures
    source ./settings.env
    cp -R ../../Tools/ihmc-python-agent-helper-package ./ihmc-python-agent-helper-package
    docker build -t ${DOCKER_IMAGE_NAME_LOWERCASE} .
    if [[ $? -ne 0 ]]; then
        echo "Failed to build measures_agent container, exiting now."
        exit 1
    fi
    rm -rf ./ihmc-python-agent-helper-package
popd

echo "Building/updating Gallup Agent GELP"
pushd "$root_dir"/Agents/gallup_agent_gelp
    source ./settings.env
    cp -R ../../Tools/ihmc-python-agent-helper-package ./ihmc-python-agent-helper-package
    docker build -t ${DOCKER_IMAGE_NAME_LOWERCASE} --build-arg CACHE_BREAKER=$(date +%s) .
    if [[ $? -ne 0 ]]; then
        echo "Failed to build gallup_agent_gelp container, exiting now."
        exit 1
    fi
    rm -rf ./ihmc-python-agent-helper-package
popd

echo "Building/updating Gallup Agent GOLD"
pushd "$root_dir"/Agents/gallup_agent_gold
    source ./settings.env
    cp -R ../../Tools/ihmc-python-agent-helper-package ./ihmc-python-agent-helper-package
    docker build -t ${DOCKER_IMAGE_NAME_LOWERCASE} --build-arg CACHE_BREAKER=$(date +%s) .
    if [[ $? -ne 0 ]]; then
        echo "Failed to build gallup_agent_gold container, exiting now."
        exit 1
    fi
    rm -rf ./ihmc-python-agent-helper-package
popd

echo "Building/updating AC_IHMC_TA2_Location-Monitor"
pushd "$root_dir"/Agents/AC_IHMC_TA2_Location-Monitor
    source ./settings.env
    cp -R ../../Tools/ihmc-python-agent-helper-package ./ihmc-python-agent-helper-package
    docker build -t ${DOCKER_IMAGE_NAME_LOWERCASE} --build-arg CACHE_BREAKER=$(date +%s) .
    if [[ $? -ne 0 ]]; then
        echo "Failed to build ${DOCKER_IMAGE_NAME_LOWERCASE} container, exiting now."
        exit 1
    fi
    rm -rf ./ihmc-python-agent-helper-package
popd

echo "Building/updating AC_IHMC_TA2_Player-Proximity Agent"
pushd "$root_dir"/Agents/AC_IHMC_TA2_Player-Proximity
    source ./settings.env
    cp -R ../../Tools/ihmc-python-agent-helper-package ./ihmc-python-agent-helper-package
    docker build -t ${DOCKER_IMAGE_NAME_LOWERCASE} --build-arg CACHE_BREAKER=$(date +%s) .
    if [[ $? -ne 0 ]]; then
        echo "Failed to build ${DOCKER_IMAGE_NAME_LOWERCASE} container, exiting now."
        exit 1
    fi
    rm -rf ./ihmc-python-agent-helper-package
popd

echo "Building/updating AC_IHMC_TA2_Dyad-Reporting Agent"
pushd "$root_dir"/Agents/AC_IHMC_TA2_Dyad-Reporting
    source ./settings.env
    cp -R ../../Tools/ihmc-python-agent-helper-package ./ihmc-python-agent-helper-package
    docker build -t ${DOCKER_IMAGE_NAME_LOWERCASE} --build-arg CACHE_BREAKER=$(date +%s) .
    if [[ $? -ne 0 ]]; then
        echo "Failed to build ${DOCKER_IMAGE_NAME_LOWERCASE} container, exiting now."
        exit 1
    fi
    rm -rf ./ihmc-python-agent-helper-package
popd

echo "Building/updating AC_IHMC_TA2_Joint-Activity-Interdependence"
pushd "$root_dir"/Agents/AC_IHMC_TA2_Joint-Activity-Interdependence
    source ./settings.env
    cp -R ../../Tools/ihmc-python-agent-helper-package ./ihmc-python-agent-helper-package
    cp -R ../AC_CMU_TA1_PyGLFoVAgent/ConfigFolder/maps .
    docker build -t ${DOCKER_IMAGE_NAME_LOWERCASE} --build-arg CACHE_BREAKER=$(date +%s) .
    if [[ $? -ne 0 ]]; then
        echo "Failed to build ${DOCKER_IMAGE_NAME_LOWERCASE} container, exiting now."
        exit 1
    fi
    rm -rf ./ihmc-python-agent-helper-package
    rm -rf ./maps
popd

echo "Building/updating AC_CMUFMS_TA2_Cognitive Agent"
pushd "$root_dir"/Agents/AC_CMUFMS_TA2_Cognitive
    source ./settings.env
    cp -R ../../Tools/ihmc-python-agent-helper-package ./ihmc-python-agent-helper-package
    docker build -t ${DOCKER_IMAGE_NAME_LOWERCASE} --build-arg CACHE_BREAKER=$(date +%s) .
    if [[ $? -ne 0 ]]; then
        echo "Failed to build ${DOCKER_IMAGE_NAME_LOWERCASE} container, exiting now."
        exit 1
    fi
    rm -rf ./ihmc-python-agent-helper-package
popd

echo "Building/updating CMU TA2 Team Effectiveness Diagnostic"
pushd "$root_dir"/Agents/AC_CMU_TA2_TED
    source ./settings.env
    cp -R ../../Tools/ihmc-python-agent-helper-package ./ihmc-python-agent-helper-package
    docker build -t ${DOCKER_IMAGE_NAME_LOWERCASE} --build-arg CACHE_BREAKER=$(date +%s) .
    if [[ $? -ne 0 ]]; then
        echo "Failed to build ${DOCKER_IMAGE_NAME_LOWERCASE} container, exiting now."
        exit 1
    fi
    rm -rf ./ihmc-python-agent-helper-package
popd

echo "Building/updating CMU TA2 BEARD AC"
pushd "$root_dir"/Agents/AC_CMU_TA2_BEARD
    source ./settings.env
    cp -R ../../Tools/ihmc-python-agent-helper-package ./ihmc-python-agent-helper-package
    docker build -t ${DOCKER_IMAGE_NAME_LOWERCASE} --build-arg CACHE_BREAKER=$(date +%s) .
    if [[ $? -ne 0 ]]; then
        echo "Failed to build ${DOCKER_IMAGE_NAME_LOWERCASE} container, exiting now."
        exit 1
    fi
    rm -rf ./ihmc-python-agent-helper-package
popd

echo "Building/updating AC_CMU_TA1_PyGLFoVAgent"
pushd "$root_dir"/Agents/AC_CMU_TA1_PyGLFoVAgent
    source ./settings.env
    docker build -t ${DOCKER_IMAGE_NAME_LOWERCASE} --build-arg CACHE_BREAKER=$(date +%s) .
    if [[ $? -ne 0 ]]; then
        echo "Failed to build pygl_fov_agent container, exiting now."
        exit 1
    fi
popd

echo "Building/updating ASR Agent done at up time"

echo "Building/updating Rutgers Utility AC"
pushd "$root_dir"/Agents/RutgersUtilityAC
    source ./settings.env
    cp -R ../../Tools/ihmc-python-agent-helper-package ./ihmc-python-agent-helper-package
    docker build -t ${DOCKER_IMAGE_NAME_LOWERCASE} --build-arg CACHE_BREAKER=$(date +%s) .
    if [[ $? -ne 0 ]]; then
        echo "Failed to build ${DOCKER_IMAGE_NAME_LOWERCASE} container, exiting now."
        exit 1
    fi
    rm -rf ./ihmc-python-agent-helper-package
popd

echo "Building/updating the MQTT Message Validator container"
pushd "$root_dir"/MQTTValidationServiceContainer
    docker build  -t mqttvalidationservice:${BUILD} --build-arg CACHE_BREAKER=$(date +%s) .
    if [[ $? -ne 0 ]]; then
        echo "Failed to build mqttvalidationservice container, exiting now."
        exit 1
    fi
popd

echo "Building/updating the ASIST Data Ingester container"
pushd "$root_dir"/AsistDataIngesterContainer
    docker build  -t asistdataingester:${BUILD} --build-arg CACHE_BREAKER=$(date +%s) .
    if [[ $? -ne 0 ]]; then
        echo "Failed to build asistdataingester container, exiting now."
        exit 1
    fi
popd

echo "Building/updating the Logstash container"
pushd "$root_dir"/ELK-Container/context/logstash
    docker build  -t logstash:${BUILD} .
    if [[ $? -ne 0 ]]; then
        echo "Failed to build logstash container, exiting now."
        exit 1
    fi
popd

echo "Building/updating the Postgres container"
pushd "$root_dir"/metadata/metadata-docker
    docker build  -t postgres:${BUILD} -f context/postgres/Dockerfile .
    if [[ $? -ne 0 ]]; then
        echo "Failed to build postgres container, exiting now."
        exit 1
    fi
popd

echo "Building/updating the metadata-app container"
pushd "$root_dir"/metadata/metadata-docker
    docker build  -t metadata-app:${BUILD} -f context/metadata-app/Dockerfile .
    if [[ $? -ne 0 ]]; then
        echo "Failed to build metadata-app container, exiting now."
        exit 1
    fi
popd

echo "Building/updating the metadata-msg container"
pushd "$root_dir"/metadata/metadata-docker
    if [ ! $BUILD == "latest" ]
    then
        sed -i "s/TESTBED_VERSION=NOT SET/TESTBED_VERSION=${BUILD}/" metadata/metadata-docker/metadata-app.env
    fi
    docker build  -t metadata-msg:${BUILD} -f context/metadata-msg/Dockerfile .
    if [[ $? -ne 0 ]]; then
        echo "Failed to build metadata-msg container, exiting now."
        exit 1
    fi
popd

echo "Building/updating the metadata-web container"
pushd "$root_dir"/metadata/metadata-web
    if [ ! $BUILD == "latest" ]
    then
        sed -i "s/TESTBED_VERSION=NOT SET/TESTBED_VERSION=${BUILD}/" metadata/metadata-web/metadata-web.env
        # WE SHOULD UPDATE THE HOST HERE TO SO WE DON'T HAVE TO MANUALLY DO IT EACH TIME
    fi
    docker build  -t metadata-web:${BUILD} .
    if [[ $? -ne 0 ]]; then
        echo "Failed to build metadata-web container, exiting now."
        exit 1
    fi
popd

echo "Building/updating CMU-TA1 ATLAS Agent"
pushd "$root_dir"/Agents/ASI_CMU_TA1_ATLAS
    source ./settings.env
    docker build -t ${DOCKER_IMAGE_NAME_LOWERCASE} --build-arg CACHE_BREAKER=$(date +%s) .
    if [[ $? -ne 0 ]]; then
        echo "Failed to build asi_cmu_ta1_atlas container, exiting now."
        exit 1
    fi
popd

echo "Building/updating SIFT Asistant Agent"
pushd "$root_dir"/Agents/SIFT_Asistant_Agent
    docker-compose pull
    if [[ $? -ne 0 ]]; then
        echo "Failed to pull sift_asistant, exiting now."
        exit 1
    fi
popd

echo "Building/updating Atomic Agent"
pushd "$root_dir"/Agents/atomic_agent
    #source ./settings.env
    docker-compose --env-file settings.env pull
    #./agent.sh build
    if [[ $? -ne 0 ]]; then
        echo "Failed to pull atomic_agent, exiting now."
        exit 1
    fi
popd

echo "Building/updating Cornell Team trust AC"
pushd "$root_dir"/Agents/ac_cornell_ta2_teamtrust
    source ./settings.env
    docker-compose --env-file settings.env pull
    if [[ $? -ne 0 ]]; then
        echo "Failed to build ${DOCKER_IMAGE_NAME_LOWERCASE} container, exiting now."
        exit 1
    fi
    rm -rf ./ihmc-python-agent-helper-package
popd


# Check amount of virtual memory and increase it if needed.
if [[ $OSTYPE == "linux-gnu" ]]; then
    virtual_memory_limit=`sysctl vm.max_map_count | cut -d' ' -f3`
    min_virtual_memory_required=262144
    if [[ $virtual_memory_limit -lt $min_virtual_memory_required ]]; then
        echo "Increasing virtual memory limit from ${virtual_memory_limit} to"
        echo "${min_virtual_memory_required}, the minimum required for the ELK stack."
        echo "(See https://www.elastic.co/guide/en/elasticsearch/reference/current/vm-max-map-count.html)"
        echo "If you want this value to persist across reboots of the computer,"
        echo "add the following line to /etc/sysctl.conf\n:"
        echo "    vm.max_map_count=262144"

	memTest=$(sudo sysctl -w vm.max_map_count=$min_virtual_memory_required 2>&1)
	if [[ $memTest == *"permission"* ]]; then
            echo "Failed to increase virtual memory, exiting now. You "\
                 "may need to run the following command as root:"
            echo ""
            echo "     sysctl -w vm.max_map_count=${min_virtual_memory_required}"
            exit 1
        fi
    fi
fi

echo "ELK container is now composed at up time"



exit 0
