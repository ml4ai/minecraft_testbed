@echo off



echo Get testbed version number

set "rev_tag=1.0.4.2"
rem echo %rev_tag%
echo %rev_tag% > version.txt

REM this part of the script edits a file to set the version number
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

echo Copying over Minecraft data volume
xcopy .\data .\MinecraftServer\data /E/H/I

echo Bring up Minecraft
pushd ..\Local
::docker network create malmonet
docker-compose -f docker-compose.asistmod.yml up
popd
docker ps
