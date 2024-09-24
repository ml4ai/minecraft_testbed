# Name: firstlook compare
# Description: Tool in the ASIST testbed that gathers basic statistics for two trials from a .metadata files and
#  does a deep compare to find the differences.  The basic statistics are the counts for each message type and sub_type
#
# (c) Copyright 2021 Aptima Inc.

#Imports
import argparse
#import configparser
from datetime import datetime
from deepdiff import DeepDiff
#from dictdiffer import diff
from copy import deepcopy
import json
import pprint
import re
#import requests

import time
import uuid
from prettytable import PrettyTable
from prettytable import HEADER



#define and parse the command line arguments
def parse_command_line_args():
	parser = argparse.ArgumentParser(description='ASIST replayer tool')
	parser.add_argument('-f1','--file1', dest='file_spec_1', help='The first file to be compared')
	parser.add_argument('-f2','--file2', dest='file_spec_2', help='The second file to be compared')
	parser.add_argument('-o','--output', dest='output_spec', help='The output file spec')


	return parser.parse_args()

#process hits 
def process_hits(line, pub_cnt, nopub_cnt, message_type_cnts,trial_properties):
	global cmd_args
	# setup to check message times, if needed
	header_last_time = '1970-01-01T00:00:00.0000Z'
	msg_last_time = '1970-01-01T00:00:00.0000Z'
	#print(mqtt_client)

	obs = line
	#print(obs)
	json_obj = json.loads(line)
	#json_obj = obs
	#At some point we may also want to shut off the re-capture of the replayed data as an option.
	#add a date and time to the trial_id so that we have a new unique trial_id that will be saved in elastic.  

	message_type = json_obj["header"]["message_type"]
	if "sub_type" in json_obj["msg"]:
		message_sub_type = json_obj["msg"]["sub_type"]
	else:
		message_sub_type = "None"
	#print(message_type)

	pub_cnt+=1
	#count the message types and sub_types
	if message_type in message_type_cnts:
		#print('Add one to message_type {t}.'.format(t=message_type))
		if message_sub_type in message_type_cnts[message_type]:
			message_type_cnts[message_type][message_sub_type] += 1
		else:
			message_type_cnts[message_type][message_sub_type] = 1
	else:
		message_type_cnts[message_type] = {message_sub_type:1}

		#print('Init for message type {t}.'.format(t=message_type))
	# check for  trial message and pull out the properties
	if message_type == "trial" and message_sub_type == "start":
		trial_properties["trial_id"] = json_obj["msg"]["trial_id"]
		trial_properties["trial_date"] = json_obj["msg"]["timestamp"]
		trial_properties["data"] = json_obj["data"]

	#check for the error.data message and count them
	if "error" in json_obj:
		if "data" in json_obj["error"]:
			error_msg_type = "error" 
			error_msg_sub_type = message_type + "__" + message_sub_type
			if error_msg_type in message_type_cnts:
				if error_msg_sub_type in message_type_cnts[error_msg_type]:
					message_type_cnts[error_msg_type][error_msg_sub_type] += 1
				else:
					message_type_cnts[error_msg_type][error_msg_sub_type] = 1
			else:
				message_type_cnts[error_msg_type] = {error_msg_sub_type:1}
	#grab some dates for the export time and trial time
	if message_type == "export" and message_sub_type == "trial":
		trial_properties["export_date"] = json_obj["header"]["timestamp"]

	return (pub_cnt, nopub_cnt, message_type_cnts, trial_properties)


#print_or_write: print or write to a file the output
def print_or_write(s):
	if s == None:
		return
	if config["write_output_file"]:
		f_out.write("\n"+s)
	
	print(s)

pub_record_cnt = 0
nopub_record_cnt = 0
message_type_cnts = {}
trial_properties = {}
trial_cnt = 0
replay_cnt = 0
trial_list= {}


# main
pp = pprint.PrettyPrinter(indent=4)

config = {}

#get any command line arguments
cmd_args = parse_command_line_args()
#print(cmd_args)
#pp.pprint(cmd_args)

if cmd_args.file_spec_1 != None:
	config["file_spec_1"] = cmd_args.file_spec_1
if cmd_args.file_spec_2 != None:
	config["file_spec_2"] = cmd_args.file_spec_2
if cmd_args.output_spec != None:
	config["output_spec"] = cmd_args.output_spec
	config["write_output_file"] = True
else:
	config["write_output_file"] = False

#pp.pprint(config)


if config["write_output_file"]:
	f_out = open(config["output_spec"], "w+")
# process the first file
with open(config["file_spec_1"]) as f_in:
	for line in f_in:
		(pub_record_cnt, nopub_record_cnt, message_type_cnts, trial_properties) = process_hits(line,pub_record_cnt, nopub_record_cnt, message_type_cnts, trial_properties)
file_1_counts = deepcopy(message_type_cnts)
#print("First file counts\n")
#pp.pprint(file_1_counts)
# process the second fil
with open(config["file_spec_2"]) as f_in:
	for line in f_in:
		(pub_record_cnt, nopub_record_cnt, message_type_cnts, trial_properties) = process_hits(line,pub_record_cnt, nopub_record_cnt, message_type_cnts, trial_properties)
file_2_counts = deepcopy(message_type_cnts)
#print("Second file counts\n")
#pp.pprint(file_2_counts)

json_file_1 = json.dumps(file_1_counts, sort_keys=True)
json_file_2 = json.dumps(file_2_counts, sort_keys=True)
compared = json_file_1 == json_file_2
#print(compared)

#print("Deep Diff")
#print(type(file_1_counts))
#print(type(file_2_counts))
dd = DeepDiff(file_1_counts, file_2_counts, view="tree", ignore_order=True, report_repetition=True, verbose_level=2)
pp.pprint(dd.to_json())
#print("Get values changed")
#print(dd.get('values_changed',{}))
#pp.pprint(dd)
#for i in dd.to_dict().keys():
#	print(dd[i])
#print(list(diff(file_1_counts, file_2_counts)))
#print(dd.get_stats())
#print(dd == {})
exit(dd == {})
#print out summary in the format that the experimerters can use

print_or_write("Trial Summary")
print_or_write("Trial\t{trial_number}".format(trial_number=trial_properties["data"]["trial_number"]))
print_or_write("Team\t{team}".format(team=trial_properties["data"]["experiment_name"]))
for members in trial_properties["data"]["client_info"]:
	print_or_write("Member\t{member}".format(member=members["participant_id"]))

print_or_write("CondBtwn\t{condbtwn}".format(condbtwn=trial_properties["data"]["condition"]))
print_or_write("CondWin\t{condwin}".format(condwin=trial_properties["data"]["experiment_mission"]))


print_or_write("\nTotal {cnt} records".format(cnt=pub_record_cnt))

print_or_write('\nTrial Properties')
print_or_write(pp.pformat(trial_properties))
print_or_write("\nRecord counts")
print_or_write(pp.pformat(message_type_cnts))


# add a few checks to validate the entire dataset
print_or_write("\nValidation Check Results")
check_table = PrettyTable(["Msg Type","Msg Sub Type","Check", "Results"])
check_table.hrules=HEADER
# ---
# do we have at least one instance of each of these record types
# ---
if "event" in message_type_cnts and "Event:Door" in message_type_cnts["event"] and message_type_cnts["event"]["Event:Door"] >0 :
	result = "true"
else:
	result = "false"
check_table.add_row(["event","Event:Door","At least 1 door event exists", result])

if "event" in message_type_cnts and "Event:ItemEquipped" in message_type_cnts["event"] and message_type_cnts["event"]["Event:ItemEquipped"] >0 :
	result = "true"
else:
	result = "false"
check_table.add_row(["event","Event:ItemEquipped","At least 1 item equipped event found", result])

if "event" in message_type_cnts and "Event:MissionState" in message_type_cnts["event"] and message_type_cnts["event"]["Event:MissionState"] == 2 :
	result = "true"
else:
	result = "false"
check_table.add_row(["event","Event:MissionState","Exactly 2 MissionState events found", result])

if "event" in message_type_cnts and "Event:PlayerSwinging" in message_type_cnts["event"] and message_type_cnts["event"]["Event:PlayerSwinging"] > 0 :
	result = "true"
else:
	result = "false"
check_table.add_row(["event","Event:PlayerSwing","At least 1 PlayerSwinging event found", result])

if "event" in message_type_cnts and "Event:RoleSelected" in message_type_cnts["event"] and message_type_cnts["event"]["Event:RoleSelected"] > 0 :
	result = "true"
else:
	result = "false"
check_table.add_row(["event","Event:RoleSelected","At least 1 RoleSelected events found", result])

if "event" in message_type_cnts and "Event:RubbleDestroyed" in message_type_cnts["event"] and message_type_cnts["event"]["Event:RubbleDestroyed"] > 0 :
	result = "true"
else:
	result = "false"
check_table.add_row(["event","Event:RubbleDescroyed","At least 1 RubbleDestroyed events found", result])

if "event" in message_type_cnts and "Event:ToolDepleted" in message_type_cnts["event"] and message_type_cnts["event"]["Event:ToolDepleted"] > 0 :
	result = "true"
else:
	result = "false"
check_table.add_row(["event","Event:ToolDepleted","At least 1 ToolDepleted events found", result])

if "event" in message_type_cnts and "Event:ToolUsed" in message_type_cnts["event"] and message_type_cnts["event"]["Event:ToolUsed"] > 0 :
	result = "true"
else:
	result = "false"
check_table.add_row(["event","Event:ToolUsed","At least 1 ToolUsed events found", result])

if "event" in message_type_cnts and "Event:location" in message_type_cnts["event"] and message_type_cnts["event"]["Event:location"] > 0 :
	result = "true"
else:
	result = "false"
check_table.add_row(["event","Event:location","At least 1 location events found", result])

if "event" in message_type_cnts and "Event:ProximityBlockInteraction" in message_type_cnts["event"] and message_type_cnts["event"]["Event:ProximityBlockInteraction"] > 0 :
	result = "true"
else:
	result = "false"
check_table.add_row(["event","Event:ProximityBlockInteraction","At least 1 Proximity Block Interaction events found", result])

# there is an even number of triage events e.g. equal number of InProgress and Success or Failure
if "event" in message_type_cnts and "Event:Triage" in message_type_cnts["event"] and (message_type_cnts["event"]["Event:Triage"] % 2) == 0 :
	result = "true"
else:
	result = "false"
check_table.add_row(["event","Event:Triage","An even number of triage events found", result])

if "event" in message_type_cnts and "Event:VictimPickedUp" in message_type_cnts["event"] and message_type_cnts["event"]["Event:VictimPickedUp"] > 0 :
	result = "true"
else:
	result = "false"
check_table.add_row(["event","Event:VictimPickedUp","At least 1 VictimPickedUp events found", result])

if "event" in message_type_cnts and "Event:VictimPlaced" in message_type_cnts["event"] and message_type_cnts["event"]["Event:VictimPlaced"] > 0 :
	result = "true"
else:
	result = "false"
check_table.add_row(["event","Event:VictimPlaced","At least 1 VictimPlaced events found", result])

# check that there are an equal number of victim picked up and placed events
if "event" in message_type_cnts and "Event:VictimPickedUp" in message_type_cnts["event"] \
	and "Event:VictimPlaced" in message_type_cnts["event"] \
	and message_type_cnts["event"]["Event:VictimPickedUp"] == message_type_cnts["event"]["Event:VictimPlaced"]:
	result = "true"
else:
	result = "false"
check_table.add_row(["event","Event:VictimPickedUP,Event:VictimPlaced","An equal number of VictimPickedUp and VictimPlaced events found", result])

#Check if we have any dialogue messages
if "event" in message_type_cnts and "Event:dialogue_event" in message_type_cnts["event"] and message_type_cnts["event"]["Event:dialogue_event"] > 0 :
	result = "true"
else:
	result = "false"
check_table.add_row(["event","Event:dialogue_event","At least 1 Observation speech_analysis/dialogue message found", result])

if "groundtruth" in message_type_cnts and "Mission:BlockageList" in message_type_cnts["groundtruth"] and message_type_cnts["groundtruth"]["Mission:BlockageList"]== 1 :
	result = "true"
else:
	result = "false"
check_table.add_row(["groundTruth","Mission:BlockageList","There is exactly 1 groundtruth Mission:BlockageList event found", result])

if "groundtruth" in message_type_cnts and "Mission:VictimList" in message_type_cnts["groundtruth"] and message_type_cnts["groundtruth"]["Mission:VictimList"]== 1 :
	result = "true"
else:
	result = "false"
check_table.add_row(["groundtruth","Mission:VictimList","There is exactly 1 groundtruth Mission:VictimList event found", result])

if "groundtruth" in message_type_cnts and "Mission:FreezeBlockList" in message_type_cnts["groundtruth"] and message_type_cnts["groundtruth"]["Mission:FreezeBlockList"]== 1 :
	result = "true"
else:
	result = "false"
check_table.add_row(["groundtruth","Mission:FreezeBlockList","There is exactly 1 groundtruth Mission:FreezeBlockList event found", result])

if "groundtruth" in message_type_cnts and "Mission:ThreatSignList" in message_type_cnts["groundtruth"] and message_type_cnts["groundtruth"]["Mission:ThreatSignList"]== 1 :
	result = "true"
else:
	result = "false"
check_table.add_row(["groundtruth","Mission:ThreatSignList","There is exactly 1 groundtruth Mission:ThreatSignList event found", result])

if "groundtruth" in message_type_cnts and "measures" in message_type_cnts["groundtruth"] and message_type_cnts["groundtruth"]["measures"] > 0 :
	result = "true"
else:
	result = "false"
check_table.add_row(["groundtruth","measures","At least 1 groundtruth measures message found", result])

if "groundtruth" in message_type_cnts and "SemanticMap:Initialized" in message_type_cnts["groundtruth"] and message_type_cnts["groundtruth"]["SemanticMap:Initialized"]== 1 :
	result = "true"
else:
	result = "false"
check_table.add_row(["groundtruth","SemanticMap:Initialized","There is exactly 1 groundtruth SemanticMap Initialized event found", result])

if "observation" in message_type_cnts and "state" in message_type_cnts["observation"] and message_type_cnts["observation"]["state"] > 0 :
	result = "true"
else:
	result = "false"
check_table.add_row(["observation","state","At least 1 observation state events found", result])

#Check if we have an asr messages
if "observation" in message_type_cnts and "asr:transcription" in message_type_cnts["observation"] and message_type_cnts["observation"]["asr:transcription"] > 0 :
	result = "true"
else:
	result = "false"
check_table.add_row(["observation","asr","At least 1 Observation asr:transcription message found", result])

#Check if we have any FoV messages
if "observation" in message_type_cnts and "FoV" in message_type_cnts["observation"] and message_type_cnts["observation"]["FoV"] > 0 :
	result = "true"
else:
	result = "false"
check_table.add_row(["observation","Fov","At least 1 FoV events found", result])

if "trial" in message_type_cnts and "start" in message_type_cnts["trial"] \
	and message_type_cnts["trial"]["start"] == 1 :
	result = "true"
else:
	result = "false"
check_table.add_row(["trial","start","Exactly 1 trial start events found", result])

if "trial" in message_type_cnts and "stop" in message_type_cnts["trial"] \
	and message_type_cnts["trial"]["stop"] == 1 :
	result = "true"
else:
	result = "false"
check_table.add_row(["trial","stop","Exactly 1 trial stop events found", result])

# check to see if there are any error messges
if "error" in message_type_cnts:
	result = "false"
else:
	result = "true"
check_table.add_row(["error", "data","Exactly 0 error.data messages",result])
print_or_write(check_table.get_string())
if config["write_output_file"]:
	f_out.close()
