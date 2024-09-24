# MalmoContainer

## Introduction

This docker container launches an instance of Minecraft with Malmo connected to port 10000. Because this is a docker container, port 10000 will be mapped out during the experiment to a user selected port via the MalmoControl container.

It also includes a VNC server of the Minecraft window on the host exposed port of 5900. Connecting VNC Viewer to "localhost:5900" will show the Minecraft GUI and allow for fine-grained mission control via a Minecraft Agent.

## Building Docker container
- Navigate to the root (top level) of the MalmoContainer directory, this is the same level that the dockerfile appears in
- Open a shell window in this directory and run *docker build -t malmoserver .*
- Grab a coffee and a donut, this will take 40 minutes on average!

## Updating Docker Container After a New Release --> Building From Source
- Navigate to the root (top level) of the MalmoContainer directory, this is the same level that the dockerfile appears in
- Open a shell window in this directory and run *docker build -t malmoserver --build-arg CACHE_BREAKER=somestring .*
- You can replace the word "somestring" with any string of your choice, as long as it is unique each time
- This build is significantly faster, as the majority of the image layers are already built

## Updating Docker Container After a New Release --> Pulling New Image 
- Open a shell window and run docker login --username foo --password bar. Replace foo and bar with your username and password.
- Then run docker pull gcr.io/asist-2130/malmoserver:latest
- This should update your current malmoserver image, correctly altering only the image layers that have changed

## Configuration
- You must configure the MQTT Host before using the container. THis can be done in the Local/MalmoContainer/ConfigFolder/config.json file. In the field labeled "mqtthost", enter the IP address of the machine running the ELk Stack in quotes.

## Tailing the log of the Docker container
- docker logs -f malmo-server

## Connecting a shell to Docker container
- Works better on Windows from a Powershell window (in VS Code)
- docker exec -it malmo-server /bin/bash

## Running an example Python script from within the docker container
- cd /home/malmo/MalmoPlatform/build/install/Python_Examples
- python3 TestScript.py

