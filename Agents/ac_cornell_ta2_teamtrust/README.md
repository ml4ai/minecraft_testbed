# Cornell Team Trust Analytic Component (AC) Agent

The Cornell Team Trust AC is based off the IHMC Python Starter Agent.  It calculates measures related to players' trust in their teammates. Specifically, it calculates measures related to the players' compliance behaviors (which is widely considered as a proxy for their trusting behaviors). The AC also identifies the current sub-goal of the players based on their current actions and calculates measures related to their goal-alignmemt behaviors. 

**Note:** The AC examines the trust (i.e., compliance behavior) in the other human teammates, and not the trust in the ASI agent.

## Definitions:
Refer the [Study-3 pre-registration document](https://docs.google.com/document/d/1GF7VsNF9R95IAaj6mVZUDV2mAX5ok1Bh6Tcm8zDpIkg/edit#) for the usage of the words 'Treatment', 'Stabilize', and 'Transport'.

## (a) Player compliance
The AC currently tracks three kinds of requests - 1) treatment requests of regular and critical victims, 2) transport requests of critical victims and victims with abrasion and bone damage, and 3) rubble clear requests. The AC publishes metrics related to compliance of players to requests from their teammates. The AC uses marker-based communication to track the requests and related events to track the responses to these requests.

### Observables(inputs)
The AC uses message bus data to discover victims, identify requests, and identify events that correspond to the requests. The topics subscribed are given below and also available in the config file in 'ConfigFolder' of the agent's root directory.

- for set up
    - trial: for initializing the AC
    - ground_truth/semantic_map/initialized: for initial map information
- for victims identification
    - ground_truth/mission/victims_list
    - agent/pygl_fov/player/3d/summary
- for request identification
    - observations/state
    - observations/events/player/marker_placed
    - observations/events/player/marker_removed
    - observations/events/player/marker_destroyed
    - minecraft/chat: for identifying injury type of regular victims from message shown to medic while stabilizing
- for response identification
    - observations/events/player/triage
    - observations/events/player/victim_picked_up
    - observations/events/player/victim_placed
    - observations/events/server/victim_evacuation
    - observations/events/player/rubble_destroyed

### Output: Player compliance message
The player compliance message publishes metrics related to the compliance behavior of players during their pairwise interactions, where one player is the requestor and the other player is the responder of these requests. The metrics are calculated for each of the three types of requests, namely, treatment, transport, and rubble clear. This is done in order to account for any inherent differences in the tasks (and hence their compliance behaviors) associated with the requests. 

 Specifically, the AC outputs the following compliance measures 
 - for each player of interest (Red, Green, Blue),
 - for each type of request (Treatment, Transport, Rubble clear), and
 - for each player making the requests to the player of interest including themself (Red, Green, Blue)

| Measures              | Description                                         | Range   |
| -----------           | -----------                                         |-------- |
| `N_open_requests`     | Number of unresponded requests                      |   N     |
| `compliance_overall`  | Ratio of complied requests from trial start         | [0, 1]  |
| `compliance_rate`     | Change in compliance since the last minute          | [-1, 1] |
| `response_start_time` | Average time to start response from trial start     |   R+    |
| `response_action_time`| Average time for the actual action from trial start |   R+    |


**Frequency:** This message is published to the bus when there is a new request, when there is a change in the response status of the request, and constantly every 10 seconds. 

### Message format
The metrics are published to the topic 'agents/ac/player_compliance'. The messgage format is available at `..\MessageSpecs\Cornell_TeamTrust_AC\player_compliance_message.json`.

### Measures as teamwork process predictors
The player compliance message outputs measures related to the compliance behaviors of each player that indicates the trust (and coordination) of a player in their teammates. Players with good player compliance behaviors engage in better coordination. 

In the order of importance, good compliance behaviors include 
- high compliance rate
- low number of open requests
- low response start time
- high overall compliance
- low response action time

The last three metrics are summa


### (b) Player goal alignment message ((message yet to be published)
The team's goal is to save as many victims as possible. Teamwork and effective coordination among teammates is considered to be critical to achieving this goal. While the team has a singular high-level goal, there are several sub-goals that are to be achieved to realize this high-level team goal. Players strategize and split tasks among each other based on their roles to achieve sub-goals that contribute to achieving their team goal. Players engage in more cooperative behaviors (respond quicker, count and frequency of interactions) when their current sub-goals are aligned with one another. If the goals are misaligned, players could prioritize finishing their current tasks before responding to any request for cooperation. The AC tracks three types of subgoals - exploration, treatment, and transport - for each of the three players. 


### Observables(inputs)
The AC uses message bus data to discovedentify requests, and identify events that correspond to the requests. The topics subscribed are given below and also available in the config file in 'ConfigFolder' of the agent's root directory.

- for set up
    - trial: for initializing the AC
- for player sub-goal identification
    - minecraft/chat
    - observations/state
    - observations/events/player/marker_placed
    - observations/events/player/marker_removed
    - observations/events/player/marker_destroyed
    - observations/events/player/triage
    - observations/events/player/victim_picked_up
    - observations/events/player/victim_placed
    - observations/events/server/victim_evacuation
    - observations/events/player/rubble_destroyed


### Output: Goal-alignment message
In addition to identifying current subgoals, the AC calculates goal alignment for each pair of players and the team for three time periods - current instant, recent past (2 minutes), and since the start of the mission.


**Frequency:** This message is published to the bus constantly every 10 seconds. 

### Message format
The metrics are published to the topic 'agents/ac/player_compliance'. The messgage format is available at `..\MessageSpecs\Cornell_TeamTrust_AC\goal_alignment_message.json`.


### Measures as teamwork process predictors
The goal-alignment ratio provides information on team process. The USAR mission has role-specific tasks associated with one or more of the subgoals. Teams with too low goal-alignment indicate highly individual players with less coordination. Also, teams with too high goal-alignment indicate that players could be doing redundant work. Low and high thresholds for good team process to be provided.


## Questions
Questions should be directed to Suresh Kumaar Jayaraman on the ASIST Slack Channel.


# ------------------ From the original IHMC Agent Starter Code ------------------


## Setup

### Edit `settings.env` `requirements.txt` and `config.json`

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

