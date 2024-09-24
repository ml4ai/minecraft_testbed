@echo off
set "remove_all_containers=true"


echo Bring down MQTT
pushd ..\mqtt
docker-compose down --remove-orphans
popd

echo Bring down ELK
pushd ..\ELK-Container
docker-compose down --remove-orphans
popd

echo Bring down metadata server
pushd ..\metadata\metadata-docker
docker-compose down --remove-orphans
popd

echo Bring down Import/Export dashboard
pushd ..\metadata\metadata-web
docker-compose down --remove-orphans
popd

echo Bring down Minecraft
pushd ..\Local
docker-compose -f docker-compose.asistmod.yml down --remove-orphans
popd

echo Deleting Minecraft data volume
rmdir .\MinecraftServer\data /S /Q

if "%remove_all_containers%"=="true" GOTO DONT_REMOVE_CONTAINERS
echo Stop the rest of the containers
for /f "tokens=*" %%c in ('docker container ls -q') do docker container stop %%c
:DONT_REMOVE_CONTAINERS

docker ps
