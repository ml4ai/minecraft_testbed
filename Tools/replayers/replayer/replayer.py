# Name: replayer
# Description: Tool in the ASIST testbed that replays data from the elasstic dataset
#				and replays the data by publishing it on the MQTT message bus
# (c) Copyright 2020 Aptima Inc.

#Imports
import argparse
#import certifi
import configparser
from datetime import datetime
from elasticsearch import Elasticsearch
from elasticsearch.connection import create_ssl_context
import json
import paho.mqtt.client as mqttClient
import pprint
import re
#import requests
import ssl
import time
import uuid



#define and parse the command line arguments
def parse_command_line_args():
	parser = argparse.ArgumentParser(description='ASIST replayer tool')
	parser.add_argument('-t','--trial_id', dest='trial_id', help='The trial_id to be replayed')
	parser.add_argument('-r','--replay_id', dest='replay_id', help='The replay_id to be replayed')
	parser.add_argument('-i', '--index', dest='es_index', help='The elasticsearch index to be queried')
	parser.add_argument('-ct', '--check_time', dest='check_time', action='store_true', default=False,help='If true, check message time values are always increasing.')
	parser.add_argument('-gt', '--get_trial_ids', dest='get_trial_ids', action='store_true', default=False, help='if True, Query database for trial ids.')
	parser.add_argument('-dr', '--dont_replay', dest='dont_replay', action='store_true', default=False, help='the set of topics to not replay')
	#parser.add_argument('-l', '--list', dest='list_trials', help='List the trials in elasticsearch')

	return parser.parse_args()

#process hits to re-publish
def process_hits(hits,new_replay_id, pub_cnt, nopub_cnt, message_type_cnts):
	global mqtt_client
	global cmd_args
	# setup to check message times, if needed
	header_last_time = '1970-01-01T00:00:00.0000Z'
	msg_last_time = '1970-01-01T00:00:00.0000Z'
	#print(mqtt_client)
	for item in hits:
		obs = item["_source"]
		#print(obs)
		#json_obj = json.loads(obs)
		json_obj = obs
		#At some point we may also want to shut off the re-capture of the replayed data as an option.
		#add a date and time to the trial_id so that we have a new unique trial_id that will be saved in elastic.  
		if cmd_args.check_time:
			header_last_time = check_message_time(item["_source"], header_last_time)
		#the next line will add the msg.replay_id to every message that gets replayed, even messages that didn't originally hae a msg section
		json_obj["msg"]["replay_id"] = new_replay_id
		if not cmd_args.replay_id is None:	#we must be replaying a replay, so add the root
			json_obj["msg"]["replay_root_id"] = cmd_args.replay_id		
		message_type = json_obj["header"]["message_type"]
		#print(message_type)
		#filter out messages we don't want to re-publish
		if should_republish_message(item["_source"]["topic"]):
			mqtt_client.publish(item["_source"]["topic"], json.dumps(json_obj))
			pub_cnt+=1
		else:
			nopub_cnt+=1
		if message_type in message_type_cnts:
			message_type_cnts[message_type] +=1
			#print('Add one to message_type {t}.'.format(t=message_type))
		else:
			message_type_cnts[message_type] = 1
			#print('Init for message type {t}.'.format(t=message_type))
	return (pub_cnt, nopub_cnt, message_type_cnts)

#process hits to look for trial_ids
def get_trials(hits, trial_cnt, replay_cnt, trial_list):
	for item in hits:
		obs = item["_source"]
		#print(obs)
		#json_obj = json.loads(obs)
		json_obj = obs
		message_type = json_obj["header"]["message_type"]
		#check to make sure we have the right messsge type of experiment
		if not message_type == "trial":
			print("Wrong message type to get_trials: {msg_type}".format(msg_type=message_type))
			exit(1)
		#grab the trial_id and replay_ids and build a dictionary of them
		if "msg" in item["_source"] and "trial_id" in item["_source"]["msg"]:
			trial_id = item["_source"]["msg"]["trial_id"]
			if not trial_id in trial_list:
				trial_list[trial_id] = {}
				trial_cnt+=1
			if "replay_id" in item["_source"]["msg"] and ((not "replay_root_id" in item["_source"]["msg"]) or ("replay_root_id" in item["_source"]["msg"] and item["_source"]["msg"]["replay_root_id"] is None)):
				replay_id = item["_source"]["msg"]["replay_id"]
				#print("replay_id")
				#print(replay_id)
				if not replay_id in trial_list[trial_id] and not replay_id is None:
					trial_list[trial_id][replay_id] = []
					replay_cnt+=1			
			if "replay_root_id" in item["_source"]["msg"] and not item["_source"]["msg"]["replay_root_id"] is None:		#check to see if we have a root_replay_id
				#print("replay_root_id")
				#print(item["_source"]["msg"]["replay_root_id"])
				if item["_source"]["msg"]["replay_root_id"] in trial_list[trial_id]:	#if so try to add to the replay list of the trial
					if not item["_source"]["msg"]["replay_id"] in trial_list[trial_id][(item["_source"]["msg"]["replay_root_id"])]:
						trial_list[trial_id][(item["_source"]["msg"]["replay_root_id"])].append(item["_source"]["msg"]["replay_id"])
				else:
					replay_root_id = item["_source"]["msg"]["replay_root_id"]
					trial_list[trial_id][replay_root_id] = []
	return (trial_cnt, replay_cnt, trial_list)


#decide if the topic should be republished
def should_republish_message(topic):
	global config
	if config["dont_replay"] and topic in config["dont_replay_topics"]:
		return False
	else:
		return True

#check that the message timestamp is always increasing
def check_message_time(item_source, header_last_time):
	new_header_last_time = header_last_time
	if header_last_time > item_source["@timestamp"]:
		print("@timestamp error, backward time. last @timestamp: {timestamp_last_time}, this timestamp time: {this_time}".format(header_last_time=header_last_time, this_time=item_source["@timestamp"]))
	new_header_last_time = item_source["@timestamp"]
	return new_header_last_time

#fix the query specified in the body parameter by inserting the trial_id
def fix_query(body, trial_id):
	return body.replace("<trial_id>", trial_id)

# Define config
def read_config_file(config_filespec):
	cf = {}
	config = configparser.ConfigParser()
	config.read(config_filespec)

	cf["elastic_host"] = config['ELASTIC']['host']
	cf["elastic_port"] = int(config['ELASTIC']['port'])
	cf["scheme"] = config['ELASTIC']['scheme']
	cf["timeout"] = int(config['ELASTIC']['timeout'])
	cf["index"] = config['ELASTIC']['index']
	cf["type"] = config['ELASTIC']['doc_type']
	cf["size"] = config['ELASTIC']['size']
	cf["trial_replay_query"] = config['ELASTIC']['trial_replay_query']
	cf["replay_replay_query"] = config['ELASTIC']['replay_replay_query']
	cf["use_ssl"] = config['ELASTIC'].getboolean('use_ssl')
	cf["mqtt_host"] = config["MQTT"]["host"]
	cf["mqtt_port"] = config["MQTT"]["port"]
	cf["get_trial_id_query"] = config["ELASTIC"]['get_trial_id_query']
	cf["dont_replay_topics"] = json.loads(config["REPLAYER"]['dont_replay_topics'])
	if "output_file" in config["REPLAYER"]:
		cf["output_file"] = config['REPLAYER']['output_file']
		cf['write_output_file'] = True
	else:
		cf["output_file"] = ''
		cf['write_output_file'] = False

	return cf

#mqtt on_connect
def mqtt_on_connect(client, userdata, flags, rc):
    if rc==0:
        print("connected OK Returned code=",rc)
    else:
        print("Bad connection Returned code=",rc)

#set up connection to elastic
def setup_elastic(config):
	es = Elasticsearch(
		[{
			'host': config["elastic_host"],
			'port': config["elastic_port"],
			'scheme': config["scheme"],
			'use_ssl': config["use_ssl"]
		}]
		, timeout=config["timeout"])
	return es

pub_record_cnt = 0
nopub_record_cnt = 0
message_type_cnts = {}
#initialize for trial query
trial_cnt = 0
replay_cnt = 0
trial_list= {}

# setup new trial id
def generate_replay_id():
	new_replay_id = uuid.uuid1()
	#you need to remove the first 9 characters because the urn function addes "urn:uuid:" to the uuid
	return new_replay_id.urn[9:]

# main
pp = pprint.PrettyPrinter(indent=4)

#read in the config file and set the parameters
config_filespec = 'config.ini'
config = read_config_file(config_filespec)

#get any command line arguments
cmd_args = parse_command_line_args()
pp.pprint(cmd_args)

#over-ride some config.ini parameters with the command line parameters
if "es_query" in cmd_args and cmd_args.es_query != None:
	config["body"] = cmd_args.es_query
if "es_index" in cmd_args and cmd_args.es_index != None:
	config["index"] = cmd_args.es_index
if cmd_args.check_time : 
	config["check_time"] = True
else:
	config["check_time"] = False
if cmd_args.get_trial_ids :
	config["get_trial_ids"] = True
else:
	config["get_trial_ids"] = False
if cmd_args.dont_replay :
	config["dont_replay"] = True
else:
	config["dont_replay"] = False
#Can only replay either a trial id or a replay id, not both
if cmd_args.trial_id != None and cmd_args.replay_id != None:
	print("Please only specify either a trial id or a replay id")
	exit()

if cmd_args.trial_id != None:
	config["trial_replay_query"] = fix_query(config["trial_replay_query"],cmd_args.trial_id)
if cmd_args.replay_id != None:
	config["replay_replay_query"] = fix_query(config["replay_replay_query"],cmd_args.replay_id)	

#set up the new trial id	
new_replay_id = generate_replay_id()
print("New replay_id: " + new_replay_id)
pp.pprint(config)

#connect to elastic
es = setup_elastic(config)

# setup and connect to the mqtt messge bus
mqtt_client = mqttClient.Client("replayer")
mqtt_client.on_connect=mqtt_on_connect
mqtt_client.connect(config["mqtt_host"])
mqtt_client.loop_start()

if config["write_output_file"]:
	f = open(config["output_file"], "w+")

#check index exists
if not es.indices.exists(index=config["index"]):
    print("Index " + config["index"] + " does not exists")
    exit()

# Init scroll by search
if config["get_trial_ids"]:
	data = es.search(index=config["index"],  scroll='2m', size=config["size"], body=config["get_trial_id_query"])
else:
	if cmd_args.trial_id != None:
		data = es.search(index=config["index"],  scroll='2m', size=config["size"], body=config["trial_replay_query"])
	else:
		data = es.search(index=config["index"],  scroll='2m', size=config["size"], body=config["replay_replay_query"])

# Get the scroll ID
sid = data['_scroll_id']
scroll_size = len(data['hits']['hits'])

while scroll_size > 0:
    #before scroll, process current batch of hits
	if config["get_trial_ids"]:
		(trial_cnt, replay_cnt, trial_list) = get_trials(data['hits']['hits'], trial_cnt, replay_cnt, trial_list)
	else:
		(pub_record_cnt, nopub_record_cnt, message_type_cnts) = process_hits(data['hits']['hits'],new_replay_id,pub_record_cnt, nopub_record_cnt, message_type_cnts)

	data = es.scroll(scroll_id=sid, scroll='2m')

    #update the scroll ID
	sid = data['_scroll_id']

    #Get the number of results that returned in the last scroll
	scroll_size = len(data['hits']['hits'])

# clean up the mqtt connection
#wait a bit to make sure the mqtt messages have been sent
time.sleep(5)
mqtt_client.loop_stop()    #Stop loop 
mqtt_client.disconnect() # disconnect

if config["get_trial_ids"]:
	print('Found {cnt} trial records'.format(cnt=trial_cnt))
	print('found {cnt} replay records'.format(cnt=replay_cnt))
	print('trial_id [ <replay_id>, <replay_id>, ...]')
	pp.pprint(trial_list)
else:
	print('Published {cnt} records'.format(cnt=pub_record_cnt))
	print('Did not publish {cnt} records'.format(cnt=nopub_record_cnt))
	pp.pprint(message_type_cnts)
	print('New replay id is: {new_replay_id}'.format(new_replay_id=new_replay_id))
if config["write_output_file"]:
	f.close()


