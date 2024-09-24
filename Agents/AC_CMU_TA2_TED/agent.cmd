@echo off
:: load in the settings.env variables
for /f "delims== tokens=1,2" %%G in (settings.env) do set %%G=%%H

::echo Parm1 - %1
::echo DOCKER_IMAGE_NAME_LOWERCASE - %DOCKER_IMAGE_NAME_LOWERCASE%
::echo DOCKER_CONTAINER_NAME - %DOCKER_CONTAINER_NAME%
::echo AGENT_NAME - %AGENT_NAME%
::echo AGENT_MAIN_RUN_FILE - %AGENT_MAIN_RUN_FILE%

IF "%1"=="up" (
  echo "Bring up Agent: %AGENT_NAME%"
  docker-compose --env-file settings.env up
  docker ps
  exit /B
)

IF "%1"=="upd" (
  echo "Bring up Agent: %AGENT_NAME%"
  docker-compose --env-file settings.env up -d
  docker ps
  exit /B
)

IF "%1"=="down" (
  echo "Bring down Agent: %AGENT_NAME%"
  docker-compose --env-file settings.env down --remove-orphans
  docker ps
  exit /B
)

IF "%1"=="build" (
  echo "updating the Reference agent image for %AGENT_NAME%"
  docker build -t %DOCKER_IMAGE_NAME_LOWERCASE% .
  exit /B
)

IF "%1"=="export" (
  echo "exporting the docker image for %AGENT_NAME%"
  docker save -o %DOCKER_IMAGE_NAME_LOWERCASE%.tar %DOCKER_IMAGE_NAME_LOWERCASE%
  exit /B
)

echo "Usage: agent.cmd [up|upd|down|build|export]"