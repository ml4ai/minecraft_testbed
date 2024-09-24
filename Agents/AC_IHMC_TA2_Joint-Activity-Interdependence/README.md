# IHMC Interdependence agent

The IHMC Interdependence AC is based off the IHMC Python Starter Agent.

It computes player participation in joint activity.

### Input (observables)
- for set up:
  - trial: used to know which map is being used and who the players are
- for FOV:
  - observations/state: used on FOV calculation
  - ground_truth/mission/victims_list: used on FOV calculation
  - ground_truth/mission/blockages_list: used on FOV calculation
- for event tracking:
  - Event:Triage
  - Event:ProximityBlockInteraction
  - Event:VictimPickedUp
  - Event:VictimPlaced
  - Event:VictimEvacuated

### Output (measurements)

This AC is does not output a continuous variable as defined in the standard message format. It is event based, publishing only
as player's experience events. It is more foundational, providing information about knowledge of activity,
status of activity, progress and timeliness. This information is essential to understand the work being done by the players. We have two types of messages:

**Discovery:** this informs ASI when the agent becomes aware of needed activity<br>

**Update:** this informs the ASI when updates to the status of known activity occur. These updates include:
   - Awareness: who knows about it and when
   - Addressing: who is working on it, when and for how long
   - Completion: who completed it and at what time  

This AC provides a framework of templates for joint activity in the SAR domain (JAGs). These are used to generate instances
based on what player's experience during the trial. The state of the instances can be used to infer what players are likely to do next.

### Message bus format

See [JointActivityInterdependence](../../MessageSpecs/JointActivityInterdependence) message spec

### Frequency of measurement

Event-based publishing occurs as trial unfolds.

### How ASI agents can generate assessments from measures

This AC provides information about the number of "things" known to each agent. As a metaphor, it is like the list of items 
on the player's todo list. One way to an assessment is to consider how many things the player has to do based on what they
should know. More advanced assessments could also track the time to complete those items against the time remaining in the
trial.

Since this AC provides the information tailored to what each individual experiences, the ASI will have an idea about the
difference between what one player knows about what needs to be done, compared to what another player knows needs to be done.
This difference can be used, for example, to understand why one player may not be helping another.

This AC also provides tracking on who is working on what tasks. This provides the foundation for tracking how coordinated
joint activity is proceeding. This can be used to track how long tasks are taking and how efficiently work is getting done.
Specifically, we can track the amount of time that is taken for a particular set of activities. 

Based on the tracking of time within elements of the activity, this AC can provide an assessment of hinderance time. This
is the amount of time a player is blocked by a sequential interdependence on another player. We can also what players do 
with the time when they are blocked (e.g., waiting, or moving to another task). We also can measure the amount of time a 
player takes performing an activity which can inform ASIs about player competence. 

## Developing locally

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

## Questions
Questions should be directed to Roger Carff on the ASIST Slack Channel.