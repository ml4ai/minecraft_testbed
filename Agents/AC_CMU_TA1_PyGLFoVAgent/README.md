# PyGL FoV Agent Instructions

The PyGL FoV Agent computes a summary of blocks of interest in each participant's viewport, using OpenGL to render the scene as seen by the participant.

## Observables (Subscribed Topics)

* [trial](https://gitlab.com/artificialsocialintelligence/study3/-/tree/main//MessageSpecs/Trial/trial.md)
    * used to know which map the participants are in, and the names / participant_ids of the participants to be monitored, and when to generate heartbeat messages
* [ground_truth/mission/blockages_list](https://gitlab.com/artificialsocialintelligence/study3/-/tree/main//MessageSpecs/GroundTruth/BlockageList/blockagelist_groundtruth_message.md)
    * used to know the locations of _static_ rubble in the environment
* [ground_truth/mission/threatsign_list](https://gitlab.com/artificialsocialintelligence/study3/-/tree/main//MessageSpecs/GroundTruth/ThreatSignList/threatsign_groundtruth_message.md)
    * used to know the location of threat signs (used in Study 2)
* [ground_truth/mission/victims_list](https://gitlab.com/artificialsocialintelligence/study3/-/tree/main//MessageSpecs/GroundTruth/VictimList/victimlist_groundtruth_message.md)
    * used to know the location of victims in the environment
* [observations/events/player/door](https://gitlab.com/artificialsocialintelligence/study3/-/tree/main//MessageSpecs/Door/door_event_message.md)
    * used to know the state of each door in the environment (open or closed)
* [observations/events/player/lever](https://gitlab.com/artificialsocialintelligence/study3/-/tree/main//MessageSpecs/Lever/lever_event_message.md)
    * used to know the state of each lever in the environment (actived / deactivated)
* [observations/events/perturbation/marker_destroyed](https://gitlab.com/artificialsocialintelligence/study3/-/tree/main//MessageSpecs/MarkerDestroyed/marker_destroyed_event_message.md)
    * used to know when a marker is removed from the environment
* [observations/events/player/marker_removed](https://gitlab.com/artificialsocialintelligence/study3/-/tree/main//MessageSpecs/MarkerRemoved/marker_removed_event_message.md)
    * used to know when a marker is removed from the environment
* [observations/events/player/marker_placed](https://gitlab.com/artificialsocialintelligence/study3/-/tree/main//MessageSpecs/MarkerPlaced/marker_placed_event_message.md)
    * used to know when a marker is placed in the environment
* [observations/events/mission](https://gitlab.com/artificialsocialintelligence/study3/-/tree/main//MessageSpecs/MissionState/missionstate_event_message.md)
    * used to know when to start and stop generating FoV messages
* [observations/events/player/rubble_collapse](https://gitlab.com/artificialsocialintelligence/study3/-/tree/main//MessageSpecs/RubbleCollapse/rubble_collapse_event_message.md)
    * used to know when _dynamic_ rubble appears in the environment
* [observations/events/player/rubble_destroyed](https://gitlab.com/artificialsocialintelligence/study3/-/tree/main//MessageSpecs/RubbleDestroyed/rubble_destroyed_event_message.md)
    * used to know when rubble is removed from the environment
* [observations/events/server/rubble_placed](https://gitlab.com/artificialsocialintelligence/study3/-/tree/main//MessageSpecs/RubblePlaced/rubble_placed_event_message.md)
    * used to know when _dynamic_ rubble appears in the environment
* [agent/control/rollcall/request](https://gitlab.com/artificialsocialintelligence/study3/-/tree/main//MessageSpecs/Agent/rollcall/agent_rollcall.md)
    * used to generate responses to the testbed
* [observations/events/player/triage](https://gitlab.com/artificialsocialintelligence/study3/-/tree/main//MessageSpecs/Triage/triage_event_message.md)
    * used to know when a victim changes stabilization state
* [observations/events/player/victim_picked_up](https://gitlab.com/artificialsocialintelligence/study3/-/tree/main//MessageSpecs/VictimPickedUp/victim_picked_up_event_message.md)
    * used to know when a player picks up a victim
* [observations/events/player/victim_placed](https://gitlab.com/artificialsocialintelligence/study3/-/tree/main//MessageSpecs/VictimPlaced/victim_placed_event_message.md)
    * used to know the location where a victim is placed in the environment
* [observations/events/perturbation/victim_no_longer_safe](https://gitlab.com/artificialsocialintelligence/study3/-/tree/main//MessageSpecs/VictimNoLongerSafe/victim_no_longer_safe_event_message.md)
    * used to know if any victims become unstable again
* [ground_truth/mission/victims_expired](https://gitlab.com/artificialsocialintelligence/study3/-/tree/main//MessageSpecs/GroundTruth/VictimsExpired/victimsexpired_event_message.md)
    * used to know when victims change from critical to expired
* [observations/state](https://gitlab.com/artificialsocialintelligence/study3/-/tree/main//MessageSpecs/PlayerState/observation_state.md)
    * used to monitor the position and orientation of each participant, and generate FoV messages


## Measurements (Published Topics)

* [agent/control/rollcall/response](https://gitlab.com/artificialsocialintelligence/study3/-/tree/main//MessageSpecs/Agent/rollcall/agent_rollcall.md)
    * Published in accordance to agent-testbed interaction protocol
* [agent/pygl_fov/versioninfo](https://gitlab.com/artificialsocialintelligence/study3/-/tree/main//MessageSpecs/Agent/versioninfo/agent_versioninfo.md)
    * Published at the start of trial in accordance to agent-testbed interaction protocol
* [status/pygl_fov/heartbeats](https://gitlab.com/artificialsocialintelligence/study3/-/tree/main//MessageSpecs/Status/status.md)
    * Periodically published in accordance to agent-testbed interaction protocol.
* [agent/pygl_fov/player/3d/summary](https://gitlab.com/artificialsocialintelligence/study3/-/tree/main//MessageSpecs/PyGLFoVAgent/fov.md)
    * Published after `observations/state` messages, as frequently as possible given the platform the agent is running on.

## Requirements

The agent requires three packages to be installed, `MinecraftElements`, `MinecraftBridge`, and `pygl_fov`.  The URLS for the repos are

* `MinecraftElements` - https://gitlab.com/cmu_asist/MinecraftElements

* `MinecraftBridge` - https://gitlab.com/cmu_asist/MinecraftBridge

* `pygl_fov` - https://gitlab.com/cmu_asist/pygl_fov

Each of these packages will have their own dependencies, which are listed in the corresponding `README.md` files in the repos.

In general, the repos can be cloned and installed via pip.  For each of the above packages, the general approach is:

    git clone https://gitlab.com/cmu_asist/<package_name>
    cd <package_name>
    pip3 install --user -e .

Note that these can be installed in an arbitrary location.  The `--user` flag can be omitted, if desired, and administrative priviledges are available.


## Running

From the root directory, the agent can be run from command line

    python3 src/PyGLFoVAgent.py

Note that the testbed needs to be running and generating messages to the MQTT bus for the agent to actually generate output.


## Building the Docker container
- From the root directory of this repo, run `./build.sh` (Linux) or `build.cmd` (Windows).


## Configuration
- The configuration file, `config.json`, contains the settings for the MQTT Host.
    - The field labeled `"host"` should contain the IP address of the machine running the MQTT Message Bus in quotes. 
    - The field labeled `"port"` should contain the port number of the machine running the MQTT Message Bus in quoates.
	- The paths to the map files is in the field labeled `"maps"`
- Map files (in JSON format) should be stored in the `ConfigFolder/maps` folder.
- `window_size` indicates the size of the player's Minecraft screen, and should match (as close as possible) to the player's actual screen.  At a minimum, the aspect ratio (width:height) should be maintained to avoid false positives and negatives with respect to block detection.
-`block_type` refers to the blocks the FoV agent should summarize and report on.  Only blocks of these types will be present in the generated messages.  To include all block types in messages, remove the `block_type` entry (including the key, don't just have an empty list).  By default, the block list includes doors, levers, torches, victims (all types), blockages (gravel and bedrock), and fire.


## Running the Docker container
- From the root directory of this repo, run `./up.sh` (Linux) or `up.cmd` (Windows).


## Stopping the Docker container
- Press **Ctrl-C** to stop the container.
- To clean up docker and stop the Agent, run `./down.sh` (Linux) or `down.cmd` (Windows).


## Scripts
Multiple scripts are provided in the `scripts/` directory.  See the `README.md` file in this folder for details on each script.
