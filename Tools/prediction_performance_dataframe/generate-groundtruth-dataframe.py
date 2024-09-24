from argparse import ArgumentParser
from os.path import join
import pandas as pd
import numpy as np
import copy
import json
import math
import os

NEAREST_DOOR_MAX_RADIUS = 2
PLAYER_PROXIMITY_TO_MB = 2
M7_RESOLUTION_THRESHOLD = 1


def main():
    parser = ArgumentParser(description='get ground truth from trial data')
    parser.add_argument('-d', '--input_dir', type=str, required=True, help='path to dir containing metadata files')
    args = parser.parse_args()

    if not os.path.exists(args.input_dir):
        print('File does not exist')
        return    

    for root, dirs, files in os.walk(args.input_dir):

        dfs = pd.DataFrame(columns=['Trial ID', 'Trial', 'Subject', 'Measure', 'Ground Truth', 'Door ID',\
                                    'Start Elapsed Time', 'resolved_elapsed_time', 'Block Location: X', 'Block Location: Z', 'Block Placed By', 'Block Type'])
        for file in files:
            if file.split('.')[-1] == 'metadata':
                print('scanning', file)

                trial_number = 'N/A'
                trial_id = 'N/A'
                measure = 'N/A'
                subject = 'N/A'
                team = 'N/A'
                ground_truth = 'N/A'
                door_id = 'N/A'
                start_elapsed_time = 'N/A'
                resolved_elapsed_time = 'N/A'
                block_location_x = 'N/A'
                block_location_z = 'N/A'
                placed_by_callsign = 'N/A'
                block_type = 'N/A'
                client_info = {}
                room_list = []
                door_list = []
                M7 = {}

                with open(os.path.join(root, file)) as f:
                    f2 = []
                    for line in f:
                        f2.append(line)
                    f.seek(0)
                    for line in f:
                        metadata = json.loads(line)

                        if metadata['header']['message_type'] == 'trial':
                            trial_id = metadata['msg']['trial_id']
                            trial_number = metadata['data']['trial_number']
                            team = metadata['data']['experiment_name']
                            client_info = metadata['data']['client_info']

                        if 'topic' in metadata.keys():
                            if metadata['topic'] == 'ground_truth/semantic_map/initialized':
                                room_list, door_list = get_semanticmap_data(metadata)
                                # recalculate m7
                                
                                M7 = recalculateM7(f2, room_list, door_list, client_info)
                                measure = 'M7'
                                for item in M7:
                                    subject = item['player_info']['player_name']
                                    door_id = item['marker_block']['nearest_door']['door_properties']['door_id']
                                    ground_truth = item['marker_block']['player_enters_door']
                                    start_elapsed_time = item['marker_block']['start_event_time']
                                    resolved_elapsed_time = item['player_info']['event_time']
                                    block_location_x = item['marker_block']['marker_block_info']['marker_x']
                                    block_location_z = item['marker_block']['marker_block_info']['marker_z']
                                    placed_by_callsign = item['marker_block']['source_callsign']
                                    block_type = item['marker_block']['marker_block_info']['type']

                                    dfs = dfs.append({'Trial ID': trial_id, 'Trial': trial_number, 'Subject': subject, 'Measure': measure, 'Ground Truth': ground_truth,\
                                                      'Door ID': door_id, 'Start Elapsed Time': start_elapsed_time, 'resolved_elapsed_time': resolved_elapsed_time, 'Block Location: X': block_location_x,\
                                                      'Block Location: Z': block_location_z, 'Block Placed By': placed_by_callsign, 'Block Type': block_type}, ignore_index=True)
                                    ground_truth = 'N/A'
                                    enters_door = 'N/A'
                                    start_elapsed_time = 'N/A'
                                    resolved_elapsed_time = 'N/A'
                                    block_location_x = 'N/A'
                                    block_location_z = 'N/A'
                                    placed_by_callsign = 'N/A'
                                    block_type = 'N/A'
                                    door_id = 'N/A'
                                    
                        if metadata['header']['message_type'] == 'groundtruth':
                            if metadata['msg']['source'] == 'Measures_Agent':
                                measure = 'M1'
                                subject = team
                                ground_truth = metadata['data']['M1']['final_score']
                                dfs = dfs.append({'Trial ID': trial_id, 'Trial': trial_number, 'Subject': subject, 'Measure': measure, 'Ground Truth': ground_truth,\
                                                      'Door ID': door_id, 'Start Elapsed Time': start_elapsed_time, 'resolved_elapsed_time': resolved_elapsed_time, 'Block Location: X': block_location_x,\
                                                      'Block Location: Z': block_location_z, 'Block Placed By': placed_by_callsign, 'Block Type': block_type}, ignore_index=True)

                                measure = 'M3'
                                for element in client_info:
                                    subject = element['participant_id']
                                    ground_truth = element['staticmapversion']
                                    dfs = dfs.append({'Trial ID': trial_id, 'Trial': trial_number, 'Subject': subject, 'Measure': measure, 'Ground Truth': ground_truth,\
                                                      'Door ID': door_id, 'Start Elapsed Time': start_elapsed_time, 'resolved_elapsed_time': resolved_elapsed_time, 'Block Location: X': block_location_x,\
                                                      'Block Location: Z': block_location_z, 'Block Placed By': placed_by_callsign, 'Block Type': block_type}, ignore_index=True)
                                
                                measure = 'M6'
                                for element in client_info:
                                    subject = element['participant_id']
                                    ground_truth = element['markerblocklegend']
                                    dfs = dfs.append({'Trial ID': trial_id, 'Trial': trial_number, 'Subject': subject, 'Measure': measure, 'Ground Truth': ground_truth,\
                                                      'Door ID': door_id, 'Start Elapsed Time': start_elapsed_time, 'resolved_elapsed_time': resolved_elapsed_time, 'Block Location: X': block_location_x,\
                                                      'Block Location: Z': block_location_z, 'Block Placed By': placed_by_callsign, 'Block Type': block_type}, ignore_index=True)
                                break

    dfs.to_csv('groundtruth_output.csv', index=False)
    print('predictions saved to groundtruth_output.csv') 


def get_semanticmap_data(metadata):
    room_list = []
    door_list = []

    for room in metadata['data']['semantic_map']['locations']:
        if 'room' in room['type']:
            room_list.append(room['id'])

    for room in metadata['data']['semantic_map']['connections']:
        if 'door' in room['type']:
            door = {}
            door['connected_locations'] = room['connected_locations']
            door['door_id'] = room['id']
            door['bounds'] = room['bounds']['coordinates']
            door_list.append(door)

    return room_list, door_list

def recalculateM7(in_file, room_list, door_list, client_info):
    mb_list = []
    player_mb_actions = []
    active_event_list = {}
    players = []
    player_id_mapping = {}
    call_sign_mapping = {}

    # map callsigns and ids, track current location
    for player in client_info:
        if 'playername' in player.keys():
            player_id_mapping[player['playername']] = player['participant_id']
    for player in client_info:
        active_event_list[player['participant_id']] = []
        call_sign_mapping[player['participant_id']] = player['callsign']

        loc = {}
        loc[player['participant_id']] = None
        players.append(loc)

    p_id = 'UNKNOWN'
    key_type = 'UNKNOWN'

    for line in in_file:
        metadata = json.loads(line)
        # handle playername / participant id
        if 'participant_id' in metadata['data'].keys() or 'playername' in metadata['data'].keys():
            if 'participant_id' not in metadata['data'].keys():
                p_id = player_id_mapping[metadata['data']['playername']]
                key_type = 'playername'
            else:
                p_id = metadata['data']['participant_id']
                key_type = 'participant_id'

        # save players current locations in players array       
        if 'topic' in metadata.keys():
            if metadata['topic'] == 'observations/events/player/location':
                if 'locations' in metadata['data'].keys():
                    for p in players:
                        for k, v in p.items():
                            if k == p_id:
                                p[k] = metadata['data']['locations'][-1]
                        
            elif metadata['topic'] == 'observations/events/player/marker_placed':
                dup = False
                data = metadata['data']
                mb_x = data['marker_x'] + 0.5
                mb_z = data['marker_z'] + 0.5
                nearest_door_distance = NEAREST_DOOR_MAX_RADIUS
                nearest_door = {}
                if 'participant_id' not in data.keys():
                    data['participant_id'] = p_id
                # find closest door to marker block
                for door in door_list:
                    door_x = (door['bounds'][0]['x'] + door['bounds'][1]['x']) / 2
                    door_z = (door['bounds'][0]['z'] + door['bounds'][1]['z']) / 2
                    distance_to_door = math.sqrt(abs(mb_x-door_x)*abs(mb_x-door_x) + abs(mb_z-door_z)*abs(mb_z-door_z))

#                    closest_bb_to_mb_x = min(abs(door['bounds'][0]['x'] - mb_x), abs(door['bounds'][1]['x'] - mb_x))
#                    closest_bb_to_mb_z = min(abs(door['bounds'][0]['z'] - mb_z), abs(door['bounds'][1]['z'] - mb_z))
                    # closest_bb_to_mb_0_x = abs(door['bounds'][0]['x'] - mb_x)
                    # closest_bb_to_mb_0_z = abs(door['bounds'][0]['z'] - mb_z)
                    # closest_bb_to_mb_1_x = abs(door['bounds'][1]['x'] - mb_x)
                    # closest_bb_to_mb_1_z = abs(door['bounds'][1]['z'] - mb_z)
                    # distance_to_door = min(math.sqrt(closest_bb_to_mb_0_x * closest_bb_to_mb_0_x + closest_bb_to_mb_0_z*closest_bb_to_mb_0_z),
                    #                        math.sqrt(closest_bb_to_mb_1_x * closest_bb_to_mb_1_x + closest_bb_to_mb_1_z*closest_bb_to_mb_1_z))
#                    distance_to_door = math.sqrt((closest_bb_to_mb_x * closest_bb_to_mb_x) + (closest_bb_to_mb_z * closest_bb_to_mb_z))
                    
                    if distance_to_door <= nearest_door_distance:
                        nearest_door['door_properties'] = door
                        nearest_door['distance'] = np.around(distance_to_door, 4)
                        nearest_door_distance = distance_to_door

                #check for duplicate marker blocks if not add to list
                for i, block in enumerate(mb_list):
                    for k, v in mb_list[i]['nearest_door'].items():
                        if k == 'door_properties':
                            if 'door_properties' in nearest_door.keys():
                                #handle 'strip of marker blocks' by a door: takes first placed by same player
                                if nearest_door['door_properties']['door_id'] == mb_list[i]['nearest_door']['door_properties']['door_id']:
                                    if data['participant_id'] == mb_list[i]['marker_block_info']['participant_id']:
                                        dup = True
                                        

                    #handle block placed on top of another block
                    if block['marker_block_info']['marker_x'] == data['marker_x'] and block['marker_block_info']['marker_z'] == data['marker_z']:
                        dup = True
                        mb_list[i]['marker_block_info'] = data
                        mb_list[i]['source_callsign'] = call_sign_mapping[data['participant_id']]

                if not dup:
                    marker_block_data = {}
                    marker_block_data['marker_block_info'] = data
                    marker_block_data['nearest_door'] = nearest_door
                    marker_block_data['mb_placed_time'] = data['elapsed_milliseconds']
                    marker_block_data['source_callsign'] = call_sign_mapping[data['participant_id']]
                    mb_list.append(marker_block_data)

            # check if player is near a marker block
            elif metadata['topic'] == 'observations/state':
                data = metadata['data']
                if p_id is not None: # was throwing an error in some training files

                    for block in mb_list:
                        if block['marker_block_info']['participant_id'] != p_id:
                            delta_x = abs(block['marker_block_info']['marker_x'] + 0.5 - data['x'])
                            delta_z = abs(block['marker_block_info']['marker_z']  + 0.5 - data['z'])
                            if math.sqrt(delta_x * delta_x + delta_z * delta_z) <= PLAYER_PROXIMITY_TO_MB:
                                if block['nearest_door'] != {}:
                                    # add to event list

                                    if block not in active_event_list[p_id]:
                                        block['player_enters_door'] = False
                                        block['start_event_time'] = data['elapsed_milliseconds']
                                        # append only if player not in a room
                                        # save players location at the event start time
                                        for p in players:
                                            for k, v in p.items():
                                                if k == p_id:
                                                    if v['id'] not in room_list: 
                                                        # print('event started')
                                                        block['original_location'] = v
                                                        active_event_list[p_id].append(block)

                    # use location monitor to detect changes
                    # checks location is one of the door's connected locations
                    # and checks if the location has changed from time of event
                    # we shouldn't be modifying the list below while we are iterating over it.  
                    #  so, make a list of the indices to be deleted and delete them after the for look.
                    idx_list = []
                    for idx, mb_proximity_event in enumerate(active_event_list[p_id]):
                        # ending_loc = ''
                        for p in players:
                            for k, v in p.items():
                                if k == p_id:
                                    if v['id'] in mb_proximity_event['nearest_door']['door_properties']['connected_locations']:
                                        # ending_loc = v['id']
                                        # print(mb_proximity_event['original_location']['name'], mb_proximity_event['original_location']['id'], '->', v['name'], v['id'])

                                        if v['id'] != mb_proximity_event['original_location']['id']:
                                            # print(mb_proximity_event['original_location']['name'], '->', v['name'])

                                            mb_proximity_event['player_enters_door'] = True

                        delta_x = abs(mb_proximity_event['marker_block_info']['marker_x'] + 0.5 - data['x'])
                        delta_z = abs(mb_proximity_event['marker_block_info']['marker_z'] + 0.5 - data['z'])
                        #Event resolved by leaving area 
                        if math.sqrt(delta_x * delta_x + delta_z * delta_z) > PLAYER_PROXIMITY_TO_MB + M7_RESOLUTION_THRESHOLD:
                            # print('event resolved')
                            #add this idx to a list to remove later
                            idx_list.append(idx)
                            resolved_block = active_event_list[p_id][idx]
                            measure_obj = {}
                            player_obj = {}
                            player_obj['player_name'] = p_id
                            player_obj['event_time'] = data['elapsed_milliseconds']
                            measure_obj['player_info'] = player_obj
                            measure_obj['marker_block'] = copy.deepcopy(resolved_block)

                            player_mb_actions.append(measure_obj)

                    #now removed the items from the list that should be removed
                    off_set = 0
                    for index in idx_list:
                        # active_event_list[p_id].pop(index-off_set)
                        del active_event_list[p_id][index-off_set]
                        off_set = off_set + 1

                    # print('player', p_id, 'goes through door: ', resolved_block['player_enters_door'])
                            # print('marker block placed by', resolved_block['marker_block_info']['participant_id'], 'color', resolved_block['marker_block_info']['type'])
                            # print('at location', resolved_block['marker_block_info']['marker_x'], ',', resolved_block['marker_block_info']['marker_z'], 'start time of event', round(resolved_block['start_event_time'] / 1000 // 60 , 1))
                            # print('starting location', mb_proximity_event['original_location']['id'], 'ending location', ending_loc, 'mb placed at', round(resolved_block['mb_placed_time'] / 1000 // 60 , 1))
    return player_mb_actions


if __name__ == '__main__':
    main()
