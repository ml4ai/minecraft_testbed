# ClientMapSystem Instructions

## Building Docker container
- All containers can be built by running either the testbed_build.sh, testbed_build.cmd, or testbed_build.ps1 scripts from the Local directory. Choose whichever is suitable for you operating system and environment. 

- If you wish to build the container by itself follow the steps below:

### Building the Docker Container By Itself
- Navigate to the root (top level) of the ClientMapSystem directory, this is the same level that the dockerfile appears in
- Open a shell window and run *docker build -t client_map .*

## Updating Docker Container After a New Release --> Building From Source
- Navigate to the root (top level) of the ClientMapSystem directory, this is the same level that the dockerfile appears in
- Open a shell window in this directory and run *docker build -t client_map --build-arg CACHE_BREAKER=somestring .*
- You can replace the word "somestring" with any string of your choice, as long as it is unique each time
- This build is significantly faster, as the majority of the image layers are already built, and only new layers will be updated

## Configuration

- The Client Map configuration is done in the docker-compose.asistmod.yml file, in the clientmap service section

## Usage

- The Client Map interface can be found at https://depolyment-ip-or-domain:9000/ClientMap/
- Once you know your Minecraft Playername, it can be entered into the login page, along with the developlment password: "admin"
- The Client Map currently shows the player's position during the mission, and allows for basic chat intervention messages from an agent
- To see how an agent might send a message to the Client Map, see the TestAgent system in ReferenceAgents/TestAgent directory.
- Note: It is intended that the ClientMap take up only 1/3rd of the player's screen (horizontally), with the remaining 2/3rd's being utilized by the Minecraft GUI
