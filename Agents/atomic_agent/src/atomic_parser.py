#!/usr/bin/env python3

"""
reads messages from bus & builds a knowledge structure for each player

email:skenny@ict.usc.edu
"""

import os
import json
import uuid
from asistagenthelper import ASISTAgentHelper
import logging
import psychsim
#from live_analyze_json import *
from atomic.parsing.asist_world import *

# probably don't need run_rddl will import
import numpy as np

#from live_make_world_tree import atomicParser

__author__ = 'skenny'

# This is the function which is called when a message is received 
# for a topic which this Agent is subscribed to.
def on_message(topic, header, msg, data, mqtt_message):
    global helper, extra_info, logger, aparser, init_chat, num_starts, playeridlist
    
    # readd topic & header
    mqtt_message.update({'topic':topic})
    mqtt_message.update({'header':header})

    # handle trial start
    if topic == 'trial' and msg['sub_type'] == 'start':
        #aparser.get_playerlist(data['client_info'])
        for p in data['client_info']:
            playeridlist.append(p['participant_id'])

        logger.info(" - Trial Started with Mission set to: " + data['experiment_mission'])
        init_chat = 0
        num_starts += 1

    # requires location monitor to be running
    elif topic == 'ground_truth/semantic_map/initialized':
        #aparser.load_semantic_map(mqtt_message)
        logger.info("SUCCESS: semantic map is initialized in atomic parser")

    #if num_starts == 2: # we're on 2nd trial, reinit asistworld obj & increment
     #   aparser = ASISTWorld()
      #  num_starts += 1
    resmsg = aparser.process_msg(mqtt_message)
    if resmsg:
        minutes = int(data['elapsed_milliseconds'] / 1000 / 60)
        seconds = (data['elapsed_milliseconds'] / 1000) - (minutes * 60)
        logger.info(" - At " + str(minutes) + ":" + str(seconds) + " into the mission " + data['participant_id'] + " sending intervention to chat! playeridlist == "+str(playeridlist))
        comment = str(resmsg)
        msg_data = {
            "id": str(uuid.uuid4()),
            "agent": helper.agent_name,
            "created": helper.generate_timestamp(),
            "start": -1,
            "content": comment,
            #"receivers": [data['participant_id']],
            "receivers": playeridlist,
            "type": 'string',
            "renderers": ["Minecraft_Chat"],
            "explanation": {"reason": "INTERVENTION SENT TO PLAYERS"}
        }
        helper.send_msg("agent/intervention/"+helper.agent_name+"/chat",
                        "agent",
                        "Intervention:Chat",
                        "0.1",
                        timestamp=msg['timestamp'],
                        data=msg_data)

        # Agent Initialization
helper = ASISTAgentHelper(on_message)
aparser = ASISTWorld()
init_chat = 0
num_starts = 0
playeridlist = [] # eventually should be stored in asistworld object
# Set the helper's logging level to INFO
LOG_HANDLER = logging.StreamHandler()
LOG_HANDLER.setFormatter(logging.Formatter("%(asctime)s | %(name)s | %(levelname)s — %(message)s"))
helper.get_logger().setLevel(logging.INFO)
helper.get_logger().addHandler(LOG_HANDLER)

# Create our own logger for the MoreComplexAgent
logger = logging.getLogger(helper.agent_name)
logger.setLevel(logging.INFO)
logger.addHandler(LOG_HANDLER)

# load extra info from the ConfigFolder for use later
extra_path = os.path.join(helper.config_folder, 'extraInfo.json')
extra_info = {}
if os.path.exists(extra_path):
    with open(extra_path) as extra_file:
        extra_info = json.load(extra_file)
if "default" not in extra_info.keys():
    extra_info["default"] = "I guess {0} is an okay role."

# Set the agents status to 'up' and start the agent loop on a separate thread
helper.set_agent_status(helper.STATUS_UP)
logger.info("Starting Agent Loop on a separate thread.")
helper.start_agent_loop_thread()
logger.info("Agent is now running...")

# if you need to do anything else you can do it here and if you want to stop the agent thread
# you can run the following, but until the agent loop is stopped, the process will continue to run.
#
# helper.stop_agent_loop_thread()
