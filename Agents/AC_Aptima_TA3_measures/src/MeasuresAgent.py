#!/usr/bin/env python3

import os
import json
import numpy as np
import math
import copy
import logging
from asistagenthelper import ASISTAgentHelper
from operator import itemgetter

trial_infos = {}

NUM_PLAYERS = 3
VERSION = '3.5.1'

CRITICAL_POINT_VALUE = 50
NORMAL_POINT_VALUE = 10
MILLISECONDS_PER_MINUTE = 60000

# mission millis go to -1 when stopped so need a value currently 17 mins
MILLISECONDS_PER_MISSION = 1020000

victims_by_room = []
discovered_victims = []

team_score = 0
total_victim_count = 0
total_potential_score = 0

perturbation_stats = {}
trapped_players = []

player_locations = {}

# This is the function which is called when a message is received for a to
# topic which this Agent is subscribed to.
def on_message(topic, header, msg, data, mqtt_message):

    global victims_by_room
    global discovered_victims
    global trapped_players

    global team_score
    global total_victim_count
    global total_potential_score

    # Now handle the message based on the topic.  Refer to Message Specs for the contents of header, msg, and data
    if topic == 'trial':
        if msg['sub_type'] == 'start':
            print('trial started')
            print(victims_by_room)
            print(discovered_victims)
            # handle the start of a trial!!
            trial_info = data
            trial_info['experiment_id'] = msg['experiment_id']
            trial_info['trial_id'] = msg['trial_id']
            trial_info['replay_id'] = msg['replay_id'] if 'replay_id' in msg.keys() else None
            trial_info['replay_root_id'] = msg['replay_root_id'] if 'replay_root_id' in msg.keys() else None

            trial_key = trial_info['trial_id']
            if 'replay_id' in trial_info and not trial_info['replay_id'] is None:
                trial_key = trial_key + ":" + trial_info['replay_id']
            trial_infos[trial_key] = trial_info
            
            # reset measures at trial start
            team_score = 0
            total_victim_count = 0
            total_potential_score = 0
            perturbation_stats.clear()
            trapped_players = []
            player_locations.clear()

        if msg['sub_type'] == 'stop':
            print('trial stopped')
            trial_key = msg['trial_id']
            if 'replay_id' in msg and not msg['replay_id'] is None:
                trial_key = trial_key + ":" + msg['replay_id']
            if trial_key in trial_infos.keys():
                trial_info = trial_infos[trial_key]

                # for testing, publish at mission stop
                # publish_M1(msg['timestamp'], elapsed_milli=MILLISECONDS_PER_MISSION, event_type='event', message_type='trial', sub_type='stop')
                # publish_M2(msg['timestamp'], elapsed_milli=MILLISECONDS_PER_MISSION, event_type='event', message_type='trial', sub_type='stop')
                # publish_M3(msg['timestamp'], elapsed_milli=MILLISECONDS_PER_MISSION, event_type='event', message_type='trial', sub_type='stop')
                # publish_M4(msg['timestamp'], elapsed_milli=MILLISECONDS_PER_MISSION, event_type='event', message_type='trial', sub_type='stop', p_stats=perturbation_stats)

                team_score = 0
                total_victim_count = 0
                total_potential_score = 0
                perturbation_stats.clear()
                trapped_players = []
                victims_by_room = []
                discovered_victims = []
                player_locations.clear()


    elif topic == 'observations/events/mission':
        if data['mission_state'] == 'Stop':
            print('Mission stopped')
            # handle no perturbation
            if 'pre_pertubation_score' not in perturbation_stats.keys():
                perturbation_stats['pre_pertubation_score'] = team_score
                perturbation_stats['pre_pertubation_period'] = MILLISECONDS_PER_MISSION
                perturbation_stats['pre_pertubation_points_available'] = total_potential_score
                print('no perturbation found', perturbation_stats)

            perturbation_stats['post_pertubation_score'] = team_score - perturbation_stats['pre_pertubation_score']
            perturbation_stats['post_pertubation_period'] = MILLISECONDS_PER_MISSION - perturbation_stats['pre_pertubation_period']
            perturbation_stats['post_pertubation_points_available'] = total_potential_score - perturbation_stats['pre_pertubation_score']

            publish_M1(msg['timestamp'], elapsed_milli=MILLISECONDS_PER_MISSION, event_type='event', message_type='trial', sub_type='stop')
            publish_M2(msg['timestamp'], elapsed_milli=MILLISECONDS_PER_MISSION, event_type='event', message_type='trial', sub_type='stop')
            publish_M3(msg['timestamp'], elapsed_milli=MILLISECONDS_PER_MISSION, event_type='event', message_type='trial', sub_type='stop')
            publish_M4(msg['timestamp'], elapsed_milli=MILLISECONDS_PER_MISSION, event_type='event', message_type='trial', sub_type='stop', p_stats=perturbation_stats)
            publish_M14(msg['timestamp'], elapsed_milli=MILLISECONDS_PER_MISSION , event_type='event', message_type='trial', sub_type='stop', recent_exit=None)

            team_score = 0
            total_victim_count = 0
            total_potential_score = 0
            perturbation_stats.clear()
            victims_by_room = []
            discovered_victims = []
            trapped_players = []
            player_locations.clear()

    # Calculate ASI-M1
    elif topic == 'observations/events/scoreboard':
        print('Scoreboard updated - TeamScore: ', data['scoreboard']['TeamScore'])
        trial_key = msg['trial_id']
        if 'replay_id' in msg and not msg['replay_id'] is None:
            trial_key = trial_key + ":" + msg['replay_id']
        if trial_key in trial_infos.keys():
            trial_info = trial_infos[trial_key]
            team_score = data['scoreboard']['TeamScore']

    # group victims for each room
    elif topic == 'ground_truth/mission/victims_list':
        print('getting victim list')
        total_victim_count = 0
        total_potential_score = 0

        total_victim_count = len(data['mission_victim_list'])
        for victim in data['mission_victim_list']:
            # print(victim['unique_id'], victim['room_name'])

            if 'proximity' in victim['block_type']:
                total_potential_score = total_potential_score + CRITICAL_POINT_VALUE
            else:
                total_potential_score = total_potential_score + NORMAL_POINT_VALUE

            victim_object = {}
            victim_object['room_name'] = victim['room_name']
            victim_object['unique_id'] = victim['unique_id']
            victim_object['discovery_time'] = 0
            victim_object['rescue_time'] = 0            
            victim_object['rescued'] = False
            victims_by_room.append(victim_object)

        print('Number of Victims:', total_victim_count, 'Points:', total_potential_score)

    elif topic == 'observations/events/player/triage':

        if data['triage_state'] == 'SUCCESSFUL':
            roomname = ''
            for victim in victims_by_room:
                if victim['unique_id'] == data['victim_id']:
                    roomname = victim['room_name']
            victim_object = {}
            victim_object['room_name'] = roomname
            victim_object['unique_id'] = data['victim_id']
            victim_object['discovery_time'] = data['elapsed_milliseconds']
            victim_object['rescue_time'] = 0            
            victim_object['rescued'] = False

            new_victim = True
            for victim in discovered_victims:
                if victim['unique_id'] == victim_object['unique_id']:
                    new_victim = False
            if new_victim:
                discovered_victims.append(victim_object)
                print('Medic Discovered a Victim! Total:', len(discovered_victims))
                publish_M3(msg['timestamp'], elapsed_milli=data['elapsed_milliseconds'], event_type='event', message_type='event', sub_type='Event:Triage')

    # listen for beeps
    elif topic == 'observations/events/player/signal':
        print('signal triggered - ROOM NAME: ', data['roomname'])
        for victim in victims_by_room:
            if victim['room_name'] == data['roomname']:
                new_victim = True
                for disc_victim in discovered_victims:
                    if victim['unique_id'] == disc_victim['unique_id']:
                        new_victim = False
                if new_victim:
                    victim_object = {}
                    victim_object['room_name'] = data['roomname']
                    victim_object['unique_id'] = victim['unique_id']
                    victim_object['discovery_time'] = data['elapsed_milliseconds']
                    victim_object['rescue_time'] = 0            
                    victim_object['rescued'] = False
                    discovered_victims.append(victim_object)
                    print('Signal Discovered a Victim! Total:', len(discovered_victims))
                    publish_M3(msg['timestamp'], elapsed_milli=data['elapsed_milliseconds'], event_type='event', message_type='event', sub_type='Event:Signal')

    elif topic == 'observations/events/player/victim_evacuated' or topic == 'observations/events/server/victim_evacuated':
        if data['success'] == True:
            for discovered_victim in discovered_victims:
                if discovered_victim['unique_id'] == data['victim_id']:

                    discovered_victim['rescue_time'] = data['elapsed_milliseconds']
                    discovered_victim['rescued'] = True
                    print('victim evacuated', discovered_victim)

            publish_M2(msg['timestamp'], elapsed_milli=data['elapsed_milliseconds'], event_type='event', message_type='event', sub_type='Event:VictimEvacuated')
            publish_M3(msg['timestamp'], elapsed_milli=data['elapsed_milliseconds'], event_type='event', message_type='event', sub_type='Event:VictimEvacuated')


    elif topic == 'observations/events/mission/perturbation':
        if data['mission_state'] == 'start':
            perturbation_stats['pre_pertubation_score'] = team_score
            perturbation_stats['pre_pertubation_period'] = data['elapsed_milliseconds']
            perturbation_stats['pre_pertubation_points_available'] = total_potential_score
            print('PerturbationStart', perturbation_stats)

            publish_M4(msg['timestamp'], elapsed_milli=data['elapsed_milliseconds'] , event_type='event', message_type='event', sub_type='Event:Perturbation', p_stats=perturbation_stats)

    elif topic == 'observations/events/player/rubble_collapse' or topic == 'observations/events/server/rubble_collapse':
            
        trapped_player = {}
        trapped_player['id'] = data['participant_id']
        trapped_player['room_id'] = player_locations[data['participant_id']]
        trapped_player['start_time'] = data['elapsed_milliseconds']
        trapped_player['end_time'] = 0
        trapped_player['trapped'] = True
        print(trapped_player['id'], 'trapped at location:', trapped_player['room_id'])

        trapped_players.append(trapped_player)

    elif topic == 'observations/events/player/location':
        # trach each players location
        if 'locations' in data.keys():
            player_locations[data['participant_id']] = data['locations'][0]['id']
        else:
            player_locations[data['participant_id']] = 'UNKNOWN'

        if len(trapped_players) > 0:
            for player in trapped_players:
                if player['id'] == data['participant_id'] and player['trapped'] == True:
                    if 'exited_locations' in data.keys():
                        for p in data['exited_locations']:
                            if player['room_id'] == p['id']:
                                player['trapped'] = False
                                player['end_time'] = data['elapsed_milliseconds']
                                publish_M14(msg['timestamp'], elapsed_milli=data['elapsed_milliseconds'] , event_type='event', message_type='event', sub_type='Event:Location', recent_exit=player)
                                print(player['id'], 'exited trap after', player['end_time'] - player['start_time'], 'milliseconds')



    

def publish_M1(timestamp, elapsed_milli, event_type, message_type, sub_type):

    m1_data = {}
    m1_data['study_version'] = "3"
    m1_data['elapsed_milliseconds'] = elapsed_milli
    m1_data['event_properties'] = {}
    m1_data['event_properties']['qualifying_event_type'] = event_type
    m1_data['event_properties']['qualifying_event_message_type'] = message_type
    m1_data['event_properties']['qualifying_event_sub_type'] = sub_type
    
    m1_data['measure_data'] = []

    measure_data = {}
    measure_data['measure_id'] = 'ASI-M1'
    measure_data['datatype'] = 'integer'
    measure_data['measure_value'] = team_score
    measure_data['description'] = 'ASI Utility'
    measure_data['additional_data'] = {}

    m1_data['measure_data'].append(measure_data)

    helper.send_msg("agent/measures/AC_Aptima_TA3_measures",
                            "agent",
                            "measures",
                            VERSION,
                            timestamp,
                            m1_data
                            )
    print('[M1]', message_type, sub_type, 'Value:', m1_data['measure_data'][0]['measure_value'])


def publish_M2(timestamp, elapsed_milli, event_type, message_type, sub_type):

    avg_rescue_time = 0.0
    successful_rescues_times = []
    for victim in discovered_victims:
        if victim['rescued'] == True:
            time = 0.0
            time = victim['rescue_time'] - victim['discovery_time']
            successful_rescues_times.append(time)

    if len(successful_rescues_times) > 0:
        avg_rescue_time = np.around(np.mean(successful_rescues_times), 4)
    else:
        avg_rescue_time = 0.0


    m2_data = {}
    m2_data['study_version'] = "3"
    m2_data['elapsed_milliseconds'] = elapsed_milli
    m2_data['event_properties'] = {}
    m2_data['event_properties']['qualifying_event_type'] = event_type
    m2_data['event_properties']['qualifying_event_message_type'] = message_type
    m2_data['event_properties']['qualifying_event_sub_type'] = sub_type
    
    m2_data['measure_data'] = []
    measure_data = {}
    measure_data['measure_id'] = 'ASI-M2'
    measure_data['datatype'] = 'double'
    measure_data['measure_value'] = avg_rescue_time
    measure_data['description'] = 'Synchronization'
    measure_data['additional_data'] = discovered_victims

    m2_data['measure_data'].append(measure_data)


    helper.send_msg("agent/measures/AC_Aptima_TA3_measures",
                            "agent",
                            "measures",
                            VERSION,
                            timestamp,
                            m2_data
                            )
    print('[M2]', message_type, sub_type, 'Value:', m2_data['measure_data'][0]['measure_value'])


def publish_M3(timestamp, elapsed_milli, event_type, message_type, sub_type):

    victims_discovered = len(discovered_victims)
    rescued_victims = 0
    for victim in discovered_victims:
        if victim['rescued'] == True:
            rescued_victims = rescued_victims + 1

    m3_data = {}
    m3_data['study_version'] = "3"
    m3_data['elapsed_milliseconds'] = elapsed_milli
    m3_data['event_properties'] = {}
    m3_data['event_properties']['qualifying_event_type'] = event_type
    m3_data['event_properties']['qualifying_event_message_type'] = message_type
    m3_data['event_properties']['qualifying_event_sub_type'] = sub_type
    
    m3_data['measure_data'] = []
    measure_data = {}
    measure_data['measure_id'] = 'ASI-M3'
    measure_data['datatype'] = 'double'
    div = 0
    if victims_discovered != 0:
        div = rescued_victims / victims_discovered
    measure_data['measure_value'] = np.around(1 - div, 4)
    measure_data['description'] = 'Error Rate'
    measure_data['additional_data'] = {}
    measure_data['additional_data']['victims_rescued'] = rescued_victims
    measure_data['additional_data']['victims_discovered'] = victims_discovered
    
    m3_data['measure_data'].append(measure_data)


    helper.send_msg("agent/measures/AC_Aptima_TA3_measures",
                            "agent",
                            "measures",
                            VERSION,
                            timestamp,
                            m3_data
                            )
    print('[M3]', message_type, sub_type, 'Value:', m3_data['measure_data'][0]['measure_value'])


def publish_M4(timestamp, elapsed_milli, event_type, message_type, sub_type, p_stats):

    adaptation_score = 0.0

    m4_data = {}
    m4_data['study_version'] = "3"
    m4_data['elapsed_milliseconds'] = elapsed_milli
    m4_data['event_properties'] = {}
    m4_data['event_properties']['qualifying_event_type'] = event_type
    m4_data['event_properties']['qualifying_event_message_type'] = message_type
    m4_data['event_properties']['qualifying_event_sub_type'] = sub_type
    m4_data['measure_data'] = []

    if 'post_pertubation_score' not in p_stats.keys() \
        or p_stats['post_pertubation_period'] == 0 \
        or p_stats['post_pertubation_points_available'] == 0 \
        or p_stats['pre_pertubation_period'] == 0 \
        or p_stats['pre_pertubation_points_available'] == 0: # div by 0
        adaptation_score = 0.0
    else:
        top = (p_stats['post_pertubation_score'] / (p_stats['post_pertubation_period'] / MILLISECONDS_PER_MINUTE)) / p_stats['post_pertubation_points_available']
        bottom =  (p_stats['pre_pertubation_score'] / (p_stats['pre_pertubation_period'] / MILLISECONDS_PER_MINUTE)) / p_stats['pre_pertubation_points_available']
        adaptation_score = np.around(top / bottom, 4)
    measure_data = {}
    measure_data['measure_id'] = 'ASI-M4'
    measure_data['datatype'] = 'double'
    measure_data['measure_value'] = adaptation_score
    measure_data['description'] = 'Adaptation / Resilience'
    measure_data['additional_data'] = p_stats

    m4_data['measure_data'].append(measure_data)

    helper.send_msg("agent/measures/AC_Aptima_TA3_measures",
                            "agent",
                            "measures",
                            VERSION,
                            timestamp,
                            m4_data
                            )
    print('[M4]', message_type, sub_type, 'Value:', m4_data['measure_data'][0]['measure_value'])

def publish_M14(timestamp, elapsed_milli, event_type, message_type, sub_type, recent_exit):
    
    time_trapped = 0
    desc = 'Risk'
    m_data = trapped_players
    if recent_exit:
        m_data = recent_exit
        time_trapped = recent_exit['end_time'] - recent_exit['start_time']
    else:
        desc = desc + ' (sum)'
        for trapped in trapped_players:
            if trapped['trapped'] == False:
                time_trapped = time_trapped + (trapped['end_time'] - trapped['start_time'])


    m14_data = {}
    m14_data['study_version'] = "3"
    m14_data['elapsed_milliseconds'] = elapsed_milli
    m14_data['event_properties'] = {}
    m14_data['event_properties']['qualifying_event_type'] = event_type
    m14_data['event_properties']['qualifying_event_message_type'] = message_type
    m14_data['event_properties']['qualifying_event_sub_type'] = sub_type
    
    m14_data['measure_data'] = []

    measure_data = {}
    measure_data['measure_id'] = 'ASI-M14'
    measure_data['datatype'] = 'integer'
    measure_data['measure_value'] = time_trapped
    measure_data['description'] = desc
    measure_data['additional_data'] = m_data

    m14_data['measure_data'].append(measure_data)

    helper.send_msg("agent/measures/AC_Aptima_TA3_measures",
                            "agent",
                            "measures",
                            VERSION,
                            timestamp,
                            m14_data
                            )
    print('[M14]', message_type, sub_type, 'Value:', m14_data['measure_data'][0]['measure_value'])#, m14_data['measure_data'][0]['additional_data'])


# Agent Initialization
helper = ASISTAgentHelper(on_message)

# Set the helper's logging level to INFO
LOG_HANDLER = logging.StreamHandler()
LOG_HANDLER.setFormatter(logging.Formatter("%(asctime)s | %(name)s | %(levelname)s — %(message)s"))
helper.get_logger().setLevel(logging.INFO)
helper.get_logger().addHandler(LOG_HANDLER)
logger = logging.getLogger("MeasuresAgent")
logger.setLevel(logging.INFO)
logger.addHandler(LOG_HANDLER)

# Set the agents status to 'up' and start the agent loop on a separate thread
helper.set_agent_status(helper.STATUS_UP)
logger.info("Starting Agent Loop on a separate thread.")
helper.start_agent_loop_thread()
logger.info("Agent is now running...")