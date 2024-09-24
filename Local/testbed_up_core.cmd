@echo off

REM ----------

REM get any arguments to the main script and optionally start up containers
REM the default on agents is now NOT to start them
REM Agent default settings
set "fov_agent_up=false"
set "location_agent_up=false"
set "proximity_agent_up=false"
set "joint_activity_interdependence_agent_up=false"
set "cmufms_cognitive_load_agent_up=false"
set "asr_agent_up=false"
set "speech_analyzer_up=false"
set "dialog_agent_up=false"
set "tmm_agent_up=false"
set "gallup_agent_gelp_up=false"
set "gallup_agent_gold_up=false"
set "rita_agent_up=false"
set "cmuta2_ted_agent_up=false"
set "cmuta2_beard_agent_up=false"
set "utility_agent_up=false"
set "sift_agent_agent_up=false"
set "atomic_agent_up=false"
set "cmu_ta1_agent=false"
set "cra_psicoach_agent_up=false"
set "cu_request_agent_up=false"
REM Core containers
set "testbed_core_up=false"
set "measures_agent_up=false"

if NOT "%1"=="h" GOTO NO_HELP
	echo @on
	echo "Default is to start no core components and no agents."
	echo "To start the core or agents add the letter(s) to the command line separated by space."
	echo " z - core testbed components"
	echo " l - location monitor agent"
	echo " f - FoV AC"
	echo " m - Measures AC"
	echo " a - UAZ ASR AC"
	echo " w - UAZ SpeechAnalyzer AC"
	echo " d - UAZ Dialog AC"
	echo " t - UAZ TMM agent"
	echo " g - Gallup Agent GELP"
	echo " n - Gallup Agent GOLD"
	echo " p - IHMC proximity AC"
	echo " j - IHMC Joint Activity Interdependence AC"
	echo " k - CMUFMS Cognitive Load AC"
	echo " r - DOLL Rita Agent"
	echo " s - SIFT Asistant Agent"
	echo " x - atomic agent"
	echo " u - Rutgers Utility agent"
	echo " e - CMU TA2 Team Effectiveness Diagnostic AC"
	echo " v - CMU TA2 BEARD AC"
	echo " c - CMU-TA1 ATLAS Agent"
	echo " o - CRA PSI-Coach Agent"
	echo " b - CU Request Tracker AC"
	echo @off
	exit /b
:NO_HELP

:CMD_LOOP
IF "%1"=="" GOTO CMD_CONTINUE
	if "%1"=="z" set "testbed_core_up=true"
	if "%1"=="f" set "fov_agent_up=true"
	if "%1"=="m" set "measures_agent_up=false"
	if "%1"=="l" set "location_agent_up=true"
	if "%1"=="p" set "proximity_agent_up=true"
	if "%1"=="j" set "joint_activity_interdependence_agent_up=true"
	if "%1"=="k" set "cmufms_cognitive_load_agent_up=true"
	if "%1"=="a" set "asr_agent_up=true"
	if "%1"=="w" set "speech_analyzer_up=true"
	if "%1"=="d" set "dialog_agent_up=true"
	if "%1"=="t" set "tmm_agent_up=true"
	if "%1"=="g" set "gallup_agent_gelp_up=true"
	if "%1"=="n" set "gallup_agent_gold_up=true"
	if "%1"=="r" set "rita_agent_up=true"
	if "%1"=="u" set "utility_agent_up=true"
	if "%1"=="s" set "sift_agent_agent_up=true"
	if "%1"=="x" set "atomic_agent_up=true"
	if "%1"=="e" set "cmuta2_ted_agent_up=true"
	if "%1"=="v" set "cmuta2_beard_agent_up=true"
	if "%1"=="c" set "cmu_ta1_agent=true"
	if "%1"=="o" set "cra_psicoach_agent_up=true"
	if "%1"=="b" set "cu_request_agent_up=true"
SHIFT
GOTO CMD_LOOP
:CMD_CONTINUE

echo "testbed core: %testbed_core_up%"
echo "Agent startup status:"
echo "Location Monitor Agent: %location_agent_up%"
echo "Proximity AC Agent: %proximity_agent_up%"
echo "Joint Activity Interdependence AC Agent: %joint_activity_interdependence_agent_up%"
echo "Cognitive Load AC Agent: %cmufms_cognitive_load_agent_up%"
echo "FoV Agent: %fov_agent_up%"
echo "Measures Agent: %measures_agent_up%"
echo "ASR agent: %asr_agent_up%"
echo "SpeechAnalyzer agent: %speech_analyzer_up%"
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
echo "CU Reuqest Tracker AC: %cu_request_agent_up%"


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

if "%testbed_core_up%"=="false" GOTO NO_TESTBED_CORE
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

:NO_TESTBED_CORE

if "%measures_agent_up%"=="false" GOTO NO_MEASURES_AGENT
pushd ..\Agents\AC_Aptima_TA3_measures
echo Bring up Measures
docker-compose --env-file settings.env up -d
popd
:NO_MEASURES_AGENT

if "%location_agent_up%"=="false" GOTO NO_LOCATION_AGENT
pushd ..\Agents\IHMCLocationMonitor
echo Bring up IHMC Location Monitor
docker-compose --env-file settings.env up -d
popd
:NO_LOCATION_AGENT

if "%proximity_agent_up%"=="false" GOTO NO_PROXIMITY_AC_AGENT
echo Bring up IHMC Proximity/Dyad AC Agents
pushd ..\Agents\IHMCProximityAC
docker-compose --env-file settings.env up -d
popd
pushd ..\Agents\IHMCDyadAC
docker-compose --env-file settings.env up -d
popd
:NO_PROXIMITY_AC_AGENT

if "%joint_activity_interdependence_agent_up%"=="false" GOTO NO_JOINT_ACTIVITY_INTERDEPENDENCE_AC_AGENT
echo Bring up IHMC Joint-Activity-Interdependence AC Agent
pushd ..\Agents\AC_IHMC_TA2_Joint-Activity-Interdependence
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
pushd ..\Agents\AC_UAZ_TA1_ASR_Agent
echo Bringing up ASR Agent
docker-compose -f google.yml up -d
popd
:NO_ASR_AGENT

if "%speech_analyzer_up%"=="false" GOTO NO_SPEECH_ANALYZER
pushd ..\Agents\AC_UAZ_TA1_SpeechAnalyzer
echo Bringing up Speech Analyzer
docker-compose up -d
popd
:NO_SPEECH_ANALYZER

if "%dialog_agent_up%"=="false" GOTO NO_DIALOG_AGENT
pushd ..\Agents\uaz_dialog_agent
echo Bringing up Dialog Agent
docker-compose up -d
popd
:NO_DIALOG_AGENT

if "%cra_psicoach_agent_up%"=="false" GOTO NO_PSICOACH_AGENT
pushd ..\Agents\PsiCoachAgent
echo Bring up CRA PSI-Coach Agent
docker-compose up -d
popd
:NO_PSICOACH_AGENT

if "%tmm_agent_up%"=="false" GOTO NO_TMM_AGENT
pushd ..\Agents\uaz_tmm_agent
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
echo Bring up CMU-TA1 ATLAS Agent
docker-compose --env-file settings.env up -d
popd
:NO_CMU_TA1_AGENT

if "%cra_psicoach_agent_up%"=="false" GOTO NO_PSICOACH_AGENT
pushd ..\Agents\PsiCoachAgent
echo Bring up CRA PSI-Coach Agent
docker-compose up -d
popd
:NO_PSICOACH_AGENT

if "%cu_request_agent_up%"=="false" GOTO NO_CU_REQUEST_TRACKER_AC
pushd ..\Agents\cu_request_ac
echo Bringing up CU Request Tracker AC
docker-compose --env-file settings.env up -d
popd
:NO_CU_REQUEST_TRACKER_AC

if "%testbed_core_up%"=="false" GOTO NO_TESTBED_CORE_2
echo Copying over Minecraft data volume
xcopy .\data .\MinecraftServer\data /E/H/I

echo Bring up Minecraft
pushd ..\Local
docker-compose -f docker-compose.asistmod.yml up
popd
:NO_TESTBED_CORE_2
docker ps
