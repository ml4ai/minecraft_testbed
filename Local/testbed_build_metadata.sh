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

# echo "Building/updating the metadata-msg container"
# pushd "$root_dir"/metadata/metadata-docker
#     if [ ! $BUILD == "latest" ]
#     then
#         sed -i "s/TESTBED_VERSION=NOT SET/TESTBED_VERSION=${BUILD}/" metadata/metadata-docker/metadata-app.env
#     fi
#     docker build  -t metadata-msg:${BUILD} -f context/metadata-msg/Dockerfile .
#     if [[ $? -ne 0 ]]; then
#         echo "Failed to build metadata-msg container, exiting now."
#         exit 1
#     fi
#     if [ ! -z "${APTIMADOCKERREGPW:-}" ] ; then
#         docker login gitlab.asist.aptima.com:5050 --username=dhoward --password=${APTIMADOCKERREGPW}
#         docker tag metadata-msg:${BUILD} registry.gitlab.com/artificialsocialintelligence/study3/metadata-msg:${BUILD}
#         docker tag metadata-msg:${BUILD} registry.gitlab.com/artificialsocialintelligence/study3/metadata-msg:${MINOR}
#         docker tag metadata-msg:${BUILD} registry.gitlab.com/artificialsocialintelligence/study3/metadata-msg:${MAJOR}
#         docker tag metadata-msg:${BUILD} registry.gitlab.com/artificialsocialintelligence/study3/metadata-msg:latest
#         docker push registry.gitlab.com/artificialsocialintelligence/study3/metadata-msg:${BUILD}
#         docker push registry.gitlab.com/artificialsocialintelligence/study3/metadata-msg:${MINOR}
#         docker push registry.gitlab.com/artificialsocialintelligence/study3/metadata-msg:${MAJOR}
#         docker push registry.gitlab.com/artificialsocialintelligence/study3/metadata-msg:latest
#     fi
# popd

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

exit 0
