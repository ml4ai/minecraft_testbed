from argparse import ArgumentParser
from os.path import join
from operator import itemgetter
import numpy as np
import math
import json
import os

NUM_SECONDS_DOOR_M2 = 2
NUM_PLAYERS = 3
POINTS_GREEN = 10
POINTS_YELLOW = 30

def main():
    # command line arguments -f 'inputfile.metadata'
    parser = ArgumentParser(description='get ground truth from trial data')
    parser.add_argument('-f', '--input_file', type=str, required=True, help='path to trial metadata file')
    args = parser.parse_args()

    if not os.path.exists(args.input_file):
        print('File does not exist')
        return    

    header = {}
    measures = {}
    measures['M1'] = {}
    measures['M2'] = {}
    measures['M3'] = {}
    measures['M4'] = {}
    measures['M5'] = {}

    messages = []
    with open(args.input_file) as f:
        print('Scanning Trial Data..\n')
        for line in f:
            messages.append(json.loads(line))

    room_list = scan_room_id(messages)

    measures['study_number'], measures['trial_number'], measures['experiment_name'] = get_trial_info(messages)
    measures['M1']['gt_final_score'] = scan_m1(messages)
    measures['M2']['n_value'] = NUM_SECONDS_DOOR_M2
    measures['M2']['post_room_exit_locations'] = scan_m2(messages, NUM_SECONDS_DOOR_M2, room_list)    
    measures['M3'] = scan_m3(messages)
    measures['M4']['hvt_victims'], measures['M4']['trial_loiter_stats'] = scan_m4(messages)
    measures['M5']['rooms_visited'], measures['M5']['total_revisits'] = scan_m5(messages, room_list)

    with open(f"NotHSRData_Measurements_Study-{measures['study_number']}"
              f"-Pilot_Trial-{measures['trial_number']}"
              f"_Team-{measures['experiment_name']}.json", "w") as write_file:
        json.dump(measures, write_file, indent=4)

def get_trial_info(messages):

    for message in messages:
        if message['msg']['sub_type'] == 'start':
            return message['data']['study_number'], message['data']['trial_number'], message['data']['experiment_name']
        
def scan_room_id(messages):
    room_list = []

    for message in messages:
        if message['msg']['sub_type'] == 'SemanticMap:Initialized':
            for room in  message['data']['semantic_map']['locations']:
                if room['type'] == 'room':
                    room_list.append(room['id'])
    return room_list


# Get the Final Score
def scan_m1(messages):
    print('Running M1...')
    gt_final_score = 0
    for message in messages:
        if message['msg']['sub_type'] == 'Event:Triage':
            if message['data']['triage_state'] == 'SUCCESSFUL':
                if message['data']['color'].lower() == 'Yellow'.lower():
                    gt_final_score = gt_final_score + POINTS_YELLOW
                if message['data']['color'].lower() == 'Green'.lower():
                    gt_final_score = gt_final_score + POINTS_GREEN


        # if message['msg']['sub_type'] == 'Event:Scoreboard':
        #     gt_final_score = message['data']['scoreboard']['TeamScore']
    return gt_final_score


# Get position n seconds after leaving a room
# x, and z after n seconds are relative to origin at the point event was triggered
def scan_m2(messages, seconds, room_list):
    print('Running M2...')

    # ignore y (2d)
    x = 0
    z = 0
    start_time = 0
    player_name = ''
    events = []
    event_triggered = False
    mission_started = False

    for message in messages:
        # store trigger event at exited_locations is of type room
        if message['msg']['sub_type'] == 'Event:location':
            if message['data']['mission_timer'] == 'Mission Timer not initialized.':
                continue
            if 'exited_locations' in message['data'].keys() and message['data']['exited_locations'][0]['id'] in room_list:
                room_name = message['data']['exited_locations'][0]['name']
                event_timestamp = message['data']['elapsed_milliseconds']
                event_triggered = True
                x = None
                z = None
                
        if event_triggered:
            
            # get x,z and time and player name at event
            # if message['msg']['sub_type'] == 'state':

                # -z axis == N relative to client map
                #  z axis == S relative to client map
                # -x axis == W relative to client map
                #  x axis == E relative to client map
                # x = message['data']['x']
                # z = message['data']['z'] * -1
            start_time = message['data']['elapsed_milliseconds']
            player_name = message['data']['playername']

            # Fast-forward n seconds, skip messages pre mission start where elapsed_millis not reset
            for seek_message in messages:
                if seek_message['msg']['sub_type'] == 'Event:MissionState':
                    if seek_message['data']['mission_state'] == 'Start':
                        mission_started = True

                if mission_started:
                    if seek_message['msg']['sub_type'] == 'state':

                        if player_name == seek_message['data']['playername']:
                            
                            if seek_message['data']['elapsed_milliseconds'] >= start_time:
                                if not x and not z:
                                    x = seek_message['data']['x']
                                    z = seek_message['data']['z'] * -1

                            if seek_message['data']['elapsed_milliseconds'] >= (seconds * 1000) + start_time:
                                event = {}
                                event['time_elapsed_milliseconds'] = event_timestamp
                                event['player_name'] = player_name
                                event['room_name'] = room_name
                                delta_x = seek_message['data']['x'] - x
                                delta_z = (seek_message['data']['z'] * -1) - z
                                
                                # event['yaw'] = seek_message['data']['yaw']
                                # event['pitch'] = seek_message['data']['pitch']
                                # event['magnitude'] = math.sqrt((delta_x * delta_x) + (delta_z * delta_z))
                                # angle in degrees relative to x axis 0 - 360 (0 = E, 90 = N, 180 = W, 270 = S)
                                # cardinal directions include upper and lower bounds
                                direction = (math.atan2(delta_z , delta_x) * (180 / math.pi))
                                unsigned = direction + 360 if direction < 0 else direction
                                event['angle'] = np.around(unsigned, 2)
                                if unsigned <= 22.5 or unsigned >= 337.5:
                                    event['direction'] = 'E'
                                if unsigned > 22.5 and unsigned < 67.5:
                                    event['direction'] = 'NE'
                                if unsigned >= 67.5 and unsigned <= 112.5:
                                    event['direction'] = 'N'
                                if unsigned > 112.5 and unsigned < 157.5:
                                    event['direction'] = 'NW'
                                if unsigned >= 157.5 and unsigned <= 202.5:
                                    event['direction'] = 'W'
                                if unsigned > 202.5 and unsigned < 247.5:
                                    event['direction'] = 'SW'
                                if unsigned >= 247.5 and unsigned <= 292.5:
                                    event['direction'] = 'S'
                                if unsigned > 292.5 and unsigned < 337.5:
                                    event['direction'] = 'SE'
                                events.append(event)
                                mission_started = False
                                event_triggered = False
                                break

    return events


def scan_m3(messages):
    print('Running M3...')

    player_maps = []
    # for message in messages:
    player_map = {}
    player_map['player_name'] = ''
    player_map['map_name'] = ''

    player_maps.append(player_map)
    return player_maps


# get max loiter time for hvt
def scan_m4(messages):
    print('Running M4...')

    players_present = []
    victims = []
    times = []
    victim_stats = {}
    trial_stats = []
    loiter_stats = {}
    
    for message in messages:
        # if 3 present calc max diff of arrival time
        if len(players_present) is NUM_PLAYERS:
            player_arrival = {}
            victim = {}
            location = players_present[0]['victim_location']
            same_location = True
            for player in players_present:
                player_arrival[player['player_name']] = player['arrival_time_elapsed_milliseconds']
                # check if at same victim / location
                if player['victim_location'] != location:
                    same_location = False
            victim['victim_location'] = players_present[0]['victim_location']
            victim['loiter_time'] = (max(list(player_arrival.values())) - min(list(player_arrival.values()))) / 1000
            victim['player_arrivals'] = player_arrival
            if same_location:
                times.append(victim['loiter_time'])
                victims.append(victim)
            players_present = []
        # add to list if enter range, pop if left
        if message['msg']['sub_type'] == 'Event:ProximityBlockInteraction':
            player_state = {}
            if message['data']['action_type'] == 'LEFT_RANGE':
                players_present = [player for player in players_present if player['player_name'] != message['data']['playername']]
            if message['data']['action_type'] == 'ENTERED_RANGE':
                player_state['victim_location'] = {}
                player_state['victim_location']['x'] = message['data']['victim_x']
                player_state['victim_location']['z'] = message['data']['victim_z']
                player_state['player_name'] = message['data']['playername']
                player_state['arrival_time_elapsed_milliseconds'] = message['data']['elapsed_milliseconds']
                players_present.append(player_state)

    if times:
        loiter_stats['max'] = max(times)
        loiter_stats['min'] = min(times)
        loiter_stats['avg'] = np.around(np.mean(times), 4)

    return victims, loiter_stats


def scan_m5(messages, room_list):
    print('Running M5...')
    total_revisits = 0
    medical_revisits = 0
    hazard_revisits = 0
    search_revisits = 0
    players = {}
    rooms = {}
    
    for message in messages:
        # keep player's curent role up to date
        if message['msg']['sub_type'] == 'Event:RoleSelected':
            if message['data']['playername'] not in players:
                players[message['data']['playername']] = {}
            players[message['data']['playername']] = message['data']['new_role']
    
        # check if current location is a room
        if message['msg']['sub_type'] == 'Event:location':
            if message['data'].get('locations'):
                if message['data']['locations'][0]['id'] in room_list:
                    room_id = message['data']['locations'][0]['id']

                    if room_id not in rooms:
                        rooms[room_id] = {}
                        rooms[room_id]['room_name'] = message['data']['locations'][0]['name']
                        rooms[room_id]['Medical_Specialist'] = 0
                        rooms[room_id]['Search_Specialist'] = 0
                        rooms[room_id]['Hazardous_Material_Specialist'] = 0
                        rooms[room_id]['visitors'] = []

                    current_visitor = {}
                    current_visitor['player'] = {}
                    current_visitor['player']['name'] = message['data']['playername']

                    # check if duplate visit
                    # p[0] = name p[1] = role
                    for p in players.items():
                        if p[0] == current_visitor['player']['name']:
                            current_visitor['player']['role'] = p[1]
                            current_visitor['time_elapsed_milliseconds'] = message['data']['elapsed_milliseconds']
                            if current_visitor['player'] not in map(itemgetter('player'), rooms[room_id]['visitors']):
                            # if current_visitor['player'] not in rooms[room_id]['visitors']:
                                rooms[room_id]['visitors'].append(current_visitor)
                                current_val = rooms[room_id][p[1]]
                                rooms[room_id][p[1]] = current_val + 1

    # count totals excluding staging area
    for k, v in rooms.items():
        if  k == 'sga':
            continue
        if v['Medical_Specialist'] > 1:
            medical_revisits = medical_revisits + (v['Medical_Specialist'] - 1)
            total_revisits = total_revisits + (v['Medical_Specialist'] - 1)
        if v['Search_Specialist'] > 1:
            search_revisits = search_revisits + (v['Search_Specialist'] - 1)
            total_revisits = total_revisits + (v['Search_Specialist'] - 1)
        if v['Hazardous_Material_Specialist'] > 1:
            hazard_revisits = hazard_revisits + (v['Hazardous_Material_Specialist'] - 1)
            total_revisits = total_revisits + (v['Hazardous_Material_Specialist'] - 1)

    revisits = {}
    revisits['medical_revisits'] = medical_revisits
    revisits['search_revisits'] = search_revisits
    revisits['hazard_revisits'] = hazard_revisits
    revisits['total_revisits'] = total_revisits

    return rooms, revisits

if __name__ == '__main__':
    main()