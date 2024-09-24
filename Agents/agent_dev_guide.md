# ASIST Agent development Guide
This document describes the characteristics of a "good citizen" agent in the ASIST testbed.

## Overview
The ASIST testbed supports the integration of agents to extend the
functionality of the testbed.

Agents are integrated into the testbed using the testbed message bus to recieve and send information using a publish/subscribe paradigm.
These testbed message bus agents should follow a set of conventions in order to cooperate fully with the ASIST testbed and other agents.

## Agent Architecture

All agents will be containerized to work in a Docker environment.
Each agent will include script commands to build them, start them up, and take them down in the Docker environment along with the other containers of the testbed.

## Agent container networking

Some agents might be composed of multiple containers that communicate with each
other rather than via the message bus. If you are developing such an agent,
please document the ports that you are using, for the following reasons.

- If the ports are not exposed to the host (this should ideally be the
  default), then those ports can only be accessed by other containers on the
  same network (`asist_net`). If other performer teams wish to use ports for
  communicating between their containers, this documentation will prevent
  clashes.
- If the ports are exposed to the host, then those ports might be in use by
  another service running on the host machine, resulting in clashes.
  Documenting the ports used by your agent will help diagnose potential issues
  arising from those clashes.

### Ports that are currently in use by agents

## Agent Deployment

There are two ways to deploy a agent into the testbed environment so that it is included with the testbed distributions.

### Source deployment in Gitlab
- 
- An agent can be deployed by committing the source code into the ASIST Gitlab repository and
 controlling it via the testbed_build, testbed_up and testbed_down scripts for Linux, WIndows and Mac.
- The Gitlab software repository is located at: [Gitlab software repository](https://gitlab.com/artificialsocialintelligence/study3/)
- When the testbed from the repository is cloned or pulled, all of the components for the agent should be provided and
 the agent should be built, started up and taken down with tthe testbed scripts along with all of the other testbed components/containers.
- Each agent should be stored in a subdirectory to the Agents directory of the software repository.
- Developers should create a gitlab branch for their agent to do the development and testing work.
 After the agent is tested and ready to deploy for integration testing with other agents,
 you should submit a merge request to GitLab to merge their agent branch into the develop branch

### Container in the Registry

- Agents can be deployed with the testbed by placing a built container for the agent into the Gitlab container registry.
- The container registry is located at: [Gitlab container registry](https://gitlab.com/artificialsocialintelligence/study3/container_registry)
- Each update of the container in the registry should be tagged with a unique version number.  The latest version will not automatically be pulled
- A directory for the agent should be created in the Agents directory in the software repository to
 contain the docker and/or docker-compose files that are needed to deploy your container(s).
- Your agent directory should also contain any scripts needs to build, start up and take down your container(s).
 The scripts should reference the specific version(s) of the docker images which should be included in the agent distribution.

## Agent Implementation

See the [reference agent(s) in the ASIST source code repository](https://gitlab.com/artificialsocialintelligence/study3/-/tree/main/ReferenceAgents)
 for examples of testbed message bus agents.
 
### Languages

Agents can be developed in a large number of languages.  The main requirements is that there is MQTT message bus support for that language.
The Eclipse paho project ([paho project](https://www.eclipse.org/paho/)) provides open source MQTT clients
 for many languages including: C, C++, Java, Python, JavaScript, Go, Rust, C#

### Message Bus Agent Processing steps

A message bus agent would generally go through these processing steps:

  - Start up within a Docker container and configure
  - Connect to MQTT the message bus
  - publish an agent version message whenever a trial start message is received.
   This agent versioninfo message announces that the agent is running and identifes the version of the agent and other relevant agent information.
  - Subscribe to messages from the topic(s) of interest
  - Perform some action/computation based on messages received
  - Publish the results on the message bus
  - Check for exceptions and handle them so the agent doesn't crash
  - Automaticaly restart the agent if it does crash, taking care of any state/context that is needed to do a restart of the agent.

### Testbed released agents

If the agent is to be registered and released with the testbed it should follow these steps:

 - have a discussion with the Testbed working group on the name and function of the agent
 - In a branch, create a directory for the agent, with a unique name as a subdirectory
 in the `Agents` directory in the source repository.
 Depending on if the agent is being deployed via source [Source] or built container [Built] that directory should contain:
   - [Source and Built] README.md file with a description of the agent and instructions on how to build and run the agent
   - [Source only] build.cmd and build.sh for Windows and Linux/Mac container building
   - [Source and Built] up.cmd and up.sh for Windows and Linux/Mac container startup
   - [Source and Built] down.cmd and down.sh for Windows and Linux/Mac container shutdown
   - [Source] docker-compose.yml or dockerfile to build the docker container
   - [Source and Built as needed] config folder with config file in either .json or .ini format
   - [Source] source code
   - [Source and Built] Any other components/files necessary to run the agent.
     Components that can be gathered from the Internet to build the container do not need to be in the repository.
   - [Source and Built] add the agent name to the agent list in MessageSpecs/Agent/agent_names.md file
   - [Source and Built] For ASI agents, add a section to the
     `Local/MalmoControl/appsettings.Production.json` file to enable your
     agent to be launched from the experiment control web app.

### Agent Configuration

Agents do not have a user interface to gather input from the experimenter or the subject (except as defined by messages).
Therefore any configuration or parameters that the agent needs should be build into:
 the source code, configuration file, the start up script, docker file, etc.

### Agent Naming

Agents should be named using the following convention.  This applies to the container name as well as the name of the agent or analytic component used when publishing messageson the message bus (such as the source field).
The agent or analytic component name should be compose of the following parts:
-	Agent type [ASI | AC | Other]
-	Owner organization.  e.g. DOLL
-	TA e.g. [TA1 | TA2 ]
-	Agent name

Components are separated by underscore and each component can not contain underscore.
Examples:
- ASI_DOLL_TA1_RITA
- AC_IHMC_TA2_location-monitor 


## Agent Messages

All of the messages that are published on the message bus are documented in the [MessageSpecs directory](https://gitlab.com/artificialsocialintelligence/study3/-/tree/main/MessageSpecs) in Gitlab. Any results the agent generates and wants to share with other agents or wants to be collected in elastic should be documented in the MessageSpecs directory and published to the message bus. Any published message should be vetted with the Testbed working group.
Agents should first attempt to use already defined messages or develop generalized messages to be shared with other agents before defining special purpose messages.
Each message should have the following:

 - a subdirectory in the MessageSpecs directory with the name of the message
 - for each message new type there should be 2 files.
   - .md file with documentation of each field and an example or two See other messages for the format of this documentation.
   - .json file with the json schema definition of the format of the message.
     see the other messages in the MessageSpec directory for examples or look at [json schema](https://json-schema.org/)
 - all message should have at least a header and msg section.  Most messages will also have a data section with the detailed content of the message
   - the header section must contain the standard fields of timestamp, message_type and version.
     You can use the standard header definition in common_header.json
   - the msg section must contain: experiment_id, trial_id, timestamp, source, sub_type, version and optionally replay_parent_type, replay_parent_id and replay_id.
     You can use the standard msg definition in common_message.json
   - the data section can have any agent relevant data that is required.
     This format should be uniquely identified by the sub_type in the msg section.
 - Every message type should be assigned an MQTT topic.  Related message type groups can be assigned the same topic.
    Message topic assignment should also be vetted through the Testbed Working Group.
 - Each message type should be added to the MessageSpecs/message_topics.csv file.
    This file drives the message validation and associates a message type and topic with a json schema file for realtime message validation.

## Agent Integration and Testing

Agents should be developed and tested on a local instance of the testbed before committing and merging into the Gitlab repo.

The testbed repository will be using CI (Continuous Integration) to test all of the components of the testbed.

When software changes are committed to the develop and master branches of the repository,
 a script will be run to do basic checking of the components in that version.
The agent developer(s) are responsible for providing at least 1 test case for the testing of their agent.

An agent testcase is a run of the testbed with the agent started up and the running of a trial which exercises the agent in a meaningful way.

1. The set of messages (both from the other components of the testbed and from the agent under test are exported into a .metadata file using the Export dashboard.

This .metadata file will then we used to replay the trial and capture the set of messages from the agent being tested.

  The known-good output and the test run will be compared to determine if the agent is working.

  The outputs may not be exact based on the methods being used by the agent to generate results messages.

## Agent Memory and Learning
Agent memory and learning across experiments is not currently supported.
  This means that any models, learning, information content that the agent needs should be packaged into the container.
  That container will be reset at the beginning of each experiment.  NOTE: the experiment contains 2 trials which the agent will be able to learn across.

## Agent Discovery and Status
All agents or analytic components will publish a [versioninfo message](https://gitlab.com/artificialsocialintelligence/study3/-/tree/main//MessageSpecs/Agent/versioninfo/agent_versioninfo.md) when they receive a trial start message.
  This will provide a basic inventory of what agents and analytic components are running at the start of the trial.

These are the messages an agent or analytic component should provide for the testbed to monitor the health of the agent or analytic component and to record their health in the dataset:

 - All agents and analytic components should publish a heartbeat message every 10 seconds that indicates that they are running. See [heartbeat message](https://gitlab.com/artificialsocialintelligence/study3/-/tree/main//MessageSpecs/Status/status.md) for message details.  The testbed will monitor agents.  A heartbeat message with a "state" of "ok" indicates that the agent is functioning properly
 - All agents and analytic components should implement a "Rollcall" message response.
 The testbed will periodically publishes a message asking who is alive and any component that is alive should respond with a rollcall response message.
 The rollcall response message documentation can be found [here](https://gitlab.com/artificialsocialintelligence/study3/-/tree/main//MessageSpecs/Agent/rollcall/agent_rollcall.md)
 - [Potential Future Feature]The testbed can upon request re-publish the trial message which gives information about the trial.  This would be important if agents join (or restart) in the middle of the trial.
 - All agents and analytic components should publish a versioninfo message when the trial ends so that the data contains a record that the agent was running when the trial ended.
 The documentation for the versioninfo message can be found [here](https://gitlab.com/artificialsocialintelligence/study3/-/tree/main//MessageSpecs/Agent/versioninfo/agent_versioninfo.md)

 ### Sequence diagram for normal agent lifecycle operation
 
 ```mermaid
sequenceDiagram
autonumber
participant Testbed
participant Agent
    Testbed-)Agent: [Future]header.message_type:"control",msg.sub_type:"agent:init"
    Note over Testbed,Agent: Agent should initialize
    activate Agent
    Testbed-)Agent: [Future]header.message_type:"control",msg.sub_type:"agent:start"
    Note over Testbed,Agent: Agent should start
    Testbed-)Agent: header.message_type:"trial",msg.sub_type:"start"
    Note over Testbed,Agent: Trial is starting
    Agent-)Testbed: header.message_type:"agent",msg.sub_type:"versioninfo"
    loop Every 10 seconds until trial stop
        Agent--)Testbed: header.message_type:"status",msg.sub_type:"heartbeat"
    end
    Testbed-)Agent: header.message_type:"event",msg.sub_type:"Event:MissionState",data.mission_state:"start"
    Note over Testbed,Agent: Mission starting
    opt Rollcall request
      Testbed-)Agent: header.message_type:"agent",msg.sub_type:"rollcall:request"
      Agent-)Testbed: header.message_type:"agent",msg.sub_type:"rollcall:response"
    end
    Testbed-)Agent: header.message_type:"event",msg.sub_type:"Event:MissionState",data.mission_state:"stop"
    Note over Testbed,Agent: Mission stopped
    Testbed-)Agent: header.message_type:"trial",msg.sub_type:"stop"
    Note over Testbed,Agent: Trial is stopped
  deactivate Agent
```

### Sequence diagram for agent failure operation [Future]

 ```mermaid
sequenceDiagram
autonumber
participant Testbed
participant Agent
Note over Testbed,Agent: Agent failed
opt Agent fails
  Agent-)Testbed: [Agent failed message]
end
Note over Testbed,Agent: Agent restarts itself
Agent-)Testbed: [Agent requests current state]
alt If a trial is active
  Testbed-)Agent: [trial state information]
  Testbed-)Agent: [If mission started: mission state information]
else
  Testbed-)Agent: [No Trial active message]
end
Testbed-)Agent: [Current state information]
```
