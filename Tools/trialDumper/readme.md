# replayer

## Introduction

This tool is used to replay data from the ELK container back onto the message bus.  
The replayer tool takes a trial_id or replay_id and queries the elastic datastore for that dataset.
You can replay a trial or another replay by specifying either a trial_id or a replay_id.
In either case, the source of the replay is recorded in the new message generated as either the trial or another replay.  
It then gathers all of those records and publishes them on the message bus in message time order
on the same topic they were originally published on. 
All of the re-published data, along with any new data that any responding agents publish is all saved in elastic.
Any message bus agent that publishes data should replicate the trial_id and replay_id (if any) and replay_root_id (if any) of the messages they are receiving
so that the published messages are stored in elastic with the correct ids.

To gather the set of available trial_ids in the testbed, the replayer queries elastic (see the config file for the query).
When a trial starts, there is a control message that is sent out that contains the experiment id, the trial id and the experiment_name.
When a replay is done, the same control message(s) from the original trial will be published,
the only different is that they will contain a replay_id.
You can replay a trial multiple times and each one would get the same trial_id but a different replay_id.
There is an option to not re-publish any messages published to a list of topics that are defined in the config.ini file. 
The purpose of this tool is to dump a trial from elastic to a json file.

This tool runs as a python program on either the machine that is running the testbed, or a machine that
has access to the testbed.

To use the tool, follow these steps:
- start up the ELK container.  
- navigate to the trialDumper directory
- edit the config.ini file
  - edit the host if you are on a linux machine
  - edit the index.  This is the elastic index and not the kibana index pattern
  - edit filter_out_users if necessary.  This will remove most of the messages from this users. 
    This would commonly be used to filter out observers that you don't want in the dump
  - edit the trial_id to the UUID of the trial you want to dump.  This can also be specified on the command line
- You can run the replay tool from the command line using python


## Running the trialDumper from the command line
- Navigate to the Tools/trialDumper directory
- Edit the config.ini file
- run `python trialDumper <options>`

## Notes
- The trialDumper tool has several options use -h or --help to see them.

