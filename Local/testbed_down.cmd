@echo off
set "remove_all_containers=true"

if NOT "%1"=="h" GOTO NO_HELP
	echo @on
	echo "To take down all containers"
	echo " c - do not take down any remaining containers"
	echo @off
	exit /b
:NO_HELP

:CMD_LOOP
IF "%1"=="" GOTO CMD_CONTINUE
	if "%1"=="c" set "remove_all_containers=false"
SHIFT
GOTO CMD_LOOP
:CMD_CONTINUE

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

echo Bring down Measures
pushd ..\Agents\AC_Aptima_TA3_measures
docker-compose --env-file settings.env down --remove-orphans
popd

echo Bring down Gallup Agent GELP
pushd ..\Agents\gallup_agent_gelp
docker-compose --env-file settings.env down --remove-orphans
popd

echo Bring down Gallup Agent GOLD
pushd ..\Agents\gallup_agent_gold
docker-compose --env-file settings.env down --remove-orphans
popd

pushd ..\Agents\AC_IHMC_TA2_Location-Monitor
echo Bring down AC_IHMC_TA2_Location-Monitor
docker-compose --env-file settings.env down --remove-orphans
popd

pushd ..\Agents\IHMCProximityAC
echo Bring down IHMC Proximity AC Agent
docker-compose --env-file settings.env down --remove-orphans
popd

pushd ..\Agents\IHMCDyadAC
echo Bring down IHMC Dyad AC Agent
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

pushd ..\Agents\ASI_CMU_TA1_ATLAS
echo Bring down CMU TA1 ATLAS Agent
docker-compose --env-file settings.env down --remove-orphans
popd

pushd ..\Agents\AC_CMU_TA1_PyGLFoVAgent
echo Bring down AC_CMU_TA1 PyGLFoV Agent
docker-compose down --remove-orphans
popd

pushd ..\Agents\AC_UAZ_TA1_ToMCAT-SpeechAnalyzer
echo Bring down speech Analyzer
bash export.sh
docker-compose -f google.yml down --volumes --remove-orphans
popd

pushd ..\Agents\uaz_dialog_agent
echo Bring down dialog agent
docker-compose down --remove-orphans
popd

pushd ..\Agents\ASI_UAZ_TA1_ToMCAT
echo Bring down tmm agent
docker-compose down --remove-orphans
popd

pushd ..\Agents\Rita_Agent
echo Bring down Doll/MIT Rita agent
docker-compose down --remove-orphans
popd

echo "Bring down the SIFT Asistant Agent"
pushd ..\Agents\SIFT_Asistant_Agent
docker-compose down --remove-orphans
popd

pushd ..\Agents\RutgersUtilityAC
echo Bring down Rutgers Utility AC
docker-compose --env-file settings.env down --remove-orphans
popd

pushd ..\Agents\ASI_CRA_TA1_psicoach
echo Bring down CRA PSI-Coach agent
docker-compose down --remove-orphans
popd

pushd ..\Agents\ac_cornell_ta2_teamtrust
echo Bring down Cornell Team Trust AC
docker-compose --env-file settings.env down --remove-orphans
popd

echo "Bring down the atomic agent"
pushd ..\Agents\atomic_agent
docker-compose --env-file settings.env down --remove-orphans
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
