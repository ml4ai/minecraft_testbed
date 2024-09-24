#!/bin/python3

# Name: firstlook compare
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
import sys
import copy
#import requests

import time
import uuid
from deepdiff import DeepDiff
from prettytable import PrettyTable
from prettytable import HEADER



#define and parse the command line arguments
def parse_command_line_args():
	parser = argparse.ArgumentParser(description='ASIST replayer tool')
	parser.add_argument('file_spec_1', help='The first file to be compared')
	parser.add_argument('file_spec_2', help='The second file to be compared')
	parser.add_argument('messages', help='The messages types to count (all by default)')
	parser.add_argument('-o', '--output_spec', help='The output file spec', required=False)

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
file_1_counts = copy.deepcopy(dict(message_type_cnts))
print("First file counts\n")
pp.pprint(file_1_counts)
# process the second file
with open(config["file_spec_2"]) as f_in:
	for line in f_in:
		(pub_record_cnt, nopub_record_cnt, message_type_cnts, trial_properties) = process_hits(line,pub_record_cnt, nopub_record_cnt, message_type_cnts, trial_properties)
file_2_counts = copy.deepcopy(dict(message_type_cnts))
#print("Second file counts\n")
pp.pprint(file_1_counts)
pp.pprint(file_2_counts)

#dd = DeepDiff(file_1_counts, file_2_counts, view="tree", ignore_order=True, report_repetition=True, verbose_level=2)
dd = DeepDiff(file_1_counts, file_2_counts, ignore_order=True, report_repetition=True, verbose_level=2)
pp.pprint(dd)
print(dd == {})
exit(dd == {})

