"""
PyGLFoVAgent Metadata Merge

This script allows a user to merge metadata files with corresponding FoV 
metadata files, and write the results to a third metadata file.  The script
assumes that the metadata and FoV files are named the same, are in two separate
directories, and end in `.metdata`.  Only FoV Summary messages will be merged.
The output metadata file will be written to a third directory, with the same
name as the original and FoV metadata files.

The FoV messages will be interleaved so that an FoV message immediately follows
the corresponding PlayerState message.

Usage
-----
python merge_metadata.py <input_path> <fov_path> <output_path> [num_cpu]

Command Line Arguments
----------------------
input_path : string
	The path to the directory containing the original metadata files
fov_path : string
	The path to the directory containing the FoV metadata files
output_path : string
	The path to write merged metadata to
num_cpu : integer, optional
	The (maximum) number of CPUs / processes to run in parallel.
"""

import multiprocessing as mp 
import argparse
import os
import json
from dateutil.parser import isoparse
from datetime import datetime, timedelta


message_type_to_topic_map = {
	("observation", "FoV"): "agent/pygl_fov/player/3d/summary",
	("agent", "FoV:Profile"): "agent/pygl_fov/profile",
	("agent", "versioninfo"): "agent/pygl_fov/versioninfo"
}

player_state_message_type = ("observation","state")

prefix_message_types = [("agent", "versioninfo")]
postfix_message_types = [("agent", "FoV:Profile")]

fields_to_copy = ["@timestamp", "@version", "host"]

time_delta = 5

def parse_arguments():
	"""
	Parse the command line arguments and return a Namespace instance with the
	argument contents
	"""

	parser = argparse.ArgumentParser(description="Merge metadata and FoV messages.")
	parser.add_argument('input_path', help='path to the directory containing input metadata files.')
	parser.add_argument('fov_path', help='path to the directory containing the FoV metadata files.')
	parser.add_argument('output_path', help='path to write the merged metadata files to.')
	parser.add_argument('-n', '--num_cpu', type=int, default=None, help='number of parallel processes to run.')
	parser.add_argument('-t', '--time_delta', type=float, default=None, help='amount of time (milliseconds) to add to timestamps')

	args = parser.parse_args()

	print("Arguments")
	print("---------")
	print("Input Path: ", args.input_path)
	print("FoV Path: ", args.fov_path)
	print("Output Path: ", args.output_path)
	print("Number of CPUs: ", args.num_cpu)

	return args


def merge_files(input_file_path, fov_file_path, output_file_path):
	"""
	Load all messages from the input and FoV files, and merge the two, writing
	the results to the output file

	Arguments
	---------
	input_file_path : string
		Path to the input metadata file
	fov_file_path : string
		Path to the FoV metadata file
	output_file_path : string
		Path to the output file
	"""

	print("%s + %s --> %s" % (input_file_path, fov_file_path, output_file_path))

	# Load the input and FoV messages
	with open(input_file_path) as input_file:
		input_messages = [json.loads(x) for x in input_file.readlines()]

	with open(fov_file_path) as fov_file:
		fov_messages = [json.loads(x) for x in fov_file.readlines()]

	# Add topics to the FoV messages, and extract prefix and postfix messages.
	# The FoV Summary messages will be indexed by their observation number
	prefix_fov_messages = []
	fov_summary_messages = {}
	postfix_fov_messages = []

	# Add the topic and sort the messages according to when they should appear.
	for message in fov_messages:
		message_type = (message["header"]["message_type"], message["msg"]["sub_type"])
		message["topic"] = message_type_to_topic_map.get(message_type, "UNKNOWN")

		# Put the message in the correponding bin
		if message_type in prefix_message_types:
			prefix_fov_messages.append(message)
		elif message_type in postfix_message_types:
			postfix_fov_messages.append(message)
		else:
			fov_summary_messages[message["data"]["observation"]] = message

	# For the prefix and postfix messages, copy over the fields to copy from
	# the first and last field in input messages.  Find the first and last
	# message to have all fields
	i=0
	done = False
	while not done:
		first_message = input_messages[i]
		done = True
		for field in fields_to_copy:
			done = done and field in first_message
		i += 1

	i=-1
	done = False
	while not done:
		last_message = input_messages[i]
		done = True
		for field in fields_to_copy:
			done = done and field in last_message
		i -= 1



	for message in prefix_fov_messages:
		for field in fields_to_copy:
			message[field] = first_message[field]

	for message in postfix_fov_messages:
		for field in fields_to_copy:
			message[field] = last_message[field]

	# Order the messages from the two sources, adding FoV messages after any
	# PlayerState messages
	print(f'{output_file_path}: Prefix FoV messages')
	output_messages = prefix_fov_messages

	print(f'{output_file_path}: Metadata + FoV messages')
	for message in input_messages:

###		message_type = (message["header"]["message_type"], message["msg"]["sub_type"])

		# Ignore any previous FoV messages
###		if message_type not in message_type_to_topic_map.keys():
		output_messages.append(message)

		if (message["header"]["message_type"], message["msg"]["sub_type"]) == player_state_message_type and  message["data"]["observation_number"] in fov_summary_messages:

			fov_message = fov_summary_messages[message["data"]["observation_number"]]

			for field in fields_to_copy:
				fov_message[field] = message[field]

			# Adjust the timestamps
			fov_message['@timestamp'] = (isoparse(message['@timestamp']) + timedelta(milliseconds=time_delta)).isoformat() + 'Z'
			fov_message['header']['timestamp'] = (isoparse(message['header']['timestamp']) + timedelta(milliseconds=time_delta)).isoformat() + 'Z'
			fov_message['msg']['timestamp'] = (isoparse(message['msg']['timestamp']) + timedelta(milliseconds=time_delta)).isoformat() + 'Z'

			output_messages.append(fov_message)

	# Add any postfix messages
	print(f'{output_file_path}: Postfix FoV messages')	
	for message in postfix_fov_messages:
		output_messages.append(message)

	# Write the resulting messages to the output file
	print(f'{output_file_path}: Writing output file')	
	with open(output_file_path, 'w') as output_file:
		for message in output_messages:
			output_file.write(json.dumps(message) + '\n')



def run(input_path, fov_path, output_path, num_processes = None):
	"""
	Run the PyGLFoVAgent on the files in the given directory.  Only files 
	ending in `.metadata` will be processed.  FoV files will be written with
	the same filename

	Arguments
	---------
	input_path : string
		Path to the directory containing metadata files to process
	output_path : string
		Path to write FoV metadata files to after processing
	"""

	# Check to see if the output path exists, and create if it doesn't
	if not os.path.isdir(output_path):
		os.makedirs(output_path)

	# Process all the files -- create a list of input/output tuples, and then
	# use a process pool to process the pairs asynchronously
	input_fov_output_triples = []

	fov_filenames = os.listdir(fov_path)

	for filename in os.listdir(input_path):

		# Only process files ending in `.metadata`
		if filename.endswith('.metadata') and filename in fov_filenames:

			input_file_path = os.path.join(input_path, filename)
			fov_file_path = os.path.join(fov_path, filename)
			output_file_path = os.path.join(output_path, filename)

			input_fov_output_triples.append((input_file_path, fov_file_path, output_file_path))


	# If the number of processes isn't given, or is zero or negative, use all
	# the CPUs available
	if num_processes is None or num_processes < 1:
		num_processes = mp.cpu_count()

	# Create a pool of processes and perform the calculations.  Since the
	# processes don't return anything, using an async mapping should be the
	# most efficient, and not requrire any additional overhead.
#	pool = mp.Pool(num_processes)
#	_ = pool.starmap_async(merge_files, input_fov_output_triples)
#	pool.close()
#	pool.join()


	for files in input_fov_output_triples:
		merge_files(files[0], files[1], files[2])


if __name__ == '__main__':
	"""
	Main entry point for the script
	"""


	args = parse_arguments()
	run(args.input_path, args.fov_path, args.output_path, args.num_cpu)





