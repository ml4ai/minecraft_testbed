#!/usr/bin/env bash

docker run --rm -u $(id -u ${USER}):$(id -g ${USER}) \
       -e "asist_testbed=/testbed" \
       -v $PWD:/work \
       -v$asist_testbed:/testbed asist_base_map \
       /work/make_asist_base_map.sh $@
