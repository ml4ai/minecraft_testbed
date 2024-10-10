Testbed Local Testbed Setup and Run Process
======================================

Prerequisites
-------------
[ASIST gitlab](https://gitlab.com/artificialsocialintelligence/study3/)
* Docker:
  * for Linux V19.03.11 or newer
  * docker-compose: 1.29.2 or newer
* Access to an elevated shell such as Windows Powershell (Administrator). This is not always necessary, depending on your host configuration.
* At least one Minecraft Java Edition Client V1.11.2 , with Forge 13.20.1.2588 and
  the Asist Mod installed.  The latest ASIST mod can be found in the software repository in Local/data/mods/asistmod-x.x.x.jar

* While you may run the testbed and all Minecraft Clients on one machine, we have found that in an expirmental environment it is best to have one dedicated testbed machine,, and 3 dedicated client machines on which to run the clientside synthetic environment. In the case of ASIST, this is the Minecraft Client.
* In order for experimenters and clients to be able to access the machine on which the testbed is running, the following ports need to be accessible:
  - Kibana - 5601 --> accessed @ http://your_machines_ip:5601
  - Minecraft control website - 9000-9001 --> accessed @ https://your_machines_ip:9000/MalmoControl
  - Minecraft asist mod - 25565 accessed @ https://your_machines_ip:25565
  - mosquitto broker - 1883 accessed @ http://your_machines_ip:1883
  - metadata export - 8082 accessed @ http://your_machines_ip:8082
  - elasticsearch - 9200 @ http://your_machines_ip:9200

* Make sure your containers have at least 4GB of memory allocated to them in Docker.

* **(macOS only)** Go to your Docker Preferences, then click 'Experimental
  Features' in the sidebar on the left, then disable the 'Use gRPC FUSE for
  file sharing' option.

#  Install prerequisite software
 - Install git
   - You can get git from [git download](https://git-scm.com/downloads)
 - Install docker
   - You can get docker from [docker download](https://www.docker.com/products/docker-desktop)
   - Note that docker is changing their licensing agreement and you will soon need a subscription to use it for commercial purposes
 - Install docker-compose
   - docker-compose is included with docker desktop for Windows and Macs.  For Linux systems see [docker-compose install](https://docs.docker.com/compose/install/)

#  Building the testbed containers
 - From the directory where the testbed repository was cloned
 - set the directory to Local and run the command script for the operating system you are running on
   - Linux or Mac: `./testbed_build.sh`

 - Get the containers from the GitLab container registry
Detailed instructions on how to do this can be found in [`README_docker_build.md`](README_docker_build.md).

After either building the containers or pulling them, follow the
instructions below to start up the testbed.

# Starting up the testbed
* Change directory to `Local`
* If you have previously started up the testbed on this computer make sure that
  there are no old containers.  Run the script `testbed_down.sh` (Linux/macOS)
  or `testbed_down.cmd` (Windows) to shut down any existing running containers.
* Run the `testbed_up-core.sh -i` (Linux/macOS) script to start up the containers.
* **Note**: If you are running Google Speech-to-Text transcription, you will
  need to ensure that your Google application credentials JSON file is in the
  `Agents/speechAnalyzer` directory with the filename
  `google_application_credentials.json`. If you are not planning to run
  Speech-to-Text, then run `./testbed_up.sh -a` instead of `./testbed_up.sh`.
  Additionally, ASR will not work with Safari (at least not without jumping
  through a bunch of hoops). Use Google Chrome to access the Client Map
  instead, but make sure to configure it to allow insecure localhost (navigate
  to this URL in your Chrome browser to get to this setting:
  chrome://flags/#allow-insecure-localhost)
* When running the entire testbed on a single computer, no additional
  configuration is needed.

If you need to run the testbed in a distributed environment where the testbed
is split across multiple computers please contact the development team.

# Minecraft client
A specific version of Minecraft Java Edition is required to use the testbed.  There are two options
1. Purchase a Minecraft Java Edition license.  Purchase price is ~$30.  Then you must install the correct version of forge and place the ASIST mod in the correct local mod direction
2. Build the Minecraft Java client from source.

See Minecraft client instructions at [Minecraft client](https://gitlab.com/artificialsocialintelligence/study3/-/tree/main//docs/ClientSetup.md)

# Running an Experiment
For details on running an experiment with the testbed see [Testbed walkthrough](https://gitlab.com/artificialsocialintelligence/study3/docs/ASIST_testbed_run_walkthrough_V3.0.docx)
* After the script has run, there are multiple resources that the testbed provides:
  * Kibana for browsing data that is collected by the testbed and stored in elasticSearch. Kibana can be accessed at: `http://<testbed computer>:5601/`
  * Testbed Control user interface which is used to start, stop, control and monitor the experiment run.  The control user interface can be accessed at: `https://<testbed computer>:9000/MalmoControl/`
  * Export and Import dashboard is used to export and import data out of and into the testbed.  This tool is mainly used to generate a json file of the messages that were published during an experiment trial.  The Export/Import dashboard can be accessed at: `http://machine-ip-or-domain:8082/`
  * Container logs are collected and available using Dozzle and can be access ed at: `https://machine-ip-or-domain:9000/Logger/`

*The Minecraft client must be running the same version of the ASIST mod that is running in the testbed.  In the software release directory (which you obtained from the testbed software repository) go to "Local\data\mods\asistmod-<version number>.jar".  This is the mod file which must be in the Minecraft Client's mod folder.


## Experiment/Trial run steps

1. Start up the testbed using the instructions above.
2. Testbed startup can take a minute or two depending on the resources of your machine. When the testbed is up, open an internet browser and navigate to *https://machine-ip-or-domain:9000/MalmoControl*

3. Here you will see various basic controls for running a Testbed experiment. This page is titled **ASIST Control Center** and the testbed version is displayed next to the page title.

4. In the top left, you will see the "System Status" widget. The most important field in this widget is the "ASIST-Mod is Ready for Connections" field. This should initially be set to "False". When the experiment is fully running and ready for Minecraft clients to connect to it, this field will change to True.

5. Help on all controls can be found in the Help icon in the Title bar, a brief explanation can be found below.

6. Before running a mission, you need to start an Experiment. This can be done via the "Mission Runner" widget in the top center the page. Begin by pressing the "Create Trial and Run Mission" button.

7. You must either Choose or Create an Experiment AND start a Trial. Begin by pressing the "Select Experiment" tab. If there are no experiments, OR
you wish to create a new one, click the "Create Experiment" Tab and enter the desired experiment information. Once you click on
"Save To Experiment Store", this experiment should become availabe in the Select Experiment tab. If it is not immediately available, close the dialog box and open it again. This should refresh the experiment list. Once you have chosen an experiment, you must create a Trial in the "Create Trial" tab. After entering all desired trial information, click "Start Trial and Run Mission". The trial JSON object should now be visible in the Trial Information panel of the screen.  The Mission/Trial will start and the System Status values will update when the testbed is ready for Minecraft clients to connect.

8. Once the testbed is ready, you can connect Minecraft Client(s) with the Asist Mod in the appropriate place. Once done, Select `Multiplayer-->DirectConnect`  Then connect to `<address of testbed host>:25565`.

NOTES:
* You can turn on message validation from the `System Status` panel by clicking on the Message Validator Active slider.  Any message errors can then be found by clicking on the `Errors` button on the top right of the page.

* You may change the mission parameters in the Local/data/mods/ModSettings.json file.
The parameters avaialable for change are:
  * "mqtthost": The ip address and port of the machine hosting the ELK Stack mqtt broker
  * "observationInterval": The interval in seconds between each subsequent observation scan/publish routine
  * "missionLength": The length of the mission in minutes and seconds
  * "criticalVictimExpirationTime" The time when all critical victimes expire if not already triaged
  * "pauseTimes": The times when the mission will pause to allow discusion with the subject
  * "triagePoints": The number of points allocated to each victim type.

You can change the above parameters BETWEEN missions without bringing down the MCRVM stack. Simply alter the field of your choice and save the ModSettings.json file. You should see the changes reflected upon running the next mission.


### Ending the Experiment/Trial

Once you are done with experiment/trial, you should click the "Stop Trial" button in the Mission Running panel and disconnect the Minecraft client from the Minecraft server.

### Shutting down the testbed
To shutdown the testbed change directory to `Local` and run the script `testbed_down.sh` (Linux, MacOS) or `testbed_down.cmd` (Windows)
