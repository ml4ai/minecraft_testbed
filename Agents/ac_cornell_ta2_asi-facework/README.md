# Cornell ASI Facework AC Agent

This AC is based on the social concept of facework. For effective intervention, the players must trust the ASI agents. We employ facework to inform intervention strategies to the ASI agents. This AC is a stretch goal for us and requires significant inputs from TA1s about their intervention space and past compliance to suggestions. Facework is a set of strategic behaviors by which people attempt to maintain both their own dignity (face) and that of the people with whom they are dealing. Facework strategies include politeness, deference, tact, avoidance of conflict, etc. People are generally careful not to diminish their face and the face of others (mutual face).


This exploratory AC aims to provide an additional component to consider in deciding on an intervention: whether the intervention may be a face-threat for the participants or not. 
This AC will heavily depend on the past “performance/compliance measure” of intervention types and  each player’s sub-goals inferred by the ASI.
ASIs are expected to provide these intervention performance metrics and player’s sub-goals in order to use our AC.

Based on past work, we assume that an intervention is face-threatening if the same type of intervention has recently been suggested, and if the same type of intervention was likely rejected in the past. We separate different intervention types based on Mathieu *et al*.'s taxonomy as well as the alignment of inferred goal of the player and the proposed goal of the intervention. Hence, we consider recent repeated instances and compliance/performance rate for each intervention type, and we output “Yes”/”No” based on the possibility of face-threat for each intervention type at some interval or when there is a new event (e.g. compliance rate update, goal inference update etc.)


The first iteration of this AC follows a simple logic:
> Compliance Rate * Recency(1-1/n) > threshold ? YES : NO 
where *n* counts back the most recent instance of the same intervention type and compliance rate is a culmulative average (for now) for such type.



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

