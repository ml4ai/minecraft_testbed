#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
PyFoVAgent QC Script

This script performs quality checking on metadata files expected to contain
PyGLFoV messages.  Specifically, the script checks for and reports on the
following:

* Total number of PlayerState and FoV messages in the metadata file
* Time range (in mission time) that FoV messages were generated
* Number of FoV messages by player
* Statistics on latency between PlayerState and FoV messages
* Time delta between subsequent FoV messages by player

At the moment, the results are simply printed to stdout.


Usage
-----
python qc_pyglfov.py <inputfile>
"""

import sys
import json

import statistics

from dateutil.parser import isoparse

from collections import defaultdict


# TOPICS OF INTEREST
PLAYER_STATE_TOPIC = "observations/state"
FOV_TOPIC = "agent/pygl_fov/player/3d/summary"


def load_messages_from_metadata(filename, topics = [PLAYER_STATE_TOPIC,
	                                                FOV_TOPIC]):
	"""
	Loads and parses messages from the provided file, extracting a dictionary
	mapping the topics of interest to lists of messages.

	Arguments
	---------
	filename : string
		Path to metadata file
	topics : list
		Lists of topics of interest
	"""

	# Try to load the file
	with open(filename) as json_file:
		json_data = [json.loads(line) for line in json_file.readlines()]

	messages = { topic: [line for line in json_data if "topic" in line and line["topic"] == topic] for topic in topics }

	return messages


def get_player_state_fov_correspondences(player_state_messages, fov_messages):
	"""
	Get a list of tuples of PlayerState and corresponding FoV messages (by
	observation number).  List will be sorted from earliest to latest
	observation number.

	Arguments
	---------
	player_state_messages : list
		List of PlayerState messages
	fov_messages : list
		List of PyGLFoV messages
	"""

	# Create dictionaries mapping observation numbers to messages
	player_state_dictionary = { message["data"]["observation_number"]: message
	                            for message in player_state_messages }
	fov_message_dictionary = { message["data"]["observation"]: message
	                           for message in fov_messages }

	# What is the intersection of observation numbers?
	observation_numbers = [ number for number in player_state_dictionary.keys()
	                        if number in fov_message_dictionary.keys() ]
	observation_numbers.sort()

	# Generate a list of tuples for each shared observation number and return
	return [ (player_state_dictionary[observation], fov_message_dictionary[observation])
	         for observation in observation_numbers ]


def get_timestamp_difference(correspondences):
	"""
	Determine the amount of wall-clock time between a PlayerState observation 
	and FoV	message, based on the message timestamps.

	Arguments
	---------
	correspondences : list
		List of PlayerState / FoV message pairs

	Returns
	-------
	List of time (in seconds) between the PlayerState and FoV message
	"""

	differences = [ isoparse(correspondence[1]['msg']['timestamp']) - 
	                isoparse(correspondence[0]['msg']['timestamp'])
	                for correspondence in correspondences ]

	return [ difference.total_seconds() for difference in differences ]


def get_minimum_and_maximum_mission_time(correspondences):
	"""
	Determine the minimum and maximum mission time (elapsed_milliseconds and
	mission_timer) in the correspondences.

	Arguments
	---------
	correspondences : list
		List of PlayerState / FoV message pairs

	Returns
	-------
	minimum_elapsed_milliseconds, 
	maximum_elapsed_milliseconds, 
	earliest_mission_timer, 
	latest_mission_timer
	"""

	minimum_elapsed_milliseconds = correspondences[0][0]['data']['elapsed_milliseconds']
	maximum_elapsed_milliseconds = correspondences[-1][0]['data']['elapsed_milliseconds']

	earliest_mission_timer = correspondences[0][0]['data']['mission_timer']
	latest_mission_timer = correspondences[-1][0]['data']['mission_timer']

	return minimum_elapsed_milliseconds,maximum_elapsed_milliseconds, earliest_mission_timer, latest_mission_timer


def get_latency_by_timestamp(correspondences, timestamp="elastic"):
	"""
	Determine the minimum, maximum, average, and std-dev of the latency between
	the PlayerState and FoV messages

	Arguments
	---------
	correspondences : list
		List of PlayerState / FoV message pairs
	timestamp : string, enum
		"elastic" - get latency by "@timestamp"
		"header" - get latency by "header.timestamp"
		"msg" - get latency by "msg.timestamp"

	Returns
	-------
	minimum_latency
	maximum_latency
	average_latency
	std_dev of latency
	"""

	if timestamp not in {"elastic","header","msg"}:
		print(f"ERROR:  `timestamp` argument not valid: {timestamp}")
		return

	if timestamp == "elastic":
		player_state_timestamps = [c[0]['@timestamp'] for c in correspondences if '@timestamp' in c[0]]
		fov_timestamps = [c[1]['@timestamp'] for c in correspondences if '@timestamp' in c[1]]
	else:
		player_state_timestamps = [c[0][timestamp]['timestamp'] for c in correspondences]
		fov_timestamps = [c[1][timestamp]['timestamp'] for c in correspondences]

	timestamps = zip(player_state_timestamps, fov_timestamps)

	differences = [ (isoparse(t[1]) - isoparse(t[0])).total_seconds() for t in timestamps ]

	# Can't calculate statistics with no numbers!
	if len(differences) == 0:
		return (-1, -1, -1, -1)

	return (min(differences), max(differences), statistics.mean(differences), statistics.stdev(differences))


def get_playernames(fov_messages):
	"""
	Return the set of playernames in the provided FoV messages

	Arguments
	---------
	fov_messages : list
		List of FoV messages

	Returns
	-------
	playernames : set
		set of playernames in the FoV messages
	"""

	return set([m['data']['playername'] for m in fov_messages])


def get_fov_message_delta_by_player(fov_messages, playername, timestamp):
	"""
	Get the minimum, maximum, average, and std-dev of the time difference 
	between FoV messages for the given playername.

	Arguments
	---------
	correspondences : list
		List of PlayerState / FoV message pairs
	playername : string
		Playername to consider
	timestamp : string
		Enum of which timestamp to use ("elastic", "header", "msg")

	Return
	------
	minimum_time_delta
	maximum_time_delta
	average_time_delta
	std_dev_time_delta
	"""

	player_fov_messages = [ m for m in fov_messages if m["data"]["playername"] == playername ]

	# Get the desired timestamps from the messages
	if timestamp not in {"elastic","header","msg"}:
		print(f"ERROR:  `timestamp` argument not valid: {timestamp}")
		return

	if timestamp == "elastic":
		timestamps = [m['@timestamp'] for m in player_fov_messages if '@timestamp' in m]
	else:
		timestamps = [m[timestamp]['timestamp'] for m in player_fov_messages]

	timestamps = [isoparse(t) for t in timestamps]

	# Sort the timestamps and calculate the difference between subsequent messages
	timestamps.sort()
	deltas = [(timestamps[t] - timestamps[t-1]).total_seconds() for t in range(1,len(timestamps)-1)]

	if len(deltas) == 0:
		return (-1, -1, -1, -1)

	return (min(deltas), max(deltas), statistics.mean(deltas), statistics.stdev(deltas))



def get_FoV_count_by_player(fov_messages):
	"""
	Calculate the number of FoV messages generated per player
	"""

	count_dict = defaultdict(lambda: 0)

	for message in fov_messages:
		player = message['data']['playername']
		count_dict[player] += 1

	return count_dict


def report(filename):
	"""
	Print out a QC report for the provided file
	"""

	messages = load_messages_from_metadata(filename)

	print("PyGLFoV QC Report")
	print("=================")

	print("Total number of messages:")
	print("-------------------------")
	print(f"  PlayerState:  {len(messages[PLAYER_STATE_TOPIC])}")
	print(f"  PyGLFoVAgent: {len(messages[FOV_TOPIC])}")
	print()


	correspondences = get_player_state_fov_correspondences(messages[PLAYER_STATE_TOPIC], messages[FOV_TOPIC])

	if len(correspondences) == 0:
		print("No correspondences detected between PlayerState and PyGLFoV messages")
		return


	print("FoV Message Time Range")
	print("----------------------")

	min_ms, max_ms, earliest_mt, latest_mt = get_minimum_and_maximum_mission_time(correspondences)

	print(f"  Earliest Mission Timer: [{earliest_mt}] ({min_ms} milliseconds)")
	print(f"  Latest Mission Timer:   [{latest_mt}] ({max_ms} milliseconds)")
	print()


	print("Number of FoV Messages by Player:")
	print("---------------------------------")

	count_dict = get_FoV_count_by_player(messages[FOV_TOPIC])

	for playername, count in count_dict.items():

		print(f"  {playername}: {count}")

	print()


	print("PlayerState-FoV Message Latency:")
	print("--------------------------------")

	print("  by @timestamp:")
	min_latency, max_latency, mean_latency, stdev_latency = get_latency_by_timestamp(correspondences, "elastic")
	print(f"    Min:     {min_latency}")
	print(f"    Max:     {max_latency}")
	print(f"    Mean:    {mean_latency}")
	print(f"    Std-Dev: {stdev_latency}")

	print("  by header.timestamp:")
	min_latency, max_latency, mean_latency, stdev_latency = get_latency_by_timestamp(correspondences, "header")
	print(f"    Min:     {min_latency}")
	print(f"    Max:     {max_latency}")
	print(f"    Mean:    {mean_latency}")
	print(f"    Std-Dev: {stdev_latency}")

	print("  by msg.timestamp:")
	min_latency, max_latency, mean_latency, stdev_latency = get_latency_by_timestamp(correspondences, "msg")
	print(f"    Min:     {min_latency}")
	print(f"    Max:     {max_latency}")
	print(f"    Mean:    {mean_latency}")
	print(f"    Std-Dev: {stdev_latency}")
	print()


	print("FoV Timestamp Difference by Player:")
	print("-----------------------------------")

	# Want to ignore the first FoV message, since that usually has a very high
	# latency associated with loading the base map
	fov_messages = [c[1] for c in correspondences]

	for playername in get_playernames(messages[FOV_TOPIC]):
		print(f"  {playername}:")
		print(f"    by @timestamp:")
		min_delta, max_delta, mean_delta, stdev_delta = get_fov_message_delta_by_player(messages[FOV_TOPIC], playername, "elastic")
		print(f"      Min:     {min_delta}")
		print(f"      Max:     {max_delta}")
		print(f"      Mean:    {mean_delta}")
		print(f"      Std-Dev: {stdev_delta}")

		print(f"    by header.timestamp:")
		min_delta, max_delta, mean_delta, stdev_delta = get_fov_message_delta_by_player(messages[FOV_TOPIC], playername, "header")
		print(f"      Min:     {min_delta}")
		print(f"      Max:     {max_delta}")
		print(f"      Mean:    {mean_delta}")
		print(f"      Std-Dev: {stdev_delta}")

		print(f"    by msg.timestamp:")
		min_delta, max_delta, mean_delta, stdev_delta = get_fov_message_delta_by_player(messages[FOV_TOPIC], playername, "msg")
		print(f"      Min:     {min_delta}")
		print(f"      Max:     {max_delta}")
		print(f"      Mean:    {mean_delta}")
		print(f"      Std-Dev: {stdev_delta}")		




if __name__ == '__main__':

	# Check to see if a file was given, and exit if not
	if len(sys.argv) != 2:
		print("USAGE: python qc_pyglfov.py <input_filename>")
		sys.exit(1)

	# Run the report
	report(sys.argv[1])