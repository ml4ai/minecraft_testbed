#!/usr/bin/env python3

"""
ASIST Proximity AC

Author: Roger Carff
email:rcarff@ihmc.us
"""
import os
import json
from ASISTTools import ASISTTools
from asistagenthelper import ASISTAgentHelper
from ParticipantLocationInfo import ParticipantLocationInfo
import logging

__author__ = 'rcarff'

# Setup logging
LOG_LEVEL = logging.INFO
HELPER_LOG_LEVEL = logging.INFO  # WARN
LOG_HANDLER = logging.StreamHandler()
LOG_HANDLER.setFormatter(logging.Formatter("%(asctime)s | %(name)s | %(levelname)s — %(message)s"))
logger = logging.getLogger("IHMCProximityAC")
logger.setLevel(LOG_LEVEL)
logger.addHandler(LOG_HANDLER)
ASISTTools.set_logger(logger)


# This is the function which is called when a message is received for a
# topic which this Agent is subscribed to.
def on_message(topic, header, msg, data, mqtt_message):
    global helper, logger, maps, trial_infos, close_rooms_distance_in_blocks, update_every_n_sec, default_info

    try:
        key = helper.get_trial_key(msg)
        if key in trial_infos.keys():
            trial_infos[key]['location_handler'].process_message(topic, header, msg, data)

        if topic == 'trial':
            if msg['sub_type'] == 'start':
                logger.info('New Trial_id: ' + key + ' using map: ' + data['map_name'])
                trial_infos[key] = {'location_handler': ParticipantLocationInfo(close_location_distance=close_rooms_distance_in_blocks,
                                                                                maps_folder=helper.config_folder,
                                                                                maps_map=maps,
                                                                                helper=helper,
                                                                                output_every_n_sec=update_every_n_sec)}
                trial_infos[key]['location_handler'].set_preloaded_defaults(default_info)
                trial_infos[key]['location_handler'].process_message(topic, header, msg, data)
            else:
                trial_infos.pop(key, None)

    except Exception as ex:
        logger.error(ex)
        logger.error('Error processing topic = ' + topic)


logger.info("Starting IHMC's Proximity AC Agent")

# Agent Initialization
helper = ASISTAgentHelper(on_message)

# Set the helper's logging
helper.get_logger().setLevel(HELPER_LOG_LEVEL)
helper.get_logger().addHandler(LOG_HANDLER)

# see if the config.json file exists and load the maps filename mapping.
maps = {}
update_every_n_sec = 0.5
close_rooms_distance_in_blocks = 25.0
trial_infos = {}

logger.debug("Reading config.json config parameters...")
versionInfo = helper.get_version_info()
if 'config' in versionInfo.keys():
    try:
        for config in versionInfo['config']:
            if 'name' not in config.keys() or 'value' not in config.keys():
                continue
            if config['name'] == 'maps_file':
                maps_file = os.path.join(helper.config_folder, config['value'])
                if os.path.exists(maps_file):
                    with open(maps_file) as f:
                        maps = json.load(f)
            elif config['name'] == 'output-rate-per-second':
                update_every_n_sec = 1.0 / float(config['value'])
            elif config['name'] == 'close_rooms_distance_in_blocks':
                close_rooms_distance_in_blocks = float(config['value'])

    except Exception as ex:
        logger.error("Unable to parse config value from config.json.")

ASISTTools.get_logger().debug("Output Proximity every " + str(update_every_n_sec))

#Load the default Map
default_info = ParticipantLocationInfo(close_location_distance=close_rooms_distance_in_blocks,
                                       maps_folder=helper.config_folder,
                                       maps_map=maps,
                                       helper=helper,
                                       output_every_n_sec=update_every_n_sec)
default_info.load_map_info('DEFAULT')

# Set the agents status to 'up' and start the agent loop on a separate thread
helper.set_agent_status(helper.STATUS_UP)
logger.info("Starting Agent Loop on a separate thread.")
helper.start_agent_loop_thread()
logger.info("Agent is now running...")
