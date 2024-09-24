# replayer

## Introduction

This tool is used to replay data from the ELK container back onto the message bus.
The replayer tool takes a trial_id or replay_id and queries the elastic datastore for that dataset.
You can replay a trial or another replay by specifying either a trial_id or a replay_id.
In either case, the source of the replay is recorded in the new message generated as either the trial or another replay.
It then gathers all of those records and publishes them on the message bus in message time order
on the same topic they were originally published on.
All of the re-published data, along with any new data that any responding agents publish is all saved in elastic.
Any message bus agent that publishes data should replicate the trial_id and replay_id (if any) and replay_parent_id (if any) of the messages they are receiving
so that the published messages are stored in elastic with the correct ids.

To gather the set of available trial_ids in the testbed, the replayer queries elastic (see the config file for the query).
When a trial starts, there is a control message that is sent out that contains the experiment id, the trial id and the experiment_name.
When a replay is done, the same control message(s) from the original trial will be published,
the only different is that they will contain a replay_id.
You can replay a trial multiple times and each one would get the same trial_id but a different replay_id.
There is an option to not re-publish any messages published to a list of topics that are defined in the config.ini file.
The intention of this is to allow developers to test and debug their message bus agents, over multiple replays,
they can compare messages with the multiple replay ids to see what changed.

To use the tool, follow these steps:
- start up the ELK container.  You can also start up everything using the
  Local/testbed_up script and then ^c which will just shut down the Minecraft containers
  leaving the rest of the containers still running.
- navigate to the replayer directory
- edit the config.ini file
- You can run the replay tool either using docker or directly from the command line
  - Using Docker
    - build the replayer container using the instructions below.
    - run the replayer container using the instructions below
  - replay tool can be run directly from python

## Building the docker container
- Navigate to the Tools/replayer directory
- On Windows run docker_replay_build.bat
- On other OSs run: `docker build -t replayer .`

## Updating docker container after a new release
- use the same instructions as Building the docker container above

## Configuration
- To use the replayer, you should only start the ELK container and the replay container (if using the docker approach),
  plus any other agent containers that you want to participate in the replay.
  You should not start up the Minecraft/Malmo container
- the config.ini file must be updated BEFORE the docker build is done.
  The config.ini file contains all of the information for the replayer to connect to the ELK container,
  query elasticsearch and connect to the mqtt broker (also running in the ELK container).
  The replayer command line will accept options and override the elastic index specified in the config.ini file
- the released config.ini file should work where the ELK container and the replayer container are both running on the same machine
- To setup a replay, the config.ini file will require the following edits
  - Set the host and port properties for both ELASTIC and MQTT.
    If you are running everything locally from the command line you should uncomment the ELASTIC and MQTT properties for localhost.
  - Set the index property to the index in Elastic that contains the source data that is to be replayed.
  - You can get a list of trial_ids and the replay_id(s) that go with them using the -gt option on the replayer tool
  - The output to a file capability has been removed.  If you want to get a file of the data, use the export tool.

## Running the replayer with docker
- Navigate to the Tools/replayers/replayer directory
- Edit the config.ini file
- On Windows run docker_replay_up.bat
- On other OSs run: `docker run replayer`

## Running the replay from the command line
- Navigate to the Tools/replayers/replayer directory
- Edit the config.ini file
- run `python replayer <options>`

## Notes
- The replayer needs the UUID of the trial that you want to replay.
  You can use the -gt option with the replayer to get a list of the trial and replay ids in the elastic index in the .ini file.
  You can query elasticsearch to identify the UUID that you want to replay.
  The Control GUI also displays the trial id when you run an experiment.
  The export tool can list the trials that exist in an elasstic database.
- When you replay a trial, the replayer adds a new "replay_id" to the messages that are sent over the message bus.
  This can be used to identify that a given elasticsearch record is from either the original trial, or a replay of it.
- You can replay a trial multiple times.  Each time a trial is replayed, it will get a new replay_id, and keep the original trial_id.
- The replay will send the messages on the message bus as quickly as it can and
  doesn't try to space them out as in the original publishing of the messages.
  All of the messages will however contain their original timestamps which indicate when they were originally published and
  will be published in the same order they were originally published.
- when you replay a replay, the messages will contain a replay_parent_id which will be the parent replay_id and a new replay_id
- The replayer tool has several options use -h or --help to see them.
  This can be done either when running python directly or when running it via docker
