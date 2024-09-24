# CMU Background of Experience, Affect, and Resources Diagnostic AC
CMU TA2's Background of Experience, Affect, and Resources Diagnostic AC (BEARD-AC) uses survey and training data to generate a profile for the players and the team. Pavan Kantharaju from SIFT implemented this version of the agent. This started from the `IHMCPythonAgentStarter` code. All conceptual questions can be directed to folks at CMU TA2: Fade Eadeh, Pranav Gupta, or Anita Woolley. 

**Inputs: **
1. Gaming Experience: Simple average of 2 items that captures participants' gaming experience (MC_Prof_6, MC_Prof_7 OR QID870, QID869)
2. Mission Knowledge (sc0 variable OR SC_0dFvjllRXQzBoYR): Number of correct answers out of 8 (10 points per answer)
3. Anger: 2 item simple average derived from the Positive and Negative Affect Schedule (PANAS_8, PANAS_11 OR QID883_8, QID883_11).
4. Anxiety: 4 item simple average of PANAS (PANAS_7, PANAS_15, PANAS_18, PANAS_20 OR 883_7, 883_15, 883_18, 883_20)
5. Social Perceptiveness: Number of correct answers from the Reading the Mind in the Eyes Task (RMIE_1 to RMIE_72 OR QIDs 751-821)
6. Spatial Ability: Multi-item scale based on the Santa Barbara Sense of Direction Scale (QID13_1, QID13_2r, QID13_3, QID13_4, QID13_5, QID13_6r, QID13_7, QID13_8r, QID13_9, QID13_10r, QID13_11r, QID13_12r, QID13_13r, QID13_14, QID13_15r)
Minecraft Skill (Pranav please add something here)
7. Competency variables: Variables computed using the testbed topics "observations/events/competency/task" and "observations/events/player/role_selected"

AC's Expected output Frequency and Timing: once at the start of Mission 1 and Mission 2.

Specifically, the AC outputs the following measures for the team:
| Class             | Measures                      | Data Source |
| -----------       | -----------                   | ----------- |
| Emotions          | `anger_mean`, `anger_sd`      | Survey |
| Emotions          | `anxiety_mean`, `anxiety_sd`  | Survey |
| Skill (Social)    | `rmie_mean`, `rmie_sd`        | Survey |
| Skill (Spatial)   | `sbsod_mean`, `sbsod_mean`    | Survey |
| Skill (Gaming)    | `gaming_experience_mean`, `gaming_experience_mean`| Survey |
| Skill (Knowledge) | `mission_knowledge_mean`, `mission_knowledge_sd`| Survey |
| Skill (Minecraft) | `walking_skill_mean`, `walking_skill_sd`| Competency Test |
| Skill (Minecraft) | `marking_skill_mean`, `marking_skill_sd`| Competency Test |
| Skill (Minecraft) | `transporting_skill_mean`, `transporting_skill_sd`| Competency Test |

And the following for each player:
| Class             | Measures              | Data Source |
| -----------       | -----------           | ----------- |
| Attribute         | `role`                | Competency Test |
| Emotions          | `anger`               | Survey |
| Emotions          | `anxiety`             | Survey |
| Skill (Social)    | `rmie`                | Survey |
| Skill (Spatial)   | `sbsod`               | Survey |
| Skill (Gaming)    | `gaming_experience`   | Survey |
| Skill (Knowledge) | `mission_knowledge`   | Survey |
| Skill (Minecraft) | `walking_skill`       | Competency Test |
| Skill (Minecraft) | `marking_skill`       | Competency Test |
| Skill (Minecraft) | `transporting_skill`  | Competency Test |

We recommend creating z-scores (x-mean/sd) for each variable outputted by the BEARD agent (x = variable ouputted by BEARD agent)
based on benchmark data from ASIST Study 2:
| Variable                                                  | Measures              | Source            | Level         | Mean  | SD    |
| -----------                                               | -------               | -------           | -----------   | ----  | ----  |
| Gaming Experience                                         | `gaming_experience`   | Survey            | Individual    | 4.07  | 0.81  |
| Gaming Experience                                         | `gaming_experience`   | Survey            | Team          | 4.08  | 0.46  |
| Mission Knowledge                                         | `mission_knowledge`   | Survey            | Individual    | 70.49 | 12.27 |
| Mission Knowledge                                         | `mission_knowledge`   | Survey            | Team          | 70.38 | 7.15  |
| Anger                                                     | `anger`               | Survey            | Individual    | 1.20  | 0.52  |
| Anger                                                     | `anger`               | Survey            | Team          | 1.20  | 0.34  |
| Anxiety                                                   | `anxiety`             | Survey            | Individual    | 1.66  | 0.68  |
| Anxiety                                                   | `anxiety`             | Survey            | Team          | 1.66  | 0.42  |
| Social Perceptiveness (Reading the Mind in the Eyes Task) | `rmie`                | Survey            | Individual    | 0.74  | 0.11  |
| Social Perceptiveness (Reading the Mind in the Eyes Task) | `rmie`                | Survey            | Team          | 0.74  | 0.06  |
| Spatial Ability                                           | `sbsod`               | Survey            | Individual    | 4.89  | 0.99  |
| Spatial Ability                                           | `sbsod`               | Survey            | Team          | 4.89  | 0.58  |
| Walking Skill                                             | `walking_skill`       | Competence Test   | Individual    | 0.47  | 0.08  |
| Walking Skill                                             | `walking_skill`       | Competence Test   | Team          | 0.47  | 0.08  |

## Possible Failures and Solutions

- It is possible that survey information necessary for computing survey variables may not be available (i.e., players did not respond to the relevant survey questions or there was an error with the survey). There are two possibilities: (1) none of the information needed to compute a survey variable is available, or (2) information needed to compute a survey variable is available from at least one player.
    - (1) BEARD will set the survey variable's value to -1. The "-1" here means that this variable could not be computed and should not be used.
    - (2) BEARD will use the information from those players when computing the survey variables.

- The BEARD agent utilizes information from the competency test when calculating competency variables, and thus is required to run from start to end of an experiment. If the BEARD agent is shut down after the competency test, those variables will not be computed and set to 0.0.
    - NOTE: It may be possible to replay the competency test metadata prior to the start of Missions 1 or 2 so it can recompute those variables. However, Pavan Kantharaju, who coded up the AC, has not tested this.

# What to Run
To facilitate local development, we have created a
[poetry](https://python-poetry.org/docs/) configuration. You should run `poetry
install` to create and set up the Python virtual environment. Then, start the
virtual environment as in `poetry shell`. The rest of the commands below assume
that you are in this poetry shell.

## Playback with Elkless Replayer
You can test the agent by playing back a saved metadata file. In one shell, start this AC:
```
./run_locally.sh
```

In a second shell, run the elkless replayer (replace the metadata filename with one that is valid on your file system):
```
cd ../../Tools/replayers/elkless_replayer
./elkless_replayer ../../../../hsr-study-2/raw/train/HSRData_TrialMessages_Trial-T000417_Team-TM000109_Member-na_CondBtwn-1_CondWin-SaturnA_Vers-2.metadata
```

## Live with Zero-Conf Testbed
You can also run a live test with the zero-conf testbed. See the instructions in
the zero-conf [README](../../Tools/zero_conf/README.md) for details. Basic order
of operations:

1. Start your Minecraft client and make note of your player name.

2. Start the Minecraft bootstrapper script (in the zero_conf directory).
   ```
   ./bootstrap_minecraft.py Player231
   ```

3. Start this AC (in the poetry shell):
   ```
   ./run_locally.sh
   ```

4. Start the Minecraft server(in the zero_conf directory).
   ```
   ./light_testbed.py
   ```

5. Connect your Minecraft client to the local server.

6. In the bootstrapper, press `s` to start a trial.

7. In Minecraft, click the mission start button and start doing things.

Once this is set up, you can repeat 6 and 7 whenever you like. You can also
restart the AC whenever you like. But each time you restart the AC, you need to
do 6 and 7 so that it will start doing meaningful tracking.

# Updating the Version
When updating the version, be sure to change the values in both the
`pyproject.toml` and `ConfigFolder/config.json` files. Also add comments to the
changelog below.

## Changelog

### 0.0.7
- Add stronger error handling to survey data
- Add stronger error handling to competency data
- Future-proof survey variables

### 0.0.6
- Agent state resets after every experiment/team

### 0.0.5
- Fix pylint issues.

### 0.0.4
- Added calculation of competency skill variables to the BEARD agent.
- Renamed directory to adhere to agent naming convention in agent dev guide.
- Ensured survey variables are computed only using Sections 0 and 1 of survey.

### 0.0.3
Fixed reading of survey data. Survey data is no longer located in `survey_response` within the
`data` json object.

### 0.0.2
Survey data variables added to the agent

### 0.0.1
Initial version. This is the version number used while working through the
mechanics and setting up the skeleton.

# ------------------ From the original IHMC Agent Starter Code ------------------

# IHMC Python Agent Starter

The IHMC Python Agent Starter provides a simple implementation of an ASIST agent which
can be quickly copied and used by anyone.  It uses a library (ASISTAgentHelper) which
deals with managing the connection to the MQTT bus and provides methods to subscribe to
and publish topics.  Furthermore, it makes sure your agent is a 'model citizen' in the
ASIST agent world by handling agent heart beats, version_info messages, and roll call
messages in the background so all you have to worry about is your agent's specific code.

## Setup

### Copy this Folder
First you should copy this folder an place it in an appropriate location.  If you are
going to commit your agent to Aptima's gitlab repository, then you should copy this
folder to the <testbed>/Agents folder and rename it so that it reflects what your
agent will be doing and the group you are with.  You can also just place the copied
folder anywhere, and it will also work.

### Edit `settings.env` `requirements.txt` and `config.json`

#### `settings.env`
The `settings.env` file is used to specify the main python script to run for your agent,
the docker image and container names, and the agent's name on the message bus.  Note
that the docker image name must be all lowercase.

    DOCKER_IMAGE_NAME_LOWERCASE=your_docker_image_name
    DOCKER_CONTAINER_NAME=My_Simple_Agent_Container
    AGENT_NAME=My_Simple_Agent
    AGENT_MAIN_RUN_FILE=SimpleAgent.py

Two example agents have been provided.  The first one is a very simple agent specified in
`settings_simple.env` and `src/SimpleAgent.py`.  This first agent shows how to subscribe to
messages and how to handle receiving them.  The second example defined in `settings_complex.env`
and `src/MoreComplexAgent.py` goes into how to turn on logging, load extra configuration
information, and how to publish messages on the bus.  To test the two examples agents, just
replace `settings.env` with either `settings_simple.env` or `settings_complex.env` and then
build and run the agent (see **Building and Running below**).

#### `requirements.txt`
When you start writing your own agent code and you find that you need to install any additional
Python libraries, you can simply add them to the `requirement.txt` file.

#### `ConfigFolder`
The config folder is the location were you place any configuration files related to your agent.
For example the semantic maps used by IHMC's location monitor are placed here.  It uses the
ASISTAgentHelper class's `config_folder` variable to locate the maps and load them.  One file
that must always be in this folder is `config.json`.

#### `ConfigFolder/config.json`
This file contains information on the location of the MQTT bus (`host` and `port`) and a definition
of your agent (`version_info`) which is published on the message bus when trials start. `heartbeats_per_minute`
defines how many times a minute your agent will publish a heartbeat message.

Here is an example of a `config.json` file which connects to the MQTT bus on mosquitto:1883, publishes
a heartbeat message every 10 seconds (if a trial is running), subscribes to 4 topics, and may publish
one chat message.  The format of `version_info` is defined in Aptima's gitlab repository as the `data`
item under `MessageSpecs/Agent/versioninfo`.  (`agent_name` is automatically set by the ASISTAgentHelper
from the value set in `setting.env`.)

    {
        "host":"mosquitto",
        "port": "1883",
        "heartbeats_per_minute": 6,
        "version_info": {
            "owner": "IHMC - TA2",
            "version": "0.0.1",
            "source": [
                "https://gitlab.com/artificialsocialintelligence/study3/-/tree/main/ReferenceAgents/IHMCPythonAgentStarter"
            ],
            "publishes": [
                {"topic": "agent/intervention/My_Complex_Agent/chat", "message_type": "agent", "sub_type": "Intervention:Chat"}
            ],
            "subscribes": [
                {"topic": "trial", "message_type": "trial"},
                {"topic": "observations/events/mission"},
                {"topic": "observations/events/player/role_selected", "message_type": "event", "sub_type": "Event:RoleSelected"},
                {"topic": "observations/events/player/triage", "message_type": "event", "sub_type": "Event:Triage"}
            ]
        }
    }

### Create the Agent Script

#### Minimal ASIST Agent using the `ASISTAgentHelper` Library
This is the agent helper library that does most of the heavy work of managing the MQTT bus.  The source for the
library can be found on GitLab at https://gitlab.com/ihmc-asist/python-agent-helper. To see how it works let's
look at a minimal script:

    # import the ASISTAgentHelper class
    from asistagenthelper import ASISTAgentHelper

    # Define the method to call when subscribed to messages are received
    def on_message(topic, header, msg, data, mqtt_message):
        print("Received a message on the topic: ", topic)

    # Initialize the helper class and tell it our method to call
    helper = ASISTAgentHelper(on_message)

    # Set the agent's status to 'up' and start the Main loop (which does not return)!!!
    helper.set_agent_status(helper.STATUS_UP)
    helper.run_agent_loop()

That's it.  This is all you need to have a 'model citizen' agent which runs on the ASIST Testbed.  The
ASISTAgentHelper class handles connecting to the MQTT message bus, subscribing the to topics listed in
`config.json` and dealing with publishing the required heartbeat, versionInfo, and rollcall messages for
you, so as long as you have the `version_info` set correctly in the `config.json` file your agent is
good to go.

## ASISTAgentHelper Methods

These are the methods and variables provided for use by the ASISTAgentHelper class.  Many of these are
demonstrated in `src/MoreComplexAgent.py`:

| Method/Variable | Description |
| --- | --- |
| agent_name | This variable holds the agent's name loaded from `settings.env`. |
| config_folder | This variable holds the path to the `ConfigFolder`. |
| is_connected() | Returns True if the agent is connected to the MQTT message bus, otherwise it returns False. |
| get_version_info() | Returns the version_info object read in from the `config.json` file |
| get_logger() | Returns the logger (see `src/MoreComplexAgent.py` for an example.|
| generate_timestamp() | Helper method which returns an ASIST formatted timestamp string. |
| set_agent_state(state, message=None) | Sets the agents state which can be 'ok' or 'error' and a corresponding message if appropriate.  This is reported to the system when heartbeat messages are published. (See `MessageSpec/Status`) |
| set_agent_status(status) | Sets the agent's status, which can be one of the following: "initializing", "up", "down", or "unknown".  The status is reported when a roll call message is published.  By default an agent's status is set to 'initializing'.  You should change it to 'up' when it is ready to run and then change it depending on your agent. (See `MessageSpece/Agent/rollcall`) |
| send_msg(topic, message_type, sub_type, sub_type_version, timestamp=None, data=None, trial_key=None, msg_version="1.1") | Publishes an ASIST formatted message (header, msg, data?) on the message bus. (If a trial key is not provided then the trial info for the msg section is obtained from the last trial topic message received.) |
| get_trial_key(msg) | If passed the `msg` part of a message bus message will return a trial key which can be used in the `send_msg` and `get_trial_info` methods. |
| get_trial_info(trial_key) | Returns the `data` part of the associated trail start message was received. (See `MessageSpecs/Trial`) |
| subscribe(topic, message_type=None, sub_type=None | Subscribes to the specified message bus topic. |
| unsubscribe(topic, message_type=None, sub_type=None | Unsubscribes from the specified message bus topic. |
| run_agent_loop() | This will start the agent loop which manages connecting to the MQTT bus and sending heartbeat messages. Note that this method will not return!! |
| start_agent_loop_thread() | Starts the agent loop on a separate thread. |
| stop_agent_loop_thread() | Stops the agent loop if it is running on a separate thread. |

## Developing Locally
The scripts `run_locally.sh` and `run_locally.cmd` have been provided for you to be able to run and develop your
agent locally without having to build and run a docker image.  For the code to work you will need to have Python
3.8 or more installed on your system, a working version of git, and then install the ASISTAgentHelper library
from the requirements.txt file using pip.  You will also need to make sure the `host` value in the `config.json`
file points to the location of the MQTT bus.

## Building and Running Your Agent with `./agent.sh` and `./agent.cmd`
The Agent scripts have been provided to help you build, start, stop, and export your agent as a docker container.
For linux systems use `agent.sh` and for Windows use `agent.cmd`.

The parameters which you can pass to these scripts are as follows (replace `./agent.sh` with `agent.cmd`
on windows systems):

    ./agent.sh build

`build` will build the docker image for your agent.  This must be done before you can run your agent and must
be re-run whenever you change `settings.env` or your agent's code.

    ./agent.sh up
`up` will start your docker image in a container and output will be sent to the console.
The container will stay running until you press Ctrl-C to stop it.

    ./agent.sh upd
`upd` will start your docker image in a container which will run in the background. Use the next
command to stop it.

    ./agent.sh down
`down` will stop your running docker container.

    ./agent.sh export
`export` will save your docker image as a tar file in the current directory.

## Example output from the `MoreComplexAgent`

```
(venv) Rogers-MacBook-Pro:IHMCPythonAgentStarter rcarff$ ./run_locally.sh
2021-10-03 20:41:39,151 | MoreComplexAgent | INFO — Starting Agent Loop on a separate thread.
2021-10-03 20:41:39,151 | asistagenthelper.ASISTAgentHelper | INFO — Starting ASIST Agent Loop: My_Complex_Agent
2021-10-03 20:41:39,151 | MoreComplexAgent | INFO — Agent is now running...
2021-10-03 20:41:39,151 | asistagenthelper.ASISTAgentHelper | INFO — Starting the MQTT Bus pub/sub system...
2021-10-03 20:41:39,154 | asistagenthelper.ASISTAgentHelper | INFO — - Connected to the Message Bus.
2021-10-03 20:44:14,004 | asistagenthelper.ASISTAgentHelper | INFO — Received message for topic: trial
2021-10-03 20:44:14,004 | MoreComplexAgent | INFO — Received a message on the topic: trial
2021-10-03 20:44:14,004 | MoreComplexAgent | INFO —  - Trial Started with Mission set to: Saturn_A
2021-10-03 20:45:35,400 | asistagenthelper.ASISTAgentHelper | INFO — Received message for topic: observations/events/player/role_selected
2021-10-03 20:45:35,400 | MoreComplexAgent | INFO — Received a message on the topic: observations/events/player/role_selected
2021-10-03 20:45:35,400 | MoreComplexAgent | INFO —  - At 0:5.841 into the mission IHMC1 selected the role: Hazardous_Material_Specialist
2021-10-03 20:45:35,400 | MoreComplexAgent | INFO —  - Publishing a comment on the roll change!!
2021-10-03 20:45:45,585 | asistagenthelper.ASISTAgentHelper | INFO — Received message for topic: observations/events/player/role_selected
2021-10-03 20:45:45,586 | MoreComplexAgent | INFO — Received a message on the topic: observations/events/player/role_selected
2021-10-03 20:45:45,586 | MoreComplexAgent | INFO —  - At 1:23.125 into the mission IHMC1 selected the role: Medical_Specialist
2021-10-03 20:45:45,586 | MoreComplexAgent | INFO —  - Publishing a comment on the roll change!!
```

## Questions
Questions should be directed to Roger Carff on the ASIST Slack Channel.
