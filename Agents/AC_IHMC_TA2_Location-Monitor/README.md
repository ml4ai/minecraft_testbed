# IHMC Location Monitor Agent Instructions

## Configuration
- The configuration files and maps are located in the `testbed/Agents/AC_IHMC_TA2_Location-Monitor/ConfigFolder`.
- The configuration file, `config.json`, contains the settings for the MQTT Host, the agent's version_info, 
and also specifies a "missions to Maps" filename.
    - The field labeled `"host"` should contain the IP address of the machine running the MQTT Message Bus 
    in quotes. 
    - The file referenced by the `"maps"` config entry contains mission to Area Map filename mappings that 
    will be used.  You can add more map files to this directory and change the setting to have the Agent 
    use new maps.
- These files can be changed before starting the docker container and changes do not require you to recreate 
the docker image.

## Running Locally
The scripts `run_locally.sh` and `run_locally.cmd` enable running the Location Monitor locally without having 
to build and run a docker image.  For the code to work you will need to have Python 3.8 or higher installed 
on your system, a working version of `git`, and then install the `ASISTAgentHelper` library using the 
`requirements.txt` file with `pip`.  You will also need to make sure the `host` value in the `config.json` 
file points to the location of the MQTT bus.

## Building the Docker container
- In a shell window, navigate to the `testbed/Agents/AC_IHMC_TA2_Location-Monitor` directory, this is the same level 
as this README.md file, and run: 
    - linux: `./agent.sh build`
    - Windows: `agent.cmd build`

## Running the Docker container
- In a shell window, navigate to the `testbed/Agents/AC_IHMC_TA2_Location-Monitor` directory, this is the same level 
as this README.md file, and run the agent command with either `up` or `upd`.  `up` will run the docker container
and output the log to the console.  `upd` will run the docker container in the background: 
    - linux: `./agent.sh up` or `./agent.sh upd`
    - Windows: `agent.cmd up` or `agent.cmd upd`

## Stopping the Docker container
- Press **Ctrl-C** to stop the container if started with the `up` option.
- To clean up docker and stop the Agent (if started with `upd`), navigate to the `testbed/Agents/AC_IHMC_TA2_Location-Monitor` 
directory, this is the same level as this README.md file, and run:
    - linux: `./agent.sh down`
    - Windows: `agent.cmd down`

## Observables (Subscribed Topics)
- [**agent/control/rollcall/request**](https://gitlab.com/artificialsocialintelligence/study3/-/tree/main//MessageSpecs/Agent/rollcall/agent_rollcall.md)
  - Used to know when to publish a rollcall response
- [**trial**](https://gitlab.com/artificialsocialintelligence/study3/-/tree/main//MessageSpecs/Trial/trial.md)
  - Used to retain experiment and trial ids and associated participant ids and call signs for publish events and to know which map is being used in the trial.
- [**observations/state**](https://gitlab.com/artificialsocialintelligence/study3/-/tree/main//MessageSpecs/PlayerState/observation_state.md)
  - Used to determine participant location based on position values.

## Measurements (Published Topics)
- [**agent/control/rollcall/response**](https://gitlab.com/artificialsocialintelligence/study3/-/tree/main//MessageSpecs/Agent/rollcall/agent_rollcall.md)
  - Published whenever an **agent/control/rollcall/request** message is received.
- [**agent/AC_IHMC_TA2_Location-Monitor/versioninfo**](https://gitlab.com/artificialsocialintelligence/study3/-/tree/main//MessageSpecs/Agent/versioninfo/agent_versioninfo.md)
  - Published at start of trial.
- [**status/AC_IHMC_TA2_Location-Monitor/heartbeats**](https://gitlab.com/artificialsocialintelligence/study3/-/tree/main//MessageSpecs/Status/status.md)
  - Published at a frequency which is defined in the config.json file.  (Default is every 10 seconds.)
- [**ground_truth/semantic_map/initialized**](https://gitlab.com/artificialsocialintelligence/study3/-/tree/main//MessageSpecs/GroundTruth/SemanticMap/semanticmap_message.md)
  - Published at start of trial so that the semantic map used for location determination is published with the trial.
- [**observations/events/player/location**](https://gitlab.com/artificialsocialintelligence/study3/-/tree/main//MessageSpecs/LocationMonitor/location_event_message.md)
  - Published for each individual participant as the participant's semantic map location changes.
