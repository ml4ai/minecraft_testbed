#!/bin/bash

export AGENT_HELPER_VERSION=$(pip show asistagenthelper-pkg-rcarff-ihmc | grep Version | sed 's/Version: //')
source settings.env
export AGENT_NAME=$AGENT_NAME

python3 -m src.$AGENT_MAIN_RUN_FILE $1 $2