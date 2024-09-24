Testing for ASIST agents

## Overview
Simple extensible testing framework for ASIST agents

## Usage
> test_agents.sh config.json

## Components

# config.json
This describes the set of tests to be run. Each entry in the config file is for a separate test run. 
For each test, you must specify the following: 
- agent_names: the agent or agents to be run
- agent_directories: the directory in which each agent lives, usually testbed/Agents/*
- trial_file: the location of the ground-truth trial file to be replayed - should be found in ./data/{AgentName}
- test_messages: the list of messages to be tested by comparator files, usually all messages produced by the agent or agents
- ignore_messages: the list of messages to be ignored by the replayer, this should at minimum include all of the messages to be tested
- comparators: the list of comparator files to run on your trial and replay

# test_agents.sh
Main test script. It reads through the config file, runs a replay with the specified trial file, exports the replay, and executes each test.

# trials directory
Contains named subdirectories for each agent, each containing a trial file to be run

# comparators directory
Contains Python files and shell scripts which can be run as part of tests. Comparators must expect the following three arguments, even if they are not all used:
- trial_file: the trial file specified in the config entry
- replay_file: the replay file generated from the trial file
- messages: test_messages from the the config entry
Comparators write test results to stdout as well as to a log file in ./data/{AgentName}/logs
