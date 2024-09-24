@echo on
:: This script builds the entire testbed and all of the available agents
:: this script is run in a Windows PowerShell environment
:: Usage: ./testbed_build.cmd

:: First get the root directory for where this script is being run
set root_dir = %~dp0
echo %root_dir%

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


echo "updating MalmoControl container"
pushd ..\MalmoControl
docker build -t malmocontrol --build-arg CACHE_BREAKER=foo .
popd


REM echo "Update the test agent container"
REM pushd ..\ReferenceAgents\TestAgent
REM docker build -t test_agent --build-arg CACHE_BREAKER=foo .
REM popd

echo "Update the client map"
pushd ..\ClientMapSystem
docker build -t client_map --build-arg CACHE_BREAKER=foo .
popd

echo "updating AC_Aptima_TA3_measures"
pushd ..\Agents\AC_Aptima_TA3_measures
for /f "delims== tokens=1,2" %%G in (settings.env) do set %%G=%%H
xcopy /EI ..\..\Tools\ihmc-python-agent-helper-package ihmc-python-agent-helper-package
docker build -t %DOCKER_IMAGE_NAME_LOWERCASE% --build-arg CACHE_BREAKER=%random% .
del /S /Q ihmc-python-agent-helper-package
rmdir /S /Q ihmc-python-agent-helper-package
popd

echo "updating Gallup Agent GELP"
pushd ..\Agents\gallup_agent_gelp
for /f "delims== tokens=1,2" %%G in (settings.env) do set %%G=%%H
xcopy /EI ..\..\Tools\ihmc-python-agent-helper-package ihmc-python-agent-helper-package
docker build -t %DOCKER_IMAGE_NAME_LOWERCASE% --build-arg CACHE_BREAKER=%random% .
del /S /Q ihmc-python-agent-helper-package
rmdir /S /Q ihmc-python-agent-helper-package
popd

echo "updating Gallup Agent GOLD"
pushd ..\Agents\gallup_agent_gold
for /f "delims== tokens=1,2" %%G in (settings.env) do set %%G=%%H
xcopy /EI ..\..\Tools\ihmc-python-agent-helper-package ihmc-python-agent-helper-package
docker build -t %DOCKER_IMAGE_NAME_LOWERCASE% --build-arg CACHE_BREAKER=%random% .
del /S /Q ihmc-python-agent-helper-package
rmdir /S /Q ihmc-python-agent-helper-package
popd

echo "updating AC_IHMC_TA2_Location-Monitor"
pushd ..\Agents\AC_IHMC_TA2_Location-Monitor
for /f "delims== tokens=1,2" %%G in (settings.env) do set %%G=%%H
xcopy /EI ..\..\Tools\ihmc-python-agent-helper-package ihmc-python-agent-helper-package
docker build -t %DOCKER_IMAGE_NAME_LOWERCASE% --build-arg CACHE_BREAKER=%random% .
del /S /Q ihmc-python-agent-helper-package
rmdir /S /Q ihmc-python-agent-helper-package
popd

echo "updating AC_IHMC_TA2 Dyad-Reporting and Player-Proximity Agents"
pushd ..\Agents\AC_IHMC_TA2_Player-Proximity
for /f "delims== tokens=1,2" %%G in (settings.env) do set %%G=%%H
xcopy /EI ..\..\Tools\ihmc-python-agent-helper-package ihmc-python-agent-helper-package
docker build -t %DOCKER_IMAGE_NAME_LOWERCASE% --build-arg CACHE_BREAKER=%random% .
del /S /Q ihmc-python-agent-helper-package
rmdir /S /Q ihmc-python-agent-helper-package
popd
pushd ..\Agents\AC_IHMC_TA2_Dyad-Reporting
for /f "delims== tokens=1,2" %%G in (settings.env) do set %%G=%%H
xcopy /EI ..\..\Tools\ihmc-python-agent-helper-package ihmc-python-agent-helper-package
docker build -t %DOCKER_IMAGE_NAME_LOWERCASE% --build-arg CACHE_BREAKER=%random% .
del /S /Q ihmc-python-agent-helper-package
rmdir /S /Q ihmc-python-agent-helper-package
popd

echo "updating AC_IHMC_TA2_Joint-Activity-Interdependence"
pushd ..\Agents\AC_IHMC_TA2_Joint-Activity-Interdependence
for /f "delims== tokens=1,2" %%G in (settings.env) do set %%G=%%H
xcopy /EI ..\..\Tools\ihmc-python-agent-helper-package ihmc-python-agent-helper-package
xcopy /EI ..\AC_CMU_TA1_PyGLFoVAgent\ConfigFolder\maps .\maps
docker build -t %DOCKER_IMAGE_NAME_LOWERCASE% --build-arg CACHE_BREAKER=%random% .
del /S /Q ihmc-python-agent-helper-package
rmdir /S /Q ihmc-python-agent-helper-package
del /S /Q maps
rmdir /S /Q maps
popd

echo "updating AC_CMUFMS_TA2_Cognitive"
pushd ..\Agents\AC_CMUFMS_TA2_Cognitive
for /f "delims== tokens=1,2" %%G in (settings.env) do set %%G=%%H
xcopy /EI ..\..\Tools\ihmc-python-agent-helper-package ihmc-python-agent-helper-package
docker build -t %DOCKER_IMAGE_NAME_LOWERCASE% --build-arg CACHE_BREAKER=%random% .
del /S /Q ihmc-python-agent-helper-package
rmdir /S /Q ihmc-python-agent-helper-package
popd

echo "updating CMU TA2 Team Effectiveness Diagnostic"
pushd ..\Agents\AC_CMU_TA2_TED
for /f "delims== tokens=1,2" %%G in (settings.env) do set %%G=%%H
xcopy /EI ..\..\Tools\ihmc-python-agent-helper-package ihmc-python-agent-helper-package
docker build -t %DOCKER_IMAGE_NAME_LOWERCASE% --build-arg CACHE_BREAKER=foo .
del /S /Q ihmc-python-agent-helper-package
rmdir /S /Q ihmc-python-agent-helper-package
popd

echo "updating CMU TA2 BEARD AC"
pushd ..\Agents\AC_CMU_TA2_BEARD
for /f "delims== tokens=1,2" %%G in (settings.env) do set %%G=%%H
xcopy /EI ..\..\Tools\ihmc-python-agent-helper-package ihmc-python-agent-helper-package
docker build -t %DOCKER_IMAGE_NAME_LOWERCASE% --build-arg CACHE_BREAKER=foo .
del /S /Q ihmc-python-agent-helper-package
rmdir /S /Q ihmc-python-agent-helper-package
popdv

echo "updating AC_CMU_TA1_PyGLFoV Agent"
pushd ..\Agents\AC_CMU_TA1_PyGLFoVAgent
for /f "delims== tokens=1,2" %%G in (settings.env) do set %%G=%%H
docker build -t %DOCKER_IMAGE_NAME_LOWERCASE% --build-arg CACHE_BREAKER=%time% .
popd

echo "updating Rutgers Utility AC"
pushd ..\Agents\RutgersUtilityAC
for /f "delims== tokens=1,2" %%G in (settings.env) do set %%G=%%H
xcopy /EI ..\..\Tools\ihmc-python-agent-helper-package ihmc-python-agent-helper-package
docker build -t %DOCKER_IMAGE_NAME_LOWERCASE% --build-arg CACHE_BREAKER=%random% .
del /S /Q ihmc-python-agent-helper-package
rmdir /S /Q ihmc-python-agent-helper-package
popd

echo "updating the MQTT Message Validator container"
pushd ..\MQTTValidationServiceContainer
docker build  -t mqttvalidationservice:latest --build-arg CACHE_BREAKER=foo .
popd

echo "updating the ASIST Data Ingester container"
pushd ..\AsistDataIngesterContainer
docker build  -t asistdataingester:latest --build-arg CACHE_BREAKER=foo .
popd

echo "Building/updating the Logstash container"
pushd ..\ELK-Container/context/logstash
docker build -t logstash .
popd

echo "Building/updating the Postgres container"
pushd ..\metadata\metadata-docker
docker build -t postgres -f context\postgres\Dockerfile .
popd

echo "Building/updating the metadata-app container"
pushd ..\metadata\metadata-docker
docker build -t metadata-app -f context\metadata-app\Dockerfile .
popd

echo "Building/updating the metadata-msg container"
pushd ..\metadata\metadata-docker
docker build -t metadata-msg -f context\metadata-msg\Dockerfile .
popd

echo "Building/updating the metadata-web container"
pushd ..\metadata\metadata-web
docker build -t metadata-web .
popd
REM echo "updating Doll/MIT Rita Agent"
REM pushd ..\Agents\Rita_Agent
REM docker-compose pull
REM popd

echo "Building/updating CMU-TA1 ATLAS agent"
pushd ..\Agents\ASI_CMU_TA1_ATLAS
for /f "delims== tokens=1,2" %%G in (settings.env) do set %%G=%%H
docker build -t %DOCKER_IMAGE_NAME_LOWERCASE% --build-arg CACHE_BREAKER=%time% .
popd

echo "updating SIFT Asistant Agent"
pushd ..\Agents\SIFT_Asistant_Agent
docker-compose pull
popd

echo "Building/updating Atomic agent"
pushd ..\Agents\atomic_agent
for /f "delims== tokens=1,2" %%G in (settings.env) do set %%G=%%H
:: xcopy /EI ..\..\Tools\ihmc-python-agent-helper-package ihmc-python-agent-helper-package
:: docker build -t %DOCKER_IMAGE_NAME_LOWERCASE% --build-arg CACHE_BREAKER=%random% .
:: del /S /Q ihmc-python-agent-helper-package
:: rmdir /S /Q ihmc-python-agent-helper-package
docker-compose --env-file settings.env pull
popd

echo "updating Cornell Team Trust AC"
pushd ..\Agents\ac_cornell_ta2_teamtrust
docker-compose pull
popd

echo "List the Docker containers"
docker ps
