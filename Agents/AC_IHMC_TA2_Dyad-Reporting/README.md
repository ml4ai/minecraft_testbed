# IHMC Dyad AC Agent

The IHMC Dyad Agent AC is based off the IHMC Python Starter Agent.  It computes
participant dyads by using proximity events and looking at the distance between
players.

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

## Questions
Questions should be directed to Roger Carff on the ASIST Slack Channel.

## Observables (Subscribed Topics)
- [**agent/control/rollcall/request**](https://gitlab.com/artificialsocialintelligence/study3/-/tree/main//MessageSpecs/Agent/rollcall/agent_rollcall.md)
  - Used to know when to publish a rollcall response
- [**trial**](https://gitlab.com/artificialsocialintelligence/study3/-/tree/main//MessageSpecs/Trial/trial.md)
  - Used to retain experiment and trial ids and associated participant ids and call signs for publish events and to know which map is being used in the trial.
- [**observations/events/player/proximity**](https://gitlab.com/artificialsocialintelligence/study3/-/tree/main//MessageSpecs/Proximity/proximity_event_message.md)
  - Proximity messages are used to know the distance between each participant.
## Measurements (Published Topics)
- [**agent/control/rollcall/response**](https://gitlab.com/artificialsocialintelligence/study3/-/tree/main//MessageSpecs/Agent/rollcall/agent_rollcall.md)
  - Published whenever an **agent/control/rollcall/request** message is received.
- [**agent/AC_IHMC_TA2_Location-Monitor/versioninfo**](https://gitlab.com/artificialsocialintelligence/study3/-/tree/main//MessageSpecs/Agent/versioninfo/agent_versioninfo.md)
  - Published at start of trial.
- [**status/AC_IHMC_TA2_Location-Monitor/heartbeats**](https://gitlab.com/artificialsocialintelligence/study3/-/tree/main//MessageSpecs/Status/status.md)
  - Published at a frequency which is defined in the config.json file.  (Default is every 10 seconds.)
- [**observations/events/player/dyad**](https://gitlab.com/artificialsocialintelligence/study3/-/tree/main//MessageSpecs/Proximity/dyad_event_message.md)
  - Published when participants `start`/`end` dyadic behavior and when the probability of being in a dyad changes (`update`).
  - The `dyad_ranges` config file property determines the probability of participants being in a dyad.
  - A probability of 1.0 means that the agent is positive that the participants listed in the event are in a dyad.  A value of 0.0 means that they are not in a dyad.
