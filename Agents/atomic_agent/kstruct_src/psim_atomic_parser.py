#!/usr/bin/env python3

"""
adapted from Simple ASIST Agent

email:skenny@ict.usc.edu
"""

import os
import json
import uuid
from asistagenthelper import ASISTAgentHelper
import logging

# probably don't need run_rddl will import
import numpy as np
from rddl2psychsim.conversion.converter import Converter
from atomic.parsing.get_psychsim_action_name import Msg2ActionEntry
from atomic.parsing.parse_into_msg_qs import MsgQCreator
from atomic.parsing.count_features import CountAction, CountRoleChanges, CountTriageInHallways, CountEnterExit

from run_rddl import atomicParser

__author__ = 'rcarff'

# This is the function which is called when a message is received for a to
# topic which this Agent is subscribed to.
def on_message(topic, header, msg, data, mqtt_message):
    global helper, extra_info, logger, aparser, init_chat

    # logger.info("Received a message on the topic: " + topic)

    # Now handle the message based on the topic.  Refer to Message Specs for the contents of header, msg, and data
    if topic == 'trial' and msg['sub_type'] == 'start':
        # handle the start of a trial!!
        logger.info(" - *******************Trial Started with Mission set to: " + data['experiment_mission'])

    elif topic == 'ground_truth/semantic_map/initialized':
        print("......................................... got semantic map...................")
        aparser.load_semantic_map(data['semantic_map'])
        logger.info("semantic map is initialized in atomic parser")

    elif topic == 'ground_truth/mission/victims_list':
        print("!! got victim msg...loading....")
        aparser.load_victims(mqtt_message)
        logger.info("victim list initialized in atomic parser len vlist:: "+str(len(aparser.msg_qs.jsonParser.vList)))

    # ??? change to itemequipped here?
        
    #elif topic == 'observations/events/player/role_selected':
    elif topic == 'observations/events/player/itemequipped' and init_chat == 0: # first item equip
        init_chat = 1
        minutes = int(data['elapsed_milliseconds'] / 1000 / 60)
        seconds = (data['elapsed_milliseconds'] / 1000) - (minutes * 60)

        logger.info(" - At " + str(minutes) + ":" + str(seconds) + " into the mission " + data['participant_id'] + " initial item equipped!")
        
        comment = "MISSION STARTING! GOOD LUCK WITH YOUR RESCUES!"

        # build up the message's data and publish it
        msg_data = {
            "id": str(uuid.uuid4()),
            "agent": helper.agent_name,
            "created": helper.generate_timestamp(),
            "start": -1,
            "content": comment,
            "receivers": [data['participant_id']],
            "type": 'string',
            "renderers": ["Minecraft_Chat"],
            "explanation": {"reason": "INTERVENTION WILL BE SENT TO PLAYER HERE"}
        }
        helper.send_msg("agent/intervention/"+helper.agent_name+"/chat",
                        "agent",
                        "Intervention:Chat",
                        "0.1",
                        timestamp=msg['timestamp'],
                        data=msg_data)

    elif topic == 'observations/events/player/triage':
        minutes = int(data['elapsed_milliseconds'] / 1000 / 60)
        seconds = (data['elapsed_milliseconds'] / 1000) - (minutes * 60)

        logger.info(" - At " + str(minutes) + ":" + str(seconds) + " into mission, did triage...attempting proc_msg")
        aparser.proc_msg(mqtt_message)
        # use the info read in from the extra info file to form the comment
        comment = 'good job saving victim, buddy!'

        # build up the message's data and publish it
        msg_data = {
            "id": str(uuid.uuid4()),
            "agent": helper.agent_name,
            "created": helper.generate_timestamp(),
            "start": -1,
            "content": comment,
            "receivers": [data['participant_id']],
            "type": 'string',
            "renderers": ["Minecraft_Chat"],
            "explanation": {"reason": "INTERVENTION WILL BE SENT TO PLAYER HERE"}
        }
        helper.send_msg("agent/intervention/"+helper.agent_name+"/chat",
                        "agent",
                        "Intervention:Chat",
                        "0.1",
                        timestamp=msg['timestamp'],
                        data=msg_data)


    elif topic == 'trial' and msg['sub_type'] == 'stop':
        print("......trial over sending post trial message.....")
        comment = 'finished first trial, way to go! keep up the good work!'
        # build up the message's data and publish it
        msg_data = {
            "id": str(uuid.uuid4()),
            "agent": helper.agent_name,
            "created": helper.generate_timestamp(),
            "start": -1,
            "content": comment,
            "receivers": ['skenny'],
            "type": 'string',
            "renderers": ["Minecraft_Chat"],
            "explanation": {"reason": "more pre-trial info will be given here xxx"}
        }
        helper.send_msg("agent/intervention/"+helper.agent_name+"/chat",
                        "agent",
                        "Intervention:Chat",
                        "0.1",
                        timestamp=msg['timestamp'],
                        data=msg_data)
# Agent Initialization
helper = ASISTAgentHelper(on_message)
aparser = atomicParser()
init_chat = 0
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
