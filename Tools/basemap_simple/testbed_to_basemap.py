#!/usr/bin/env python3

import argparse
import sys
import math
import json
import os
from os.path import join

mcworldlib_filename = 'MCWorldlib.egg'
sys.path.append(mcworldlib_filename)
import mcworldlib as mc

default_json_file = 'blocks_in_building.json'
maps_base = 'Local/CLEAN_MAPS/'
testbed = os.getenv('asist_testbed')
if testbed is None:
    # see if it is relative to where we are running
    if os.path.exists(join ('../..', maps_base)):
        testbed = '../../'
    else:
        print('Environment value `asist_testbed` is required. Got:', testbed)
        sys.exit(1)


def make_world_path(world_name):
    return join(testbed, maps_base, world_name)


def process_region(region, region_blocks, ranges, all_blocks={}, block_dict={}):
    x_low, x_high, z_low, z_high, y_low, y_high = ranges

    # ---------------------------------------------------------
    # compute the region based coordinates
    x_ind_low = int(x_low / 16 - region[0] * 32)  # int((2560 + x_low)/16)
    x_ind_high = int(x_high / 16 - region[0] * 32)
    z_ind_low = int(z_low / 16 - region[1] * 32)
    z_ind_high = int(z_high / 16 - region[1] * 32)
    y_ind_low = math.floor(y_low / 16)
    y_ind_high = math.floor(y_high / 16) + 1

    y_i_low = int(y_low - y_ind_low * 16)
    y_i_high = int(y_high - y_ind_low * 16)

    # print('region: ' + str(region))
    # print(x_ind_low, x_ind_high, z_ind_low, z_ind_high, y_ind_low, y_ind_high)

    # ---------------------------------------------------------
    # read all blocks in region and store in all_blocks, where 'x' 'y' 'z' specifies patch index
    # e.g., all_blocks[(-2176, 52, 144)] = {'block_type': 'air', 'y': 4, 'z': 0, 'x': 0}
    for x_ind in range(x_ind_low, x_ind_high+1):
        for z_ind in range(z_ind_low, z_ind_high+1):
            # only process region blocks which are in the specified range
            if (x_ind, z_ind) not in region_blocks.keys():
                continue

            # print('  - len sections: ' + str(len(region_blocks[x_ind, z_ind]['']['Level']['Sections'])))

            for y_ind in range(y_ind_low, y_ind_high+1):
                if y_ind >= len(region_blocks[x_ind, z_ind]['']['Level']['Sections']):
                    continue

                blocks = region_blocks[x_ind, z_ind]['']['Level']['Sections'][y_ind]['Blocks']
                blocks = list(blocks)

                tile_entities = region_blocks[x_ind, z_ind]['']['Level']['TileEntities']
                tile_entities = list(tile_entities)

                data_bytes = region_blocks[x_ind, z_ind]['']['Level']['Sections'][y_ind]['Data']
                data_bytes = list(data_bytes)

                # offsets in the game world
                x_0 = 16 * (x_ind + region[0]*32)
                y_0 = 16 * y_ind
                z_0 = 16 * (z_ind + region[1]*32)

                print('region: ' + str(region) + ' - (' + str(x_ind) + ', ' + str(z_ind) + ') -> (' + str(x_0) + ', ' + str(y_0) + ', ' + str(z_0) + ') nb = ' + str(len(blocks)))

                # store all blocks in an array to be printed on a 16 by 16 image
                for i in range(len(blocks)):
                    # to be stored about each block
                    stats = {}

                    # 'block_type'
                    num = int(blocks[i])
                    if num < 0:
                        num = 256+num
                    stats['block_type'] = block_dict[num]

                    # if num != 0:
                    #     print('  block_type = ' + stats['block_type'])

                    # data that specifies block state and direction
                    # see the MineCraft wiki for info on what each bit means for each block
                    # doors - https://minecraft.gamepedia.com/Door#Block_data
                    # levers - https://minecraft.gamepedia.com/Lever#Block_data
                    data = int(data_bytes[int(i/2)])
                    if i % 2 != 0:
                        data = data >> 4
                    stats['data'] = data & 0xF

                    # coordinates 'x' 'y' 'z'
                    stats['y'] = math.floor(i/16/16)
                    i = i % (16*16)
                    stats['z'] = math.floor(i/16)
                    stats['x'] = i % 16

                    # look for the text associated with signs and store it with the block
                    if stats['block_type'].endswith('sign'):
                        # "{\"text\":\"\"} {\"text\":\"King Chris\\u0027s Office\"} {\"text\":\"\"} {\"text\":\"\"}"
                        for block_entity in tile_entities:
                            if block_entity['x'] == stats['x'] + x_0 and block_entity['y'] == stats['y'] + y_0 and block_entity['z'] == stats['z'] + z_0:
                                stats['text'] = (json.loads(block_entity['Text1'])['text'] + ' ' + json.loads(block_entity['Text2'])['text'] + ' ' + json.loads(block_entity['Text3'])['text'] + ' ' + json.loads(block_entity['Text4'])['text']).strip()
                                break

                    # collect blocks
                    if y_i_low <= stats['y'] <= y_i_high:
                        # all_blocks[(stats['x'] + x_0, stats['y'] + y_0, stats['z'] + z_0)] = stats
                        if x_low <= (stats['x'] + x_0) <= x_high and z_low <= (stats['z'] + z_0) <= z_high:
                            all_blocks[(stats['y'] + y_0, stats['x'] + x_0, stats['z'] + z_0)] = stats
                            # if num != 0:
                            #     print('  block_type = ' + stats['block_type'])

    return all_blocks


def generate_basemap_json(all_blocks, jsn_file=default_json_file):

    doors = {}
    levers = []
    data = []
    victims = []

    for key, value in sorted(all_blocks.items(), reverse=True):
        # print('key:' + str(key))
        # print('value:' + str(value))
        if value['block_type'] == 'air':
            continue

        if value['block_type'] == 'orange_glazed_terracotta':
            victims.append({
                "y": key[0],
                "z": key[2],
                "block_type": "block_victim_2",
                "x": key[1],
            })
            continue
        if value['block_type'].endswith('_glazed_terracotta'):
            victims.append({
                "y": key[0],
                "z": key[2],
                "block_type": "block_victim_1",
                "x": key[1],
            })
            continue

        loc = [key[1], key[0], key[2]]

        # Need to group all the door tops and bottoms together
        if value['block_type'].endswith('_door'):
            # door tops and bottoms will have the same x and z value so use that as the key
            door_key = str(key[1]) + ',' + str(key[2])
            door = []
            if door_key in doors.keys():
                door = doors[door_key]
            else:
                doors[door_key] = door
            value['loc'] = loc
            door.append(value)

        if value['block_type'] == 'lever' or value['block_type'].endswith('_button'):
            levers.append([loc, value['block_type'], value['data']])

        data_item = [loc, value['block_type'], value['data']]
        if 'text' in value.keys():
            data_item.append(value['text'])
        data.append(data_item)

    # Now prepare the door output and find any double doors
    doors_out = []
    for key, value in doors.items():
        if len(value) == 0:
            continue

        door_info = []
        bt = ''
        for db in value:
            bt = db['block_type']
            door_info.append(db['loc'])

        door_info.append(bt)
        for db in value:
            door_info.append(db['data'])
        doors_out.append(door_info)

    blocks_in_building = {"doors": doors_out, "levers": levers, "data": data}
    with open(jsn_file, 'w') as outfile:
        json.dump(blocks_in_building, outfile, indent=2)

    return victims


def make_world(world_name, ranges):
    # ---------------------------------------------------------
    # get the mapping from block id to block type
    block_dict = {}
    block_id_filename = 'block_id.json'
    with open(block_id_filename) as json_file:
        for entry in json.load(json_file):
            if entry['type'] not in block_dict:
                block_dict[entry['type']] = entry['text_type']

    # ---------------------------------------------------------
    # get the mapping from block id to block type
    world = mc.load(make_world_path(world_name))
    all_blocks = {}

    for region_key in world.regions.keys():
        process_region(region_key, world.regions[region_key], ranges, all_blocks, block_dict)

    # print(all_blocks)
    jsn_file = world_name + '.json'
    victims = generate_basemap_json(all_blocks, jsn_file)

    # print(json.dumps(victims, indent=2, separators=(',', ': ')))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Script to create minecraft world in json format')
    parser.add_argument('mc_world')
    args = parser.parse_args()
    world_name = args.mc_world
    print('Creating JSON file for world {}'.format(world_name))

    # rngs = (x_low, x_high, z_low, z_high, y_low, y_high)
    # All Saturn map Ranges
    ranges = (-2240,  -2068,   -82,    130,    60,     62)
    make_world(world_name, ranges)
