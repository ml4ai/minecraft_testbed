# ASIST atomic agent

The ASIST atomic agent generates a knowledge structure that tracks the information players acquire throughout a mission
 
## Building and Running The Agent with `./agent.sh` and `./agent.cmd`

   ./agent.sh build
`build` will build the docker image for your agent.

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

## other agents needed (for running psychsim atomic agent)
- AC_IHMC_TA2_Joint-Activity-Interdependence
- ac_cornell_ta2_teamtrust
- gallup_agent_gelp
- *to switch to the knowledge structure tracker version of the agent mv the kstruct_src directory to replace the default src directory before building the agent*


## 