"""
semanticMapRenderer.py

A simple script for rendering and saving semantic maps of the FOV given a
sequence of player poses.
"""

import numpy as np
import time

import pygl_fov
from pygl_fov.vertex_store import StaticVboStore
import pygl_fov.endpoints

import os
import sys

trajectory_path = sys.argv[1]
output_path = sys.argv[2]

print("Trajectory Path:", trajectory_path)
print("Output file folder:", output_path)

# Load the trajectory path and parse
with open(trajectory_path) as trajectory_file:
	data = trajectory_file.readlines()

# Width and height are the first two lines
WIDTH = int(data[0].strip().split('=')[1])
HEIGHT = int(data[1].strip().split('=')[1])

trajectory_data = data[2:]

poses = []

for line in trajectory_data:
	line = line.split(':')[1].strip()
	poses.append([float(x) for x in line.split()])


### WINDOW SIZE ###
WINDOW_SIZE = (WIDTH, HEIGHT)


# Create the block feeder
feeder = pygl_fov.BlockListFeeder.loadFromJson("data/map_blocks.json")
vertex_store = StaticVboStore(feeder)

#Create the perspective
perspective = pygl_fov.Perspective(position=(0,0,0),
	                               orientation=(0,0,0),
	                               window_size=WINDOW_SIZE)


# Create the FOV
fov = pygl_fov.FOV(perspective, vertex_store)

# Create the semantic visualizer and corresponding plot window
pltWindow = pygl_fov.endpoints.MatplotWindow()
semanticVis = pygl_fov.endpoints.SemanticMapVisualizer(WINDOW_SIZE)
pltWindow.add(semanticVis, 111)


for t in range(len(poses)):
	print(f'Time Step {t}')

	x, y, z, yaw, pitch = poses[t]
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
	semanticVis.save(os.path.join(output_path,"frame_%d.png"%t))


#	for block in summary():
#		print(f'Block Location: {block.location}\tBlock Type: {block.block_type}\tNum Pixels: {block.num_pixels}')

#	print()


