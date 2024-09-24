#!/usr/bin/env python3

"""
IHMC Location Monitor

Reads Area information from a JSON Map file and reports entity Area
change events when they occur

Author: Roger Carff
email:rcarff@ihmc.org
"""

import os
import time
import json
import logging
from asistagenthelper import ASISTAgentHelper
from SemanticMap import SemanticMap

__author__ = 'rcarff'

# Setup logging
LOG_HANDLER = logging.StreamHandler()
LOG_HANDLER.setFormatter(logging.Formatter("%(asctime)s | %(name)s | %(levelname)s — %(message)s"))
logger = logging.getLogger("LocationMonitor")
logger.addHandler(LOG_HANDLER)
logger.setLevel(logging.INFO)


def check_location_update(trial_info_key, timestamp, playername, pid, callsign, x, z, elapsed_ms, mission_timer, observation_number):
    global trial_infos, helper, logger

    if trial_info_key not in trial_infos.keys():
        return

    trial = trial_infos[trial_info_key]

    # get the current info for this player in this trial or create it if not there
    first_time = False

    name = pid
    if pid is None and playername is not None:
        if playername in trial['playername2ParticipantId'].keys():
            name = trial['playername2ParticipantId'][playername]
        else:
            name = playername
    if name is None:
        return

    if name not in trial['players'].keys():
        logger.info('New player: ' + name + ' in trial: ' + trial_info_key)
        player_info = {'name': name, 'x': 0.0, 'z': 0.0, 'previous': {'locations': [], 'connections': []}}
        trial['players'][name] = player_info

    player_info = trial['players'][name]
    if player_info['x'] == 0.0 and player_info['z'] == 0.0 and len(player_info['previous']['locations']) == 0:
        first_time = True

    # update the last time we received something from this player
    player_info['timestamp'] = int(round(time.time() * 1000))

    # If the player has not moved just return
    if player_info['x'] == x and player_info['z'] == z:
        return

    # Update the player's position
    player_info['x'] = x
    player_info['z'] = z

    logger.debug(name + ' is at (' + str(x) + ',' + str(z) + ') at ' + timestamp)

    current_locations = trial['semantic_map'].get_locations_containing(x, z, use_updated_map=False)
    current_connections = trial['semantic_map'].get_connections_containing(x, z, use_updated_map=False)

    exiting_locations = []
    exiting_connections = []

    previous_locations = player_info['previous']['locations']
    previous_connections = player_info['previous']['connections']

    for location in previous_locations:
        if location not in current_locations:
            exiting_locations.append(location)
    for connection in previous_connections:
        if connection not in current_connections:
            exiting_connections.append(connection)

    # if nothing has changed, then do not send an update!!
    if not first_time and \
       len(current_locations) == len(previous_locations) and \
       len(current_connections) == len(previous_connections) and \
       len(exiting_locations) == 0 and len(exiting_connections) == 0:
        return

    player_info['previous']['locations'] = current_locations
    player_info['previous']['connections'] = current_connections

    data = {}
    if output_playername and playername is not None:
        data['playername'] = playername
    data['participant_id'] = name
    if callsign is not None:
        data['callsign'] = callsign
    elif 'callsign' in player_info.keys() and player_info['callsign'] is not None:
        data['callsign'] = player_info['callsign']
    data['elapsed_milliseconds'] = elapsed_ms
    data['mission_timer'] = mission_timer
    data['corresponding_observation_number'] = observation_number
    if len(current_locations) <= 0 and len(current_connections) <= 0:
        data['locations'] = [{'id': 'UNKNOWN', 'name': 'The Player is in an Unknown Location!!!'}]
    else:
        if len(current_locations) > 0:
            data['locations'] = []
            for location in current_locations:
                data['locations'].append({'id': location['id'],
                                          'name': location['name'] if 'name' in location.keys() else ''})
        if len(current_connections) > 0:
            data['connections'] = []
            for connection in current_connections:
                data['connections'].append({'id': connection['id'],
                                            'connected_locations': connection['connected_locations']
                                            if 'connected_locations' in connection.keys() else []})
    if len(exiting_locations) > 0:
        data['exited_locations'] = []
        for location in exiting_locations:
            data['exited_locations'].append({'id': location['id'],
                                             'name': location['name'] if 'name' in location.keys() else ''})
    if len(exiting_connections) > 0:
        data['exited_connections'] = []
        for connection in exiting_connections:
            data['exited_connections'].append({'id': connection['id'],
                                               'connected_locations': connection['connected_locations']
                                               if 'connected_locations' in connection.keys() else []})
    logger.debug("current locations: " + str(current_locations))
    logger.debug(data)

    helper.send_msg("observations/events/player/location",
                    "event",
                    "Event:location",
                    "3.0",
                    trial_key=trial_info_key,
                    timestamp=timestamp,
                    data=data)


# MQTT Message callback
#  Called when there is a message on the message bus for a topic which we are subscribed to
def on_message(topic, header, msg, data, mqtt_message):
    global missions, trial_infos, helper, logger

    try:
        message_type = header["message_type"]
        key = helper.get_trial_key(msg)

        sub_type = ''
        if 'sub_type' in msg.keys():
            sub_type = msg['sub_type'].lower()

        # Process Trial Start by initializing the Trial Info and loading the Semantic Map
        if message_type == 'trial':
            map_name = data['map_name'] if 'map_name' in data.keys() else None
            experiment_mission = data['experiment_mission'] if 'experiment_mission' in data.keys() else None

            if sub_type == 'start':
                logger.info('New Trial_id: ' + key + ' using map: ' + map_name)
                trial_infos[key] = {
                    'semantic_map': SemanticMap(),
                    'players': {},
                    'playername2ParticipantId': {}
                }

                if 'client_info' in data.keys():
                    for client in data['client_info']:
                        playername = client['playername'] if 'playername' in client.keys() else None
                        callsign = client['callsign'] if 'callsign' in client.keys() else None
                        participantid = client['participant_id'] if 'participant_id' in client.keys() else None
                        if participantid is None and 'participantid' in client.keys():
                            participantid = client['participantid']
                        if participantid is None:
                            participantid = playername
                        player_info = {'name': playername,
                                       'callsign': callsign,
                                       'participantid': participantid,
                                       'x': 0.0, 'z': 0.0,
                                       'previous': {'locations': [], 'connections': []}}
                        trial_infos[key]['players'][participantid] = player_info
                        trial_infos[key]['playername2ParticipantId'][playername] = participantid

                mission = None
                for mission_prefix in missions.keys():
                    logger.debug(' checking with prefix: ' + mission_prefix.lower())
                    if map_name is not None and map_name.lower().strip() == mission_prefix.lower().strip():
                        mission = missions[mission_prefix]
                        break

                if mission is None:
                    logger.info(' No mapping found for map: ' + map_name)
                    if 'DEFAULT' in missions.keys():
                        mission = missions['DEFAULT']
                        logger.info('   - Using the DEFAULT Map: ' + mission['filename'])
                    else:
                        return

                logger.debug("Loading semanticMap: '" + mission['filename'] + "'")
                trial_infos[key]['mission_file'] = mission['filename']
                trial_infos[key]['semantic_map'].load_semantic_map(
                    os.path.join(helper.config_folder, mission['filename']))
                # post a ground truth semantic map initialized message to the bus
                gt_data = {'semantic_map_name': mission['filename'],
                           'semantic_map': trial_infos[key]['semantic_map'].semantic_map}
                helper.send_msg("ground_truth/semantic_map/initialized",
                                "groundtruth",
                                "SemanticMap:Initialized",
                                "1.0",
                                trial_key=key,
                                timestamp=msg['timestamp'],
                                data=gt_data)
                return

            elif sub_type == 'stop' and key in trial_infos.keys():
                logger.info('Received a stop Trial message for trial:' + key + ' so it has been removed.')
                del trial_infos[key]

        # ignore any message for which I did not receive a trial start message
        if key not in trial_infos.keys():
            return

        if message_type == "observation" and sub_type == 'state':
            timestamp = msg['timestamp']
            name = data['playername'] if 'playername' in data.keys() else None
            pid = data['participant_id'] if 'participant_id' in data.keys() else None
            callsign = data['callsign'] if 'callsign' in data.keys() else None
            elapsed_ms = data['elapsed_milliseconds']
            mission_timer = data['mission_timer']
            observation_number = data['observation_number']
            x = data['x']
            z = data['z']

            check_location_update(key, timestamp, name, pid, callsign, x, z, elapsed_ms, mission_timer, observation_number)

    except Exception as ex:
        logger.error(ex)
        logger.error('RX Error, topic = ' + topic)


# Initialize the Agent Helper
helper = ASISTAgentHelper(on_message)
helper.get_logger().addHandler(LOG_HANDLER)

# initialize data structures
trial_infos = {}
missions = {}
output_playername = False
player_timeout = -1

# see if the config.json file exists and load the maps filename mapping.
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
                        missions = json.load(f)
            elif config['name'] == 'output-playername':
                output_playername = True if config['value'].lower().startswith("t") else False
            elif config['name'] == 'remove-player-info-if-no-events-after-X-seconds':
                player_timeout = int(config['value'])

    except Exception as ex:
        logger.error("Unable to parse config value from config.json.")

logger.debug("output-playername is set to: " + str(output_playername))
logger.debug("player time out set to: " + str(player_timeout))
helper.set_agent_status(helper.STATUS_UP)
logger.info("Starting Agent Loop on a separate thread.")
helper.start_agent_loop_thread()
logger.info("Agent is now running...")

# if the timeout was set, then run a loop to handle player timeouts
if player_timeout > 0:
    while True:
        time_now = int(round(time.time() * 1000))
        trial_keys = list(trial_infos.keys())
        for trial_key in trial_keys:
            if trial_key not in trial_infos.keys():
                continue
            trial_info = trial_infos[trial_key]
            player_keys = list(trial_info['players'])
            for player_key in player_keys:
                if player_key not in trial_info['players'].keys():
                    continue
                player = trial_info['players'][player_key]
                if 'timestamp' in player.keys():
                    last_timestamp = player['timestamp']
                    if time_now > last_timestamp + (player_timeout * 1000):
                        logging.info('- No new info for player: ' + trial_key + ':' + player_key + ' in over ' +
                                     str(player_timeout) + ' seconds so they have been removed.')
                        del trial_info['players'][player_key]
                        if len(trial_info['players']) <= 0:
                            logging.info('- No Players associated with trial:' + trial_key + ' so it has been removed.')
                            del trial_infos[trial_key]
                    # else:
                    #     # TODO: Could output an update here every second if we want to
        time.sleep(1)
