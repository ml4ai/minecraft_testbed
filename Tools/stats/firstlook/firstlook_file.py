# Name: firstlook
# Description: Tool in the ASIST testbed that gathers basic statistics of a trial from a .metadata file
#
# (c) Copyright 2021 Aptima Inc.

#Imports
import argparse
#import configparser
from datetime import datetime

import json
import pprint
import re
#import requests

import time
import uuid
from prettytable import PrettyTable
from prettytable import HEADER

condition_checks = [
{'msgtype':'agent','subtype':'Intervention:Chat','check':'at least','number':1},
{'msgtype':'agent','subtype':'measures','check':'at least','number':1},
{'msgtype':'event','subtype':'Event:Door','check':'at least','number':1},
{'msgtype':'event','subtype':'Event:ItemEquipped','check':'at least','number':1},
{'msgtype':'event','subtype':'Event:MissionState','check':'exactly','number':2},
{'msgtype':'event','subtype':'Event:PlayerSwinging','check':'at least','number':1},
{'msgtype':'event','subtype':'Event:Signal','check':'at least','number':1},
{'msgtype':'event','subtype':'Event:RoleSelected','check':'at least','number':1},
{'msgtype':'event','subtype':'Event:RubbleDestroyed','check':'at least','number':1},
{'msgtype':'event','subtype':'Event:ToolUsed','check':'at least','number':1},
{'msgtype':'event','subtype':'Event:location','check':'at least','number':1},
{'msgtype':'event','subtype':'Event:ProximityBlockInteraction','check':'at least','number':1},
{'msgtype':'event','subtype':'Event:VictimPickedUp','check':'at least','number':1},
{'msgtype':'event','subtype':'Event:VictimPlaced','check':'at least','number':1},
{'msgtype':'event','subtype':'Event:dialogue_event','check':'at least','number':1},
{'msgtype':'groundtruth','subtype':'Mission:BlockageList','check':'exactly','number':1},
{'msgtype':'groundtruth','subtype':'Mission:VictimList','check':'exactly','number':1},
{'msgtype':'groundtruth','subtype':'Mission:FreezeBlockList','check':'exactly','number':1},
{'msgtype':'groundtruth','subtype':'Mission:ThreatSignList','check':'exactly','number':1},
{'msgtype':'groundtruth','subtype':'SemanticMap:Initialized','check':'exactly','number':1},
{'msgtype':'observation','subtype':'state','check':'at least','number':1},
{'msgtype':'observation','subtype':'asr:transcription','check':'at least','number':1},
{'msgtype':'observation','subtype':'FoV','check':'at least','number':1},
{'msgtype':'status','subtype':'Status:SurveyResponse','check':'at least','number':1},
{'msgtype':'trial','subtype':'start','check':'exactly','number':1},
{'msgtype':'trial','subtype':'stop','check':'exactly','number':1},
{'msgtype':'error','subtype':'data','check':'exactly','number':0}
]
# Odd checks that don't fit a nice generalized model like above
#{'msgtype':'event','subtype':'Event:Triage              |               An even number of triage events found                |   true  |
#{'msgtype':'event','subtype':'Event:VictimPickedUP,Event:VictimPlaced |  An equal number of VictimPickedUp and VictimPlaced events found   |   true  |
#define and parse the command line arguments
def parse_command_line_args():
	parser = argparse.ArgumentParser(description='ASIST replayer tool')
	parser.add_argument('-f','--file', dest='file_spec', help='The file to be analyzed')
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

if cmd_args.file_spec != None:
	config["file_spec"] = cmd_args.file_spec
if cmd_args.output_spec != None:
	config["output_spec"] = cmd_args.output_spec
	config["write_output_file"] = True
else:
	config["write_output_file"] = False

#pp.pprint(config)


if config["write_output_file"]:
	f_out = open(config["output_spec"], "w+")

with open(config["file_spec"],encoding='utf-8') as f_in:
	
	for line in f_in:		
		(pub_record_cnt, nopub_record_cnt, message_type_cnts, trial_properties) = process_hits(line,pub_record_cnt, nopub_record_cnt, message_type_cnts, trial_properties)
		#Get the number of results that returned in the last scroll

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
# do specific checks on the message counts
# ---

#use the condition_checks array to check for errors in the data
for cond in condition_checks:
    result = "false"
    if cond["msgtype"] in message_type_cnts and cond["subtype"] in message_type_cnts[cond["msgtype"]]:
        if cond["check"] == "at least":
            if message_type_cnts[cond["msgtype"]][cond["subtype"]] >= cond["number"]:
                result = "true"
            else:
                result = "false"
        if cond["check"] == "exactly":
            if message_type_cnts[cond["msgtype"]][cond["subtype"]] == cond["number"]:
                result = "true"
            else:
                result = "false"
    else:
        if cond["check"] == "exactly" and cond["number"] == 0:
            result = "true"
    
    check_table.add_row([cond["msgtype"],cond["subtype"],"{0} {1} {2} {3} messages found".format(cond["check"], cond["number"], cond["msgtype"], cond["subtype"]), result])    

#now check any unusual checks that don't fit into the data driven checks above
# check that there are an equal number of victim picked up and placed events
if "event" in message_type_cnts and "Event:VictimPickedUp" in message_type_cnts["event"] \
	and "Event:VictimPlaced" in message_type_cnts["event"] \
	and message_type_cnts["event"]["Event:VictimPickedUp"] == message_type_cnts["event"]["Event:VictimPlaced"]:
	result = "true"
else:
	result = "false"
check_table.add_row(["event","Event:VictimPickedUP,Event:VictimPlaced","An equal number of VictimPickedUp and VictimPlaced events found", result])

# there is an even number of triage events e.g. equal number of InProgress and Success or Failure
if "event" in message_type_cnts and "Event:Triage" in message_type_cnts["event"] and (message_type_cnts["event"]["Event:Triage"] % 2) == 0 :
	result = "true"
else:
	result = "false"
check_table.add_row(["event","Event:Triage","An even number of triage events found", result])


print_or_write(check_table.get_string())
if config["write_output_file"]:
	f_out.close()
