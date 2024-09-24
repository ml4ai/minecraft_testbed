# MalmoControl

## Introduction

This docker container is the main control system for running experiments. It is composed of an ASP.NetCore backend with API endpoints and a preliminary Front End control system for basic experiment controls.

## Building Docker container
- Navigate to the root (top level) of the MalmoControl directory, this is the same level that the dockerfile appears in
- Open a shell window and run *docker build -t malmocontrol .*

## Updating Docker Container After a New Release --> Building From Source
- Navigate to the root (top level) of the MalmoControl directory, this is the same level that the dockerfile appears in
- Open a shell window in this directory and run *docker build -t malmocontrol --build-arg CACHE_BREAKER=somestring .*
- You can replace the word "somestring" with any string of your choice, as long as it is unique each time
- This build is significantly faster, as the majority of the image layers are already built

## Updating Docker Container After a New Release --> Pulling New Image 
- Open a shell window and run docker login --username foo --password bar. Replace foo and bar with your username and password.
- Then run docker pull gcr.io/asist-2130/malmocontrol
- This should update your current malmocontrol image, correctly altering only the image layers that have changed

## Configuration
- You must configure the MQTT Host before using the container. This can be done in the Local/MalmoControl/appsettings.json file. In the field labeled "Mqtt"-->"Host", enter the IP address of the machine running the ELk Stack in quotes. Additionally, in the *Mod*-->*name* field, enter either "malmo" or "asist".

NOTE: The appsetting.json configuration will NOT update after this container has started. If you wish to change a configuration value in appsettings.json, you will need to bring the MCRVM stack down and then back up with docker-compose.

## Accessing the Front End GUI

- navigate to *https://"the-machine-ip-or-domain":9000/MalmoControl*
- here you will find various utilities that will assist you in running and monitoring an experiment.
- for more detailed instruction on how to use these utilites, click on the "Help" icon in GUI title-bar

## Tailing the log of the Docker container
- docker attach malmocontrol_Local 

## Connecting a shell to Docker container
- Works better on Windows from a Powershell window (in VS Code)
- docker exec -it malmocontrol_Local /bin/bash


