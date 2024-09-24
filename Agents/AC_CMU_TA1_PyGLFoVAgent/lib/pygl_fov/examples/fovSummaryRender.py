"""
semanticMapRenderer.py

A simple script for rendering and saving semantic maps of the FOV given a
sequence of player poses.
"""

import numpy as np
import time
import json
import pandas as pd

import pygl_fov
import pygl_fov.visualize
import pygl_fov.summaries

import os
import sys

trial_name = sys.argv[1]

trajectory_path = f'E:/dev/Data/Experiment_Huao/{trial_name}/test_frame.json'
output_path = f'E:/dev/Data/Experiment_Huao/fov/{trial_name}.csv'

print("Trajectory Path:", trajectory_path)
print("Output file folder:", output_path)

# Load the trajectory path and parse
# Here we use frame.json from human data collection pipe developed by TA1-CMU RI
# The trajectory is in json format
with open(trajectory_path) as trajectory_file:
	# data = trajectory_file.readlines()
	data = json.load(trajectory_file)

# Width and height are pre-set for 640 by 480
# WIDTH = int(data[0].strip().split('=')[1])
# HEIGHT = int(data[1].strip().split('=')[1])
WIDTH = 640
HEIGHT = 480

trajectory_data = data

poses = []

for item in trajectory_data.items():
	timestamp, pose_data = item
	# line = line.split(':')[1].strip()
	poses.append({
		'timestamp': timestamp,
		'pose':[
			float(pose_data['xPos']),
			float(pose_data['yPos']),
			float(pose_data['zPos']),
			float(pose_data['yaw']),
			float(pose_data['pitch']),
		]
	})


### WINDOW SIZE ###
WINDOW_SIZE = (WIDTH, HEIGHT)


# Create the block feeder
feeder = pygl_fov.BlockListFeeder.loadFromJson("data/map_blocks.json")

#Create the perspective
perspective = pygl_fov.Perspective(position=(0,0,0),
	                               orientation=(0,0,0),
	                               window_size=WINDOW_SIZE)


# Create the FOV
fov = pygl_fov.FOV(perspective, feeder)

# Create the semantic visualizer and corresponding plot window
pltWindow = pygl_fov.visualize.MatplotWindow()
semanticVis = pygl_fov.visualize.SemanticMapVisualizer(WINDOW_SIZE)
pltWindow.add(semanticVis, 111)

summary = pygl_fov.summaries.BlockListSummary(fov)

fov_list = []

for item in poses:
	t = item['timestamp']
	print(f'Time Step {t}')

	x, y, z, yaw, pitch = item['pose']
	print(f'  Position: ({x}, {y}, {z})')
	print(f'  Orientation: ({pitch}, {yaw}, 0)')

	# Set the player's orientation
	perspective.position = (x, y, z)
	perspective.orientation = (pitch, yaw, 0.0)

	# Create the pixel to block ID map
	pixelMap = fov.calculatePixelToBlockIdMap()

	# Create a semanticMap based on blockIDs in the pixel map
	semanticMap = np.zeros(pixelMap.shape)

	for blockID in np.unique(pixelMap):
		if blockID != -1:
			semanticMap[pixelMap == blockID] = feeder[blockID].block_type

	semanticVis.values = semanticMap
	semanticVis.update()
	# semanticVis.save(os.path.join(output_path,"frame_%d.png"%t))

	for block in summary():
		block_type = str(block.block_type)[6:]
		print(f'Timestamp: {t}\tBlock Location: {block.location}\tBlock Type: {str(block.block_type)[6:]}\tNum Pixels: {block.num_pixels}')
		if block_type == 'gold_block' or block_type == 'prismarie' or 'door' in block_type:
			fov_list.append({
				'timestamp': t,
				'block type': block_type,
				'num pixels': block.num_pixels,
				'block_loc X': block.location[0],
				'block_loc Y': block.location[1],
				'block_loc Z': block.location[2],
				'frame_loc x': x,
				'frame_loc y': y,
				'frame_loc z': z,
				'frame_loc yaw': yaw,
				'frame_loc pitch': pitch,
			})

df_fovList = pd.DataFrame(fov_list)
df_fovList.to_csv(output_path)
#	print()


