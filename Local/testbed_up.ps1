docker network create asist_net

#@echo off
echo Bring up Mosquitto Broker
pushd ..\mqtt
docker-compose up -d 
sleep 5

#echo off
echo Bring up ELK
pushd ..\ELK-Container
set MQTT_HOST=mosquitto
docker-compose up -d --build
sleep 5

popd
echo Bring up metadata server
pushd ..\metadata\metadata-docker
docker-compose up --build -d
popd

echo Bring up Import/Export dashboard
pushd ..\metadata\metadata-web
docker-compose up --build -d
popd

pushd ..\Agents\AC_IHMC_TA2_Location-Monitor
echo Bring up AC_IHMC_TA2_Location-Monitor Agent
docker-compose up --env-file settings.env -d
popd

pushd ..\Agents\AC_IHMC_TA2_Player-Proximity
echo Bring up AC_IHMC_TA2_Player-Proximity Agent
docker-compose up --env-file settings.env -d
popd

pushd ..\Agents\AC_IHMC_TA2_Dyad-Reporting
echo Bring up AC_IHMC_TA2_Dyad-Reporting Agent
docker-compose up --env-file settings.env -d
popd

pushd ..\Agents\AC_IHMC_TA2_Joint-Activity-Interdependence
echo Bring up AC_IHMC_TA2_Joint-Activity-Interdependence AC Agent
docker-compose up --env-file settings.env -d
popd

pushd ..\Agents\AC_CMUFMS_TA2_Cognitive
echo Bring up AC_CMUFMS_TA2_Cognitive AC Agent
docker-compose up --env-file settings.env -d
popd

pushd ..\Agents\AC_CMU_TA1_PyGLFoVAgent
echo Bring up AC_CMU_TA1_PyGLFoV Agent 
docker-compose up --env-file settings.env -d
popd

echo Bringing up the SIFT Asistant Agent
pushd ..\Agents\SIFT_Asistant_Agent
popd

pushd ..\Agents\AC_CMU_TA2_TED
echo Bringing up CMU TA2 Team Effectiveness Diagnostic AC Agent
docker-compose up --env-file settings.env -d
popd

pushd ..\Agents\AC_CMU_TA2_BEARD
echo Bringing up CMU TA2 BEARD AC Agent
docker-compose up --env-file settings.env -d
popd

pushd ..\Agents\ASI_CMU_TA1_ATLAS
echo Bring up CMU-TA1 ATLAS Agent 
docker-compose up --env-file settings.env -d
popd

pushd ..\Agents\ac_cornell_ta2_teamtrust
echo Bringing up Cornell Team Trust AC
docker-compose up --env-file settings.env -d
popd

pushd ..\Agents\gallup_agent_gelp
echo Bringing up Gallup Agent GELP
docker-compose up --env-file settings.env -d
popd

pushd ..\Agents\gallup_agent_gold
echo Bringing up Gallup Agent GOLD
docker-compose up --env-file settings.env -d
popd

echo Bring up Minecraft
pushd ..\Local
docker-compose -f docker-compose.asistmod.yml up 
popd
docker ps
