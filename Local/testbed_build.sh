#!/bin/bash

set -u

# Script to automatically build the testbed on Linux and macOS systems.
# Usage: ./testbed_build.sh

# If you want to disable building the Malmo container (which can take a long
# time to build and is not necessary if you are using the ASIST mod), you can
# set the environment variable BUILD_MALMO to 0, e.g.:
#
# BUILD_MALMO=0 ./testbed_build.sh


# Get the top-level ASIST testbed repo directory. The pushd/popd commands use
# this directory, so that this script can be safely executed from any
# directory.
export root_dir="$( cd "$(dirname "${BASH_SOURCE[0]}" )/../" >/dev/null 2>&1 && pwd)"
FILE=../version.txt
if test -f "$FILE"; then
    TAG=$(cat ../version.txt)
    # echo $TAG > 'latest-version.txt'
    BUILD_TYPE=""
    BUILD_NUMBER=""
    if [[ "$TAG" == *"-"* ]]; then
        BUILD="${TAG#*-}"
        BUILD_TYPE="-${BUILD%%.*}"
        BUILD_NUMBER=".${BUILD#*.}"
    fi

    # Creates strings with the following structure:
    # BUILD: 1.0.0-dev.0
    # PATCH: 1.0.0-dev
    # MINOR: 1.0-dev
    # MAJOR: 1-dev
    PATCH="${TAG%-*}"
    MINOR="${PATCH%.*}"
    MAJOR="${MINOR%.*}"
    BUILD="$PATCH"

    BUILD="$PATCH$BUILD_TYPE$BUILD_NUMBER"
    PATCH="$PATCH$BUILD_TYPE"
    MINOR="$MINOR$BUILD_TYPE"
    MAJOR="$MAJOR$BUILD_TYPE"
else
    PATCH=latest
    MINOR=latest
    MAJOR=latest
    LATEST=latest
    BUILD=latest
fi

echo "$BUILD"

# echo "Building/updating MalmoContainer container"
# export BUILD_MALMO=${BUILD_MALMO:-1}
# if (( $BUILD_MALMO )); then
#     pushd "$root_dir"/MalmoContainer
#         docker build -t malmoserver:${PATCH} --build-arg CACHE_BREAKER=$(date +%s) .
#         if [[ $? -ne 0 ]]; then
#             echo "Failed to build MalmoContainer container, exiting now."
#             exit 1
#         fi
#         if [ ! -z "${APTIMADOCKERREGPW:-}" ] ; then
#             docker login gitlab.asist.aptima.com:5050 --username=dhoward --password=${APTIMADOCKERREGPW}
#             docker tag malmoserver:${PATCH} registry.gitlab.com/artificialsocialintelligence/study3/malmoserver:${PATCH}
#             docker tag malmoserver:${PATCH} registry.gitlab.com/artificialsocialintelligence/study3/malmoserver:${MINOR}
#             docker tag malmoserver:${PATCH} registry.gitlab.com/artificialsocialintelligence/study3/malmoserver:${MAJOR}
#             docker push registry.gitlab.com/artificialsocialintelligence/study3/malmoserver:${PATCH}
#             docker push registry.gitlab.com/artificialsocialintelligence/study3/malmoserver:${MINOR}
#             docker push registry.gitlab.com/artificialsocialintelligence/study3/malmoserver:${MAJOR}
#             docker push registry.gitlab.com/artificialsocialintelligence/study3/malmoserver:latest
#         fi
#     popd
# fi

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
    if [ ! -z "${APTIMADOCKERREGPW:-}" ] ; then
        docker login gitlab.asist.aptima.com:5050 --username=dhoward --password=${APTIMADOCKERREGPW}
        docker tag malmocontrol:${BUILD} registry.gitlab.com/artificialsocialintelligence/study3/malmocontrol:${BUILD}
        docker tag malmocontrol:${BUILD} registry.gitlab.com/artificialsocialintelligence/study3/malmocontrol:${MINOR}
        docker tag malmocontrol:${BUILD} registry.gitlab.com/artificialsocialintelligence/study3/malmocontrol:${MAJOR}
        docker tag malmocontrol:${BUILD} registry.gitlab.com/artificialsocialintelligence/study3/malmocontrol:latest
        docker push registry.gitlab.com/artificialsocialintelligence/study3/malmocontrol:${BUILD}
        docker push registry.gitlab.com/artificialsocialintelligence/study3/malmocontrol:${MINOR}
        docker push registry.gitlab.com/artificialsocialintelligence/study3/malmocontrol:${MAJOR}
        docker push registry.gitlab.com/artificialsocialintelligence/study3/malmocontrol:latest
    fi
popd

echo "The Reference agent is no longer built or used"
#echo "Building/updating the Reference agent container"
#pushd "$root_dir"/ReferenceAgents/MQTTPythonReferenceAgent
#    docker build -t reference_agent --build-arg CACHE_BREAKER=$(date +%s) .
#    if [[ $? -ne 0 ]]; then
#        echo "Failed to build reference_agent container, exiting now."
#        exit 1
#    fi
#popd

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
    if [ ! -z "${APTIMADOCKERREGPW:-}" ] ; then
        docker login gitlab.asist.aptima.com:5050 --username=dhoward --password=${APTIMADOCKERREGPW}
        docker tag client_map:${BUILD} registry.gitlab.com/artificialsocialintelligence/study3/client_map:${BUILD}
        docker tag client_map:${BUILD} registry.gitlab.com/artificialsocialintelligence/study3/client_map:${MINOR}
        docker tag client_map:${BUILD} registry.gitlab.com/artificialsocialintelligence/study3/client_map:${MAJOR}
        docker tag client_map:${BUILD} registry.gitlab.com/artificialsocialintelligence/study3/client_map:latest
        docker push registry.gitlab.com/artificialsocialintelligence/study3/client_map:${BUILD}
        docker push registry.gitlab.com/artificialsocialintelligence/study3/client_map:${MINOR}
        docker push registry.gitlab.com/artificialsocialintelligence/study3/client_map:${MAJOR}
        docker push registry.gitlab.com/artificialsocialintelligence/study3/client_map:latest
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
    if [ ! -z "${APTIMADOCKERREGPW:-}" ] ; then
        docker login gitlab.asist.aptima.com:5050 --username=dhoward --password=${APTIMADOCKERREGPW}
        docker tag ${DOCKER_IMAGE_NAME_LOWERCASE} registry.gitlab.com/artificialsocialintelligence/study3/${DOCKER_IMAGE_NAME_LOWERCASE}:${BUILD}
        docker tag ${DOCKER_IMAGE_NAME_LOWERCASE} registry.gitlab.com/artificialsocialintelligence/study3/${DOCKER_IMAGE_NAME_LOWERCASE}:${MINOR}
        docker tag ${DOCKER_IMAGE_NAME_LOWERCASE} registry.gitlab.com/artificialsocialintelligence/study3/${DOCKER_IMAGE_NAME_LOWERCASE}:${MAJOR}
        docker tag ${DOCKER_IMAGE_NAME_LOWERCASE} registry.gitlab.com/artificialsocialintelligence/study3/${DOCKER_IMAGE_NAME_LOWERCASE}:latest
        docker push registry.gitlab.com/artificialsocialintelligence/study3/${DOCKER_IMAGE_NAME_LOWERCASE}:${BUILD}
        docker push registry.gitlab.com/artificialsocialintelligence/study3/${DOCKER_IMAGE_NAME_LOWERCASE}:${MINOR}
        docker push registry.gitlab.com/artificialsocialintelligence/study3/${DOCKER_IMAGE_NAME_LOWERCASE}:${MAJOR}
        docker push registry.gitlab.com/artificialsocialintelligence/study3/${DOCKER_IMAGE_NAME_LOWERCASE}:latest
    fi
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
    if [ ! -z "${APTIMADOCKERREGPW:-}" ] ; then
        docker login gitlab.asist.aptima.com:5050 --username=dhoward --password=${APTIMADOCKERREGPW}
        docker tag ${DOCKER_IMAGE_NAME_LOWERCASE}:${BUILD} registry.gitlab.com/artificialsocialintelligence/study3/${DOCKER_IMAGE_NAME_LOWERCASE}:${BUILD}
        docker tag ${DOCKER_IMAGE_NAME_LOWERCASE}:${BUILD} registry.gitlab.com/artificialsocialintelligence/study3/${DOCKER_IMAGE_NAME_LOWERCASE}:${MINOR}
        docker tag ${DOCKER_IMAGE_NAME_LOWERCASE}:${BUILD} registry.gitlab.com/artificialsocialintelligence/study3/${DOCKER_IMAGE_NAME_LOWERCASE}:${MAJOR}
        docker tag ${DOCKER_IMAGE_NAME_LOWERCASE}:${BUILD} registry.gitlab.com/artificialsocialintelligence/study3/${DOCKER_IMAGE_NAME_LOWERCASE}:latest
        docker push registry.gitlab.com/artificialsocialintelligence/study3/${DOCKER_IMAGE_NAME_LOWERCASE}:${BUILD}
        docker push registry.gitlab.com/artificialsocialintelligence/study3/${DOCKER_IMAGE_NAME_LOWERCASE}:${MINOR}
        docker push registry.gitlab.com/artificialsocialintelligence/study3/${DOCKER_IMAGE_NAME_LOWERCASE}:${MAJOR}
        docker push registry.gitlab.com/artificialsocialintelligence/study3/${DOCKER_IMAGE_NAME_LOWERCASE}:latest
    fi
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
    if [ ! -z "${APTIMADOCKERREGPW:-}" ] ; then
        docker login gitlab.asist.aptima.com:5050 --username=dhoward --password=${APTIMADOCKERREGPW}
        docker tag ${DOCKER_IMAGE_NAME_LOWERCASE}:${BUILD} registry.gitlab.com/artificialsocialintelligence/study3/${DOCKER_IMAGE_NAME_LOWERCASE}:${BUILD}
        docker tag ${DOCKER_IMAGE_NAME_LOWERCASE}:${BUILD} registry.gitlab.com/artificialsocialintelligence/study3/${DOCKER_IMAGE_NAME_LOWERCASE}:${MINOR}
        docker tag ${DOCKER_IMAGE_NAME_LOWERCASE}:${BUILD} registry.gitlab.com/artificialsocialintelligence/study3/${DOCKER_IMAGE_NAME_LOWERCASE}:${MAJOR}
        docker tag ${DOCKER_IMAGE_NAME_LOWERCASE}:${BUILD} registry.gitlab.com/artificialsocialintelligence/study3/${DOCKER_IMAGE_NAME_LOWERCASE}:latest
        docker push registry.gitlab.com/artificialsocialintelligence/study3/${DOCKER_IMAGE_NAME_LOWERCASE}:${BUILD}
        docker push registry.gitlab.com/artificialsocialintelligence/study3/${DOCKER_IMAGE_NAME_LOWERCASE}:${MINOR}
        docker push registry.gitlab.com/artificialsocialintelligence/study3/${DOCKER_IMAGE_NAME_LOWERCASE}:${MAJOR}
        docker push registry.gitlab.com/artificialsocialintelligence/study3/${DOCKER_IMAGE_NAME_LOWERCASE}:latest
    fi
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
    if [ ! -z "${APTIMADOCKERREGPW:-}" ] ; then
        docker login gitlab.asist.aptima.com:5050 --username=dhoward --password=${APTIMADOCKERREGPW}
        docker tag ${DOCKER_IMAGE_NAME_LOWERCASE} registry.gitlab.com/artificialsocialintelligence/study3/${DOCKER_IMAGE_NAME_LOWERCASE}:${BUILD}
        docker tag ${DOCKER_IMAGE_NAME_LOWERCASE} registry.gitlab.com/artificialsocialintelligence/study3/${DOCKER_IMAGE_NAME_LOWERCASE}:${MINOR}
        docker tag ${DOCKER_IMAGE_NAME_LOWERCASE} registry.gitlab.com/artificialsocialintelligence/study3/${DOCKER_IMAGE_NAME_LOWERCASE}:${MAJOR}
        docker tag ${DOCKER_IMAGE_NAME_LOWERCASE} registry.gitlab.com/artificialsocialintelligence/study3/${DOCKER_IMAGE_NAME_LOWERCASE}:latest
        docker push registry.gitlab.com/artificialsocialintelligence/study3/${DOCKER_IMAGE_NAME_LOWERCASE}:${BUILD}
        docker push registry.gitlab.com/artificialsocialintelligence/study3/${DOCKER_IMAGE_NAME_LOWERCASE}:${MINOR}
        docker push registry.gitlab.com/artificialsocialintelligence/study3/${DOCKER_IMAGE_NAME_LOWERCASE}:${MAJOR}
        docker push registry.gitlab.com/artificialsocialintelligence/study3/${DOCKER_IMAGE_NAME_LOWERCASE}:latest
    fi
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
    if [ ! -z "${APTIMADOCKERREGPW:-}" ] ; then
        docker login gitlab.asist.aptima.com:5050 --username=dhoward --password=${APTIMADOCKERREGPW}
        docker tag ${DOCKER_IMAGE_NAME_LOWERCASE}:${BUILD} registry.gitlab.com/artificialsocialintelligence/study3/${DOCKER_IMAGE_NAME_LOWERCASE}:${BUILD}
        docker tag ${DOCKER_IMAGE_NAME_LOWERCASE}:${BUILD} registry.gitlab.com/artificialsocialintelligence/study3/${DOCKER_IMAGE_NAME_LOWERCASE}:${MINOR}
        docker tag ${DOCKER_IMAGE_NAME_LOWERCASE}:${BUILD} registry.gitlab.com/artificialsocialintelligence/study3/${DOCKER_IMAGE_NAME_LOWERCASE}:${MAJOR}
        docker tag ${DOCKER_IMAGE_NAME_LOWERCASE}:${BUILD} registry.gitlab.com/artificialsocialintelligence/study3/${DOCKER_IMAGE_NAME_LOWERCASE}:latest
        docker push registry.gitlab.com/artificialsocialintelligence/study3/${DOCKER_IMAGE_NAME_LOWERCASE}:${BUILD}
        docker push registry.gitlab.com/artificialsocialintelligence/study3/${DOCKER_IMAGE_NAME_LOWERCASE}:${MINOR}
        docker push registry.gitlab.com/artificialsocialintelligence/study3/${DOCKER_IMAGE_NAME_LOWERCASE}:${MAJOR}
        docker push registry.gitlab.com/artificialsocialintelligence/study3/${DOCKER_IMAGE_NAME_LOWERCASE}:latest
    fi
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
    if [ ! -z "${APTIMADOCKERREGPW:-}" ] ; then
        docker login gitlab.asist.aptima.com:5050 --username=dhoward --password=${APTIMADOCKERREGPW}
        docker tag ${DOCKER_IMAGE_NAME_LOWERCASE}:${BUILD} registry.gitlab.com/artificialsocialintelligence/study3/${DOCKER_IMAGE_NAME_LOWERCASE}:${BUILD}
        docker tag ${DOCKER_IMAGE_NAME_LOWERCASE}:${BUILD} registry.gitlab.com/artificialsocialintelligence/study3/${DOCKER_IMAGE_NAME_LOWERCASE}:${MINOR}
        docker tag ${DOCKER_IMAGE_NAME_LOWERCASE}:${BUILD} registry.gitlab.com/artificialsocialintelligence/study3/${DOCKER_IMAGE_NAME_LOWERCASE}:${MAJOR}
        docker tag ${DOCKER_IMAGE_NAME_LOWERCASE}:${BUILD} registry.gitlab.com/artificialsocialintelligence/study3/${DOCKER_IMAGE_NAME_LOWERCASE}:latest
        docker push registry.gitlab.com/artificialsocialintelligence/study3/${DOCKER_IMAGE_NAME_LOWERCASE}:${BUILD}
        docker push registry.gitlab.com/artificialsocialintelligence/study3/${DOCKER_IMAGE_NAME_LOWERCASE}:${MINOR}
        docker push registry.gitlab.com/artificialsocialintelligence/study3/${DOCKER_IMAGE_NAME_LOWERCASE}:${MAJOR}
        docker push registry.gitlab.com/artificialsocialintelligence/study3/${DOCKER_IMAGE_NAME_LOWERCASE}:latest
    fi
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
    if [ ! -z "${APTIMADOCKERREGPW:-}" ] ; then
        docker login gitlab.asist.aptima.com:5050 --username=dhoward --password=${APTIMADOCKERREGPW}
        docker tag ${DOCKER_IMAGE_NAME_LOWERCASE}:${BUILD} registry.gitlab.com/artificialsocialintelligence/study3/${DOCKER_IMAGE_NAME_LOWERCASE}:${BUILD}
        docker tag ${DOCKER_IMAGE_NAME_LOWERCASE}:${BUILD} registry.gitlab.com/artificialsocialintelligence/study3/${DOCKER_IMAGE_NAME_LOWERCASE}:${MINOR}
        docker tag ${DOCKER_IMAGE_NAME_LOWERCASE}:${BUILD} registry.gitlab.com/artificialsocialintelligence/study3/${DOCKER_IMAGE_NAME_LOWERCASE}:${MAJOR}
        docker tag ${DOCKER_IMAGE_NAME_LOWERCASE}:${BUILD} registry.gitlab.com/artificialsocialintelligence/study3/${DOCKER_IMAGE_NAME_LOWERCASE}:latest
        docker push registry.gitlab.com/artificialsocialintelligence/study3/${DOCKER_IMAGE_NAME_LOWERCASE}:${BUILD}
        docker push registry.gitlab.com/artificialsocialintelligence/study3/${DOCKER_IMAGE_NAME_LOWERCASE}:${MINOR}
        docker push registry.gitlab.com/artificialsocialintelligence/study3/${DOCKER_IMAGE_NAME_LOWERCASE}:${MAJOR}
        docker push registry.gitlab.com/artificialsocialintelligence/study3/${DOCKER_IMAGE_NAME_LOWERCASE}:latest
    fi
popd

echo "Building/updating AC_CMU_TA1_PyGLFoVAgent"
pushd "$root_dir"/Agents/AC_CMU_TA1_PyGLFoVAgent
    source ./settings.env
    docker build -t ${DOCKER_IMAGE_NAME_LOWERCASE} --build-arg CACHE_BREAKER=$(date +%s) .
    if [[ $? -ne 0 ]]; then
        echo "Failed to build pygl_fov_agent container, exiting now."
        exit 1
    fi
    if [ ! -z "${APTIMADOCKERREGPW:-}" ] ; then
        docker login gitlab.asist.aptima.com:5050 --username=dhoward --password=${APTIMADOCKERREGPW}
        docker tag ${DOCKER_IMAGE_NAME_LOWERCASE}:${BUILD} registry.gitlab.com/artificialsocialintelligence/study3/${DOCKER_IMAGE_NAME_LOWERCASE}:${BUILD}
        docker tag ${DOCKER_IMAGE_NAME_LOWERCASE}:${BUILD} registry.gitlab.com/artificialsocialintelligence/study3/${DOCKER_IMAGE_NAME_LOWERCASE}:${MINOR}
        docker tag ${DOCKER_IMAGE_NAME_LOWERCASE}:${BUILD} registry.gitlab.com/artificialsocialintelligence/study3/${DOCKER_IMAGE_NAME_LOWERCASE}:${MAJOR}
        docker tag ${DOCKER_IMAGE_NAME_LOWERCASE}:${BUILD} registry.gitlab.com/artificialsocialintelligence/study3/${DOCKER_IMAGE_NAME_LOWERCASE}:latest
        docker push registry.gitlab.com/artificialsocialintelligence/study3/${DOCKER_IMAGE_NAME_LOWERCASE}:${BUILD}
        docker push registry.gitlab.com/artificialsocialintelligence/study3/${DOCKER_IMAGE_NAME_LOWERCASE}:${MINOR}
        docker push registry.gitlab.com/artificialsocialintelligence/study3/${DOCKER_IMAGE_NAME_LOWERCASE}:${MAJOR}
        docker push registry.gitlab.com/artificialsocialintelligence/study3/${DOCKER_IMAGE_NAME_LOWERCASE}:latest
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
    if [ ! -z "${APTIMADOCKERREGPW:-}" ] ; then
        docker login gitlab.asist.aptima.com:5050 --username=dhoward --password=${APTIMADOCKERREGPW}
        docker tag mqttvalidationservice:${BUILD} registry.gitlab.com/artificialsocialintelligence/study3/mqttvalidationservice:${BUILD}
        docker tag mqttvalidationservice:${BUILD} registry.gitlab.com/artificialsocialintelligence/study3/mqttvalidationservice:${MINOR}
        docker tag mqttvalidationservice:${BUILD} registry.gitlab.com/artificialsocialintelligence/study3/mqttvalidationservice:${MAJOR}
        docker tag mqttvalidationservice:${BUILD} registry.gitlab.com/artificialsocialintelligence/study3/mqttvalidationservice:latest
        docker push registry.gitlab.com/artificialsocialintelligence/study3/mqttvalidationservice:${BUILD}
        docker push registry.gitlab.com/artificialsocialintelligence/study3/mqttvalidationservice:${MINOR}
        docker push registry.gitlab.com/artificialsocialintelligence/study3/mqttvalidationservice:${MAJOR}
        docker push registry.gitlab.com/artificialsocialintelligence/study3/mqttvalidationservice:latest
    fi
popd

echo "Building/updating the ASIST Data Ingester container"
pushd "$root_dir"/AsistDataIngesterContainer
    docker build  -t asistdataingester:${BUILD} --build-arg CACHE_BREAKER=$(date +%s) .
    if [[ $? -ne 0 ]]; then
        echo "Failed to build asistdataingester container, exiting now."
        exit 1
    fi
    if [ ! -z "${APTIMADOCKERREGPW:-}" ] ; then
        docker login gitlab.asist.aptima.com:5050 --username=dhoward --password=${APTIMADOCKERREGPW}
        docker tag asistdataingester:${BUILD} registry.gitlab.com/artificialsocialintelligence/study3/asistdataingester:${BUILD}
        docker tag asistdataingester:${BUILD} registry.gitlab.com/artificialsocialintelligence/study3/asistdataingester:${MINOR}
        docker tag asistdataingester:${BUILD} registry.gitlab.com/artificialsocialintelligence/study3/asistdataingester:${MAJOR}
        docker tag asistdataingester:${BUILD} registry.gitlab.com/artificialsocialintelligence/study3/asistdataingester:latest
        docker push registry.gitlab.com/artificialsocialintelligence/study3/asistdataingester:${BUILD}
        docker push registry.gitlab.com/artificialsocialintelligence/study3/asistdataingester:${MINOR}
        docker push registry.gitlab.com/artificialsocialintelligence/study3/asistdataingester:${MAJOR}
        docker push registry.gitlab.com/artificialsocialintelligence/study3/asistdataingester:latest
    fi
popd

echo "Building/updating the Logstash container"
pushd "$root_dir"/ELK-Container/context/logstash
    docker build  -t logstash:${BUILD} .
    if [[ $? -ne 0 ]]; then
        echo "Failed to build logstash container, exiting now."
        exit 1
    fi
    if [ ! -z "${APTIMADOCKERREGPW:-}" ] ; then
        docker login gitlab.asist.aptima.com:5050 --username=dhoward --password=${APTIMADOCKERREGPW}
        docker tag logstash:${BUILD} registry.gitlab.com/artificialsocialintelligence/study3/logstash:${BUILD}
        docker tag logstash:${BUILD} registry.gitlab.com/artificialsocialintelligence/study3/logstash:${MINOR}
        docker tag logstash:${BUILD} registry.gitlab.com/artificialsocialintelligence/study3/logstash:${MAJOR}
        docker tag logstash:${BUILD} registry.gitlab.com/artificialsocialintelligence/study3/logstash:latest
        docker push registry.gitlab.com/artificialsocialintelligence/study3/logstash:${BUILD}
        docker push registry.gitlab.com/artificialsocialintelligence/study3/logstash:${MINOR}
        docker push registry.gitlab.com/artificialsocialintelligence/study3/logstash:${MAJOR}
        docker push registry.gitlab.com/artificialsocialintelligence/study3/logstash:latest
    fi
popd

echo "Building/updating the Postgres container"
pushd "$root_dir"/metadata/metadata-docker
    docker build  -t postgres:${BUILD} -f context/postgres/Dockerfile .
    if [[ $? -ne 0 ]]; then
        echo "Failed to build postgres container, exiting now."
        exit 1
    fi
    if [ ! -z "${APTIMADOCKERREGPW:-}" ] ; then
        docker login gitlab.asist.aptima.com:5050 --username=dhoward --password=${APTIMADOCKERREGPW}
        docker tag postgres:${BUILD} registry.gitlab.com/artificialsocialintelligence/study3/postgres:${BUILD}
        docker tag postgres:${BUILD} registry.gitlab.com/artificialsocialintelligence/study3/postgres:${MINOR}
        docker tag postgres:${BUILD} registry.gitlab.com/artificialsocialintelligence/study3/postgres:${MAJOR}
        docker tag postgres:${BUILD} registry.gitlab.com/artificialsocialintelligence/study3/postgres:latest
        docker push registry.gitlab.com/artificialsocialintelligence/study3/postgres:${BUILD}
        docker push registry.gitlab.com/artificialsocialintelligence/study3/postgres:${MINOR}
        docker push registry.gitlab.com/artificialsocialintelligence/study3/postgres:${MAJOR}
        docker push registry.gitlab.com/artificialsocialintelligence/study3/postgres:latest
    fi
popd

echo "Building/updating the metadata-app container"
pushd "$root_dir"/metadata/metadata-docker
    docker build  -t metadata-app:${BUILD} -f context/metadata-app/Dockerfile .
    if [[ $? -ne 0 ]]; then
        echo "Failed to build metadata-app container, exiting now."
        exit 1
    fi
    if [ ! -z "${APTIMADOCKERREGPW:-}" ] ; then
        docker login gitlab.asist.aptima.com:5050 --username=dhoward --password=${APTIMADOCKERREGPW}
        docker tag metadata-app:${BUILD} registry.gitlab.com/artificialsocialintelligence/study3/metadata-app:${BUILD}
        docker tag metadata-app:${BUILD} registry.gitlab.com/artificialsocialintelligence/study3/metadata-app:${MINOR}
        docker tag metadata-app:${BUILD} registry.gitlab.com/artificialsocialintelligence/study3/metadata-app:${MAJOR}
        docker tag metadata-app:${BUILD} registry.gitlab.com/artificialsocialintelligence/study3/metadata-app:latest
        docker push registry.gitlab.com/artificialsocialintelligence/study3/metadata-app:${BUILD}
        docker push registry.gitlab.com/artificialsocialintelligence/study3/metadata-app:${MINOR}
        docker push registry.gitlab.com/artificialsocialintelligence/study3/metadata-app:${MAJOR}
        docker push registry.gitlab.com/artificialsocialintelligence/study3/metadata-app:latest
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
    if [ ! -z "${APTIMADOCKERREGPW:-}" ] ; then
        docker login gitlab.asist.aptima.com:5050 --username=dhoward --password=${APTIMADOCKERREGPW}
        docker tag metadata-msg:${BUILD} registry.gitlab.com/artificialsocialintelligence/study3/metadata-msg:${BUILD}
        docker tag metadata-msg:${BUILD} registry.gitlab.com/artificialsocialintelligence/study3/metadata-msg:${MINOR}
        docker tag metadata-msg:${BUILD} registry.gitlab.com/artificialsocialintelligence/study3/metadata-msg:${MAJOR}
        docker tag metadata-msg:${BUILD} registry.gitlab.com/artificialsocialintelligence/study3/metadata-msg:latest
        docker push registry.gitlab.com/artificialsocialintelligence/study3/metadata-msg:${BUILD}
        docker push registry.gitlab.com/artificialsocialintelligence/study3/metadata-msg:${MINOR}
        docker push registry.gitlab.com/artificialsocialintelligence/study3/metadata-msg:${MAJOR}
        docker push registry.gitlab.com/artificialsocialintelligence/study3/metadata-msg:latest
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
    if [ ! -z "${APTIMADOCKERREGPW:-}" ] ; then
        docker login gitlab.asist.aptima.com:5050 --username=dhoward --password=${APTIMADOCKERREGPW}
        docker tag metadata-web:${BUILD} registry.gitlab.com/artificialsocialintelligence/study3/metadata-web:${BUILD}
        docker tag metadata-web:${BUILD} registry.gitlab.com/artificialsocialintelligence/study3/metadata-web:${MINOR}
        docker tag metadata-web:${BUILD} registry.gitlab.com/artificialsocialintelligence/study3/metadata-web:${MAJOR}
        docker tag metadata-web:${BUILD} registry.gitlab.com/artificialsocialintelligence/study3/metadata-web:latest
        docker push registry.gitlab.com/artificialsocialintelligence/study3/metadata-web:${BUILD}
        docker push registry.gitlab.com/artificialsocialintelligence/study3/metadata-web:${MINOR}
        docker push registry.gitlab.com/artificialsocialintelligence/study3/metadata-web:${MAJOR}
        docker push registry.gitlab.com/artificialsocialintelligence/study3/metadata-web:latest
    fi
popd

#echo "Building/updating Doll/MIT Rita Agent"
#pushd "$root_dir"/Agents/Rita_Agent
#    source ./.env
#    docker-compose pull
#    if [[ $? -ne 0 ]]; then
#        echo "Failed to pull Rita_Agent, exiting now."
#        exit 1
#    fi
#popd


echo "Building/updating CMU-TA1 ATLAS Agent"
pushd "$root_dir"/Agents/ASI_CMU_TA1_ATLAS
    source ./settings.env
    docker build -t ${DOCKER_IMAGE_NAME_LOWERCASE} --build-arg CACHE_BREAKER=$(date +%s) .
    if [[ $? -ne 0 ]]; then
        echo "Failed to build asi_cmu_ta1_atlas container, exiting now."
        exit 1
    fi
    if [ ! -z "${APTIMADOCKERREGPW:-}" ] ; then
        docker login gitlab.asist.aptima.com:5050 --username=dhoward --password=${APTIMADOCKERREGPW}
        docker tag ${DOCKER_IMAGE_NAME_LOWERCASE} registry.gitlab.com/artificialsocialintelligence/study3/${DOCKER_IMAGE_NAME_LOWERCASE}:${BUILD}
        docker tag ${DOCKER_IMAGE_NAME_LOWERCASE} registry.gitlab.com/artificialsocialintelligence/study3/${DOCKER_IMAGE_NAME_LOWERCASE}:${MINOR}
        docker tag ${DOCKER_IMAGE_NAME_LOWERCASE} registry.gitlab.com/artificialsocialintelligence/study3/${DOCKER_IMAGE_NAME_LOWERCASE}:${MAJOR}
        docker tag ${DOCKER_IMAGE_NAME_LOWERCASE} registry.gitlab.com/artificialsocialintelligence/study3/${DOCKER_IMAGE_NAME_LOWERCASE}:latest
        docker push registry.gitlab.com/artificialsocialintelligence/study3/${DOCKER_IMAGE_NAME_LOWERCASE}:${BUILD}
        docker push registry.gitlab.com/artificialsocialintelligence/study3/${DOCKER_IMAGE_NAME_LOWERCASE}:${MINOR}
        docker push registry.gitlab.com/artificialsocialintelligence/study3/${DOCKER_IMAGE_NAME_LOWERCASE}:${MAJOR}
        docker push registry.gitlab.com/artificialsocialintelligence/study3/${DOCKER_IMAGE_NAME_LOWERCASE}:latest
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
