@echo off

REM ----------

REM get any arguments to the main script and optionally start up containers
REM set "test_agent_up=false"
set "fov_agent_up=true"
set "measures_agent_up=true"
set "location_agent_up=true"
set "proximity_agent_up=true"
set "joint_activity_interdependence_agent_up=true"
set "cmufms_cognitive_load_agent_up=true"
set "asr_agent_up=true"
set "dialog_agent_up=true"
set "tmm_agent_up=true"
set "gallup_agent_gelp_up=true"
set "gallup_agent_gold_up=true"
set "rita_agent_up=true"
set "cmuta2_ted_agent_up=true"
set "cmuta2_beard_agent_up=true"
set "utility_agent_up=true"
set "sift_agent_agent_up=true"
set "atomic_agent_up=true"
set "cmu_ta1_agent=true"
set "cra_psicoach_agent_up=true"
set "cornell_team_trust_agent_up=true"

if NOT "%1"=="h" GOTO NO_HELP
	echo @on
	echo "Default is to start all agents.  To not start agents add the letter(s) to command line"
	echo " l - AC_IHMC_TA2_Location-Monitor"
	echo " f - FoV AC"
	echo " m - Measures AC"
	echo " a - UAZ SpeechAnalyzer AC"
	echo " d - UAZ Dialog AC"
	echo " t - UAZ TMM agent"
	echo " g - Gallup Agent GELP"
	echo " n - Gallup Agent GOLD"
	echo " p - AC_IHMC_TA2 Dyad-Reporting and Player-Proximity"
	echo " j - AC_IHMC_TA2 Joint Activity Interdependence"
	echo " k - CMUFMS Cognitive Load AC"
	echo " r - DOLL Rita Agent"
	echo " s - SIFT Asistant Agent"
    echo " x - atomic agent"
::	echo " x - atomic agent"
  	echo " u - Rutgers Utility agent"
	echo " e - CMU TA2 Team Effectiveness Diagnostic AC"
	echo " v - CMU TA2 BEARD AC"
	echo " c - CMU-TA1 ATLAS Agent"
	echo " o - CRA PSI-Coach Agent"
	echo " b - Cornell  Team Trust AC"
	echo @off
	exit /b
:NO_HELP

:CMD_LOOP
IF "%1"=="" GOTO CMD_CONTINUE
	if "%1"=="f" set "fov_agent_up=false"
	if "%1"=="m" set "measures_agent_up=false"
	if "%1"=="l" set "location_agent_up=false"
	if "%1"=="p" set "proximity_agent_up=false"
	if "%1"=="j" set "joint_activity_interdependence_agent_up=false"
	if "%1"=="k" set "cmufms_cognitive_load_agent_up=false"
	if "%1"=="a" set "asr_agent_up=false"
	if "%1"=="d" set "dialog_agent_up=false"
	if "%1"=="t" set "tmm_agent_up=false"
	if "%1"=="g" set "gallup_agent_gelp_up=false"
	if "%1"=="n" set "gallup_agent_gold_up=false"
	if "%1"=="r" set "rita_agent_up=false"
 	if "%1"=="u" set "utility_agent_up=false"
 	if "%1"=="s" set "sift_agent_agent_up=false"
::	if "%1"=="x" set "atomic_agent_up=false"
	if "%1"=="e" set "cmuta2_ted_agent_up=false"
	if "%1"=="v" set "cmuta2_beard_agent_up=false"
	if "%1"=="c" set "cmu_ta1_agent=false"
	if "%1"=="o" set "cra_psicoach_agent_up=false"
	if "%1"=="b" set "cornell_team_trust_agent_up=false"
SHIFT
GOTO CMD_LOOP
:CMD_CONTINUE

echo "Agent startup status:"
echo "AC_IHMC_TA2_Location-Monitor: %location_agent_up%"
echo "AC_IHMC_TA2 Dyad-Reporting and Player-Proximity: %proximity_agent_up%"
echo "AC_IHMC_TA2_Joint-Activity-Interdependence: %joint_activity_interdependence_agent_up%"
echo "AC_CMUFMS_TA2_Cognitive: %cmufms_cognitive_load_agent_up%"
echo "FoV Agent: %fov_agent_up%"
echo "AC_Aptima_TA3_measures: %measures_agent_up%"
echo "ASR agent: %asr_agent_up%"
echo "Dialog agent: %dialog_agent_up%"
echo "TMM agent: %tmm_agent_up%"
echo "Gallup Agent GELP: %gallup_agent_gelp_up%"
echo "Gallup Agent GOLD: %gallup_agent_gold_up%"
echo "Rita agent: %rita_agent_up%"
echo "CMU TA2 Process Dignostic AC Agent: %cmuta2_ted_agent_up%"
echo "CMU TA2 BEARD AC Agent: %cmuta2_beard_agent_up%"
echo "Utility agent: %utility_agent_up%"
echo "SIFT Asistant agent: %sift_agent_agent_up%"
echo "atomic agent: %atomic_agent_up%"
echo "CMU-TA1 ATLAS Agent: %cmu_ta1_agent%"
echo "CRA PSI-Coach agent: %cra_psicoach_agent_up%"
echo "Cornell Team Trust AC: %cornell_team_trust_agent_up%"


echo Get testbed version number
pushd ..
docker run --rm -v "%cd%:/repo" gittools/gitversion:5.7.1-alpine.3.12-x64-5.0 /repo /nocache /showvariable FullSemVer > Local\versionSemVer.txt
docker run --rm -v "%cd%:/repo" gittools/gitversion:5.7.1-alpine.3.12-x64-5.0 /repo /nocache /showvariable ShortSha > Local\versionSHA.txt
popd
set /p versemver=<versionSemVer.txt
set /p vershaver=<versionSHA.txt
del versionSemVer.txt
del versionSHA.txt
set "rev_tag=%versemver%-%vershaver%"
rem echo %rev_tag%
echo %rev_tag% > version.txt

REM this part of the scrip edits a file to set the version number
setlocal EnableDelayedExpansion
set "newver=%rev_tag%"
set "searchfor=system_version"
set "replaceStr="system_version^": ^"%newver%^","
REM echo %replaceStr%
del %temp%\testing_Output.txt

Set "file=MalmoControl\appsettings.Production.json"
(for /f "delims=" %%s in ('Type %file%') do (
     set "sline=%%s"
     echo !sline! | find /I "%searchfor%" && set "sline=!replaceStr!"
    echo !sline! >>%temp%\testing_Output.txt
	)
)
Copy /Y %temp%\testing_Output.txt %file%
del %temp%\testing_Output.txt

set "searchfor=TESTBED_VERSION"
set "replaceStr=TESTBED_VERSION=%newver%"
set "file=..\metadata\metadata-web\metadata-web.env
(for /f "delims=" %%s in ('Type %file%') do (
     set "sline=%%s"
     echo !sline! | find /I "%searchfor%" && set "sline=!replaceStr!"
    echo !sline! >>%temp%\testing_Output.txt
	)
)
Copy /Y %temp%\testing_Output.txt %file%
del %temp%\testing_Output.txt
set "file=..\metadata\metadata-docker\metadata-app.env
(for /f "delims=" %%s in ('Type %file%') do (
     set "sline=%%s"
     echo !sline! | find /I "%searchfor%" && set "sline=!replaceStr!"
    echo !sline! >>%temp%\testing_Output.txt
	)
)
Copy /Y %temp%\testing_Output.txt %file%
del %temp%\testing_Output.txt

echo "Create the asist network"
docker network create asist_net

echo Bring up MQTT
pushd ..\mqtt
docker-compose up -d
sleep 5
popd

echo Bring up ELK
pushd ..\ELK-Container
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

if "%measures_agent_up%"=="false" GOTO NO_MEASURES_AGENT
pushd ..\Agents\AC_Aptima_TA3_measures
echo Bring up Measures
docker-compose --env-file settings.env up -d
popd
:NO_MEASURES_AGENT

if "%location_agent_up%"=="false" GOTO NO_LOCATION_AGENT
pushd ..\Agents\AC_IHMC_TA2_Location-Monitor
echo Bring up AC_IHMC_TA2_Location-Monitor Agent
docker-compose --env-file settings.env up -d
popd
:NO_LOCATION_AGENT

if "%proximity_agent_up%"=="false" GOTO NO_PROXIMITY_AC_AGENT
echo Bring up AC_IHMC_TA2 Dyad-Reporting and Player-Proximity Agents
pushd ..\Agents\AC_IHMC_TA2_Player-Proximity
docker-compose --env-file settings.env up -d
popd
pushd ..\Agents\AC_IHMC_TA2_Dyad-Reporting
docker-compose --env-file settings.env up -d
popd
:NO_PROXIMITY_AC_AGENT

if "%joint_activity_interdependence_agent_up%"=="false" GOTO NO_JOINT_ACTIVITY_INTERDEPENDENCE_AC_AGENT
pushd ..\Agents\AC_IHMC_TA2_Joint-Activity-Interdependence
echo Bring up AC_IHMC_TA2_Joint-Activity-Interdependence AC Agent
docker-compose --env-file settings.env up -d
popd
:NO_JOINT_ACTIVITY_INTERDEPENDENCE_AC_AGENT

if "%cmufms_cognitive_load_agent_up%"=="false" GOTO NO_CMUFMS_COGNITIVE_LOAD_AC_AGENT
echo Bring up the CMUFMS Cognitive Load AC Agent
pushd ..\Agents\AC_CMUFMS_TA2_Cognitive
docker-compose --env-file settings.env up -d
popd
:NO_CMUFMS_COGNITIVE_LOAD_AC_AGENT

if "%fov_agent_up%"=="false" GOTO NO_FOV_AGENT
pushd ..\Agents\AC_CMU_TA1_PyGLFoVAgent
echo Bring up AC_CMU_TA1_PyGLFoV Agent
docker-compose --env-file settings.env up -d
popd
:NO_FOV_AGENT

if "%asr_agent_up%"=="false" GOTO NO_ASR_AGENT
pushd ..\Agents\AC_UAZ_TA1_ToMCAT-SpeechAnalyzer
echo Bringing up Speech Analyzer
docker-compose -f google.yml  up -d
popd
:NO_ASR_AGENT

if "%dialog_agent_up%"=="false" GOTO NO_DIALOG_AGENT
pushd ..\Agents\uaz_dialog_agent
echo Bringing up Dialog Agent
SET TDAC_HOSTNAME=host.docker.internal
docker-compose up -d
popd
:NO_DIALOG_AGENT

if "%cra_psicoach_agent_up%"=="false" GOTO NO_PSICOACH_AGENT
pushd ..\Agents\ASI_CRA_TA1_psicoach
echo Bring up CRA PSI-Coach Agent
docker-compose up -d
popd
:NO_PSICOACH_AGENT

if "%tmm_agent_up%"=="false" GOTO NO_TMM_AGENT
pushd ..\Agents\ASI_UAZ_TA1_ToMCAT
echo Bringing up TMM Agent
docker-compose up -d
popd
:NO_TMM_AGENT

if "%gallup_agent_gelp_up%"=="false" GOTO NO_GALLUP_GELP_AGENT
pushd ..\Agents\gallup_agent_gelp
echo Bringing up Gallup Agent GELP
docker-compose --env-file settings.env up -d
popd
:NO_GALLUP_GELP_AGENT

if "%gallup_agent_gold_up%"=="false" GOTO NO_GALLUP_GOLD_AGENT
pushd ..\Agents\gallup_agent_gold
echo Bringing up Gallup Agent GOLD
docker-compose --env-file settings.env up -d
popd
:NO_GALLUP_GOLD_AGENT

if "%cmuta2_ted_agent_up%"=="false" GOTO NO_CMUTA2_TED_AGENT
pushd ..\Agents\AC_CMU_TA2_TED
echo Bringing up CMU TA2 Team Effectiveness Diagnostic AC Agent
docker-compose --env-file settings.env up -d
popd
:NO_CMUTA2_TED_AGENT

if "%cmuta2_beard_agent_up%"=="false" GOTO NO_CMUTA2_BEARD_AGENT
pushd ..\Agents\AC_CMU_TA2_BEARD
echo Bringing up CMU TA2 BEARD AC Agent
docker-compose --env-file settings.env up -d
popd
:NO_CMUTA2_BEARD_AGENT

if "%rita_agent_up%"=="false" GOTO NO_RITA_AGENT
pushd ..\Agents\Rita_Agent
echo Bringing up Doll MIT Rita Agent
docker-compose --env-file .env up -d
popd
:NO_RITA_AGENT

if "%utility_agent_up%"=="false" GOTO NO_UTILITY_AGENT
echo Bring up Rutgers Utility AC
pushd ..\Agents\RutgersUtilityAC
docker-compose --env-file settings.env up -d
popd
:NO_UTILITY_AGENT


if "%sift_agent_agent_up%"=="false" GOTO NO_SIFT_ASISTANT_AGENT
echo Bring up SIFT Asistant Agent
pushd ..\Agents\SIFT_Asistant_Agent
docker-compose up -d
popd
:NO_SIFT_ASISTANT_AGENT

if "%atomic_agent_up%"=="false" GOTO NO_ATOMIC_AGENT
echo Bring up atomic agent
pushd ..\Agents\atomic_agent
docker-compose --env-file settings.env up -d
popd
:NO_ATOMIC_AGENT

if "%cmu_ta1_agent%"=="false" GOTO NO_CMU_TA1_AGENT
pushd ..\Agents\ASI_CMU_TA1_ATLAS
echo Bring up CMU-TA1 Intervention Agent
docker-compose --env-file settings.env up -d
popd
:NO_CMU_TA1_AGENT

if "%cornell_team_trust_agent_up%"=="false" GOTO NO_CORNELL_TEAM_TRUST_AC
pushd ..\Agents\ac_cornell_ta2_teamtrust
echo Bringing up Cornell Team Trust AC
docker-compose --env-file settings.env up -d
popd
:NO_CORNELL_TEAM_TRUST_AC

echo Copying over Minecraft data volume
xcopy .\data .\MinecraftServer\data /E/H/I

echo Bring up Minecraft
pushd ..\Local
docker-compose -f docker-compose.asistmod.yml up
popd
docker ps
