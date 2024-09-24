#!/usr/bin/env python3

"""
Simple Dyad AC Agent

Author: Roger Carff
email:rcarff@ihmc.us
"""
import json
import uuid
from asistagenthelper import ASISTAgentHelper
import logging

__author__ = 'rcarff'

# Setup logging
LOG_LEVEL = logging.INFO
HELPER_LOG_LEVEL = logging.WARN

LOG_HANDLER = logging.StreamHandler()
LOG_HANDLER.setFormatter(logging.Formatter("%(asctime)s | %(name)s | %(levelname)s — %(message)s"))
logger = logging.getLogger("IHMCProximityAC")
logger.setLevel(LOG_LEVEL)
logger.addHandler(LOG_HANDLER)


# This is the function which is called when a message is received for a to
# topic which this Agent is subscribed to.
def on_message(topic, header, msg, data, mqtt_message):
    global logger, callsign2pid_map

    if topic != 'observations/events/player/proximity':
        return

    # Look for dyad changes in the proximity event
    # time, p1:callsign, p1:part_id, p2:callsign, p2:part_id, distance
    for participant in data['participants']:
        # TODO:  This masks any role changes updates we would want to publish!!!
        callsign2pid_map[participant['callsign']] = {"callsign": participant['callsign'],
                                                     "participant_id": participant['participant_id'],
                                                     "role": participant['role']}
        for dist_info in participant['distance_to_participants']:
            if dist_info['id'] not in callsign2pid_map:
                continue
            check_for_dyad(data['elapsed_milliseconds'],
                           participant['callsign'],
                           dist_info['id'],
                           dist_info['distance'])


def check_for_dyad(ms_elapsed, cs1, cs2, distance):
    global logger, dyads, dyad_ranges

    if cs1 is None or cs2 is None or distance is None:
        return

    # Build the dyad key based on callsign names
    key = cs1 + ":" + cs2 if cs1 < cs2 else cs2 + ":" + cs1

    # determine the dyad range/probability for this distance
    probability = 0.0
    for dr in dyad_ranges:
        if dr[0] <= distance < dr[1]:
            probability = dr[2]
            break

    if key in dyads.keys():
        # dyad already exists.  See if there is any change.
        dyad = dyads[key]
        if probability <= 0.0:
            # dyad is over publish an end event and pop this dyad from the list
            dyad['in-dyad-probability'] = 0.0
            publish_dyad(ms_elapsed, dyad, "end")
            dyads.pop(key, None)
        elif probability != dyad['in-dyad-probability']:
            # publish probability change
            dyad['in-dyad-probability'] = probability
            publish_dyad(ms_elapsed, dyad, "update")
    elif probability > 0.0:
        # new dyad possibly starting!!
        dyad = {"id": str(uuid.uuid4()),
                "start_time": ms_elapsed,
                "p1": cs1,
                "p2": cs2,
                "in-dyad-probability": probability}
        dyads[key] = dyad
        publish_dyad(ms_elapsed, dyad, "start")


def publish_dyad(ms_elapsed, dyad, dyad_type):
    global helper, logger, callsign2pid_map

    data = {"id": dyad["id"],
            "event_type": dyad_type,
            "elapsed_milliseconds": ms_elapsed,
            "participants": [callsign2pid_map[dyad["p1"]], callsign2pid_map[dyad["p2"]]],
            "in-dyad-probability": dyad["in-dyad-probability"]}
    if dyad_type == "end":
        data['duration'] = ms_elapsed - dyad["start_time"]

    logger.info("Publishing Dyad: " + json.dumps(data))

    helper.send_msg("observations/events/player/dyad",
                    "event",
                    "Event:dyad", "1.0",
                    data=data)


logger.info("Starting IHMC's Dyad AC Agent")

# Agent Initialization
helper = ASISTAgentHelper(on_message)

# Set the helper's logging level to INFO
helper.get_logger().setLevel(HELPER_LOG_LEVEL)
helper.get_logger().addHandler(LOG_HANDLER)

# see if the config.json file exists and load the maps filename mapping.
dyads = {}
dyad_ranges = []
callsign2pid_map = {}

logger.debug("Reading config.json config parameters...")
versionInfo = helper.get_version_info()
if 'config' in versionInfo.keys():
    try:
        for config in versionInfo['config']:
            if 'name' not in config.keys() or 'value' not in config.keys():
                continue
            if config['name'] == 'dyad_ranges':
                dyad_ranges = json.loads(config['value'])

    except Exception as ex:
        logger.error("Unable to parse config value from config.json.")

logger.info("Dyad Ranges: " + str(dyad_ranges))

# Set the agents status to 'up' and start the agent loop on a separate thread
helper.set_agent_status(helper.STATUS_UP)
logger.info("Starting Agent Loop on a separate thread.")
helper.start_agent_loop_thread()
logger.info("Agent is now running...")
