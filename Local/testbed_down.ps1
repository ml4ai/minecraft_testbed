#@echo off
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

pushd ..\Agents\AC_IHMC_TA2_Location-Monitor
echo Bring down AC_IHMC_TA2_Location-Monitor Agent
docker-compose --env-file settings.env down --remove-orphans
popd

pushd ..\Agents\AC_IHMC_TA2_Player-Proximity
echo Bring down AC_IHMC_TA2_Player-Proximity Agent
docker-compose --env-file settings.env down --remove-orphans
popd

pushd ..\Agents\AC_IHMC_TA2_Dyad-Reporting
echo Bring down AC_IHMC_TA2_Dyad-Reporting Agent
docker-compose --env-file settings.env down --remove-orphans
popd

pushd ..\Agents\AC_IHMC_TA2_Joint-Activity-Interdependence
echo Bring down AC_IHMC_TA2_Joint-Activity-Interdependence Agent
docker-compose --env-file settings.env down --remove-orphans
popd

pushd ..\Agents\AC_CMUFMS_TA2_Cognitive
echo Bring down CMUFMS Cognitive Load Agent
docker-compose --env-file settings.env down --remove-orphans
popd

pushd ..\Agents\AC_CMU_TA2_TED
echo Bring down CMU TA2 Team Effectiveness Diagnostic AC
docker-compose --env-file settings.env down --remove-orphans
popd

pushd ..\Agents\AC_CMU_TA2_BEARD
echo Bring down CMU TA2 BEARD AC
docker-compose --env-file settings.env down --remove-orphans
popd

pushd ..\Agents\AC_CMU_TA1_PyGLFoVAgent
echo Bring down AC_CMU_TA1_PyGLFoV Agent
docker-compose down --remove-orphans
popd

echo Bring down the SIFT Asistant Agent
pushd ..\Agents\SIFT_Asistant_Agent
docker-compose down --remove-orphans
popd

echo Bring down the CMU-TA1 ATLAS Agent
pushd ..\Agents\ASI_CMU_TA1_ATLAS
docker-compose --env-file settings.env down --remove-orphans
popd

pushd ..\Agents\ac_cornell_ta2_teamtrust
echo Bring down Cornell Team Trust AC
docker-compose --env-file settings.env down --remove-orphans
popd

pushd ..\Agents\gallup_agent_gelp
echo Bring down Gallup Agent GELP
docker-compose --env-file settings.env down --remove-orphans
popd

pushd ..\Agents\gallup_agent_gold
echo Bring down Gallup Agent GOLD
docker-compose --env-file settings.env down --remove-orphans
popd

echo Bring down Minecraft
pushd ..\Local
docker-compose -f docker-compose.asistmod.yml down --remove-orphans
popd

echo Bring down Mosquitto
pushd ..\mqtt
docker-compose down --remove-orphans
popd
#echo Stop the rest of the containers
#for /f "tokens=*" %%c in ('docker container ls -q') do docker container stop %%c
docker ps
