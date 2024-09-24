"""
testRenderTime.py

A simple script to test the time requirements for a rendering pipeline.  This
script tests multiple states of the pipeline, specifically:
    1.  Feeding blocks into the OpenGL rendering pipeline
    2.  Performing the OpenGL rendering
    3.  Reading the frame buffer to a numpy array
    4.  Summarizing block information
"""


import numpy as np
import time

import pygl_fov
import pygl_fov.endpoints
import pygl_fov.vertex_store

import MinecraftElements

import sys

if len(sys.argv) > 1:
	map_file = sys.argv[1]
else:
	map_file = "data/map_blocks.json"

print("Using Map File: %s" % map_file)


### PLAYER POSE AND WINDOW SIZE ###
### The position represents a value that would come out of the USAR experiment,
### as of testbed version 0.4.  The position listed here corresponds to the 
### intersections of the three main hallways. 
PLAYER_POSITION = (-2139.0, 52.0, 176.0)
PLAYER_ORIENTATION = (0.0, 0.0, 0.0)
WINDOW_SIZE = (640, 480)


## OVERVIEW:  This example loads the USAR voxel map (stored as a pickle file)
##            and generates a sequence of poses (orientation only).  After each
##            pose update, the semantic map of the player's FoV is generated 
##            and rendered to a Matplot window.
## STEPS:
##    1.  Create a VoxelMapBlockFeeder, which loads a pickle file containing
##        the voxel map of the USAR environment
##    2.  Create a Perspective, which represents the current player's pose
##    3.  Create a FOV instance with the above two components
##    4.  Create a SemanticMapVisualizer to get a semantic visualization of the
##        field of view
##    5.  Loop through a 360 degree spin of the player (incrementing yaw by 10
##        degrees); get the pixelToBlockID map from the FOV instance, and render
##        in the semantic visualizer.

# First create an instance of a BlockFeeder (which is used by FOV to query
# the environment for which blocks are present) and a Perspective (which is
# used by FOV to generate the block-ID-to-pixel map).

# VoxelMapBlockFeeder uses a previously generated VoxelMap (stored as a pickle
# file) to maintain which blocks are in the environment
#feeder = pygl_fov.VoxelMapBlockFeeder.loadFromPickle("data/USAR_VoxelMap.pkl")

# The Perspective class requires the initial position and orientation of the
# perspective, and the size of the window presented to the player.  All values
# can be updated during execution (e.g., as the player moves); the window size
# should match that of the Minecraft window, or at least have the same aspect
# ratio.
perspective = pygl_fov.Perspective(position=PLAYER_POSITION,
	                               orientation=PLAYER_ORIENTATION,
	                               window_size=WINDOW_SIZE)

# BlockListFeeder uses a list of blocks in the environment, which is simpler to
# use and allows for block modifiers (e.g., facing). 
feeder = pygl_fov.BlockFeeder.loadFromJson(map_file)

# A vertex store manages vertices corresponding to blocks in a feeder
vertex_store = pygl_fov.vertex_store.StaticVboStore(feeder)


# The FOV class controls interaction between the block feeder and perspective.
# As we want to test timing of specific aspects of the FoV pipeline, we want
# to control the steps of calculating the pixel to block ID map, don't register
# the FoV with the subcomponents
fov = pygl_fov.FOV(perspective, vertex_store, False)

# The summary we want to use
block_filter = set([ MinecraftElements.Block.torch,
		MinecraftElements.Block.standing_sign,
		MinecraftElements.Block.wooden_door,
		MinecraftElements.Block.wall_sign,
		MinecraftElements.Block.lever,
		MinecraftElements.Block.iron_door,
		MinecraftElements.Block.unlit_redstone_torch,
		MinecraftElements.Block.redstone_torch,
		MinecraftElements.Block.stone_button,
		MinecraftElements.Block.wooden_button,
		MinecraftElements.Block.spruce_door,
		MinecraftElements.Block.birch_door,
		MinecraftElements.Block.jungle_door,
		MinecraftElements.Block.acacia_door,
		MinecraftElements.Block.dark_oak_door,
		MinecraftElements.Block.block_victim_1,
		MinecraftElements.Block.block_victim_2,
		MinecraftElements.Block.block_victim_saved
	])

summary = pygl_fov.endpoints.FilteredBlockListSummary(feeder, block_filter)


# List of times taken to compute each step of the process, which currently 
# consist of the following:
#   1.  render - push blocks to the OpenGL rendering pipeline
#   2.  readFromOpenGL - read the resulting image buffer (as numpy array)
#   3.  convert - convert colors back to block IDs
#   4.  summarize - create a summary of blocks in the FoV
times = { 'prepareVBO':     [],
          'render':         [],
          'readFromOpenGL': [],
          'convert':        [],
          'summarize':      [],
          'total':          []
        }

NUM_POSES = 100
X_RANGE = [-2220.0, -2090.0]
Z_RANGE = [-10.0, 120.0]
YAW_RANGE = [0.0, 360.0]
PITCH_RANGE = [-90.0, 90.0]

for step in range(NUM_POSES):
	print(f'Step Number {step+1} / {NUM_POSES}')

	position = (np.random.random()*(X_RANGE[1]-X_RANGE[0]) + X_RANGE[0],
				60.0,
		        np.random.random()*(Z_RANGE[1]-Z_RANGE[0]) + Z_RANGE[0])
	orientation = (np.random.random()*(PITCH_RANGE[1]-PITCH_RANGE[0]) + PITCH_RANGE[0],
		           np.random.random()*(YAW_RANGE[1]-YAW_RANGE[0]) + YAW_RANGE[0],
		           0.0)
	
	perspective.set_pose(position, orientation)	

	# Create VBOs
#	start_time = time.time()
#	fov.prepareVBO()
#	end_time = time.time()

#	times['prepareVBO'].append(end_time - start_time)

	# Feed blocks into the OpenGL pipeline
	start_time = time.time()
	fov.render()
	end_time = time.time()

	times['render'].append(end_time-start_time)

	# Read the image from OpenGL pipeline
	start_time = time.time()
	blockIdImage = perspective.getImage()
	end_time = time.time()

	times['readFromOpenGL'].append(end_time-start_time)

	# Convert color to BlockID
	start_time = time.time()
	pixelToBlockIdMap = fov.color_map.id((blockIdImage[:,:,0],
		                                  blockIdImage[:,:,1],
		                                  blockIdImage[:,:,2]))
	end_time = time.time()
	print(len(np.unique(pixelToBlockIdMap)))

	times['convert'].append(end_time-start_time)

	# Summarize
	start_time = time.time()
	block_list = summary(pixelToBlockIdMap)
	end_time = time.time()

	print(f'  Number of Blocks: {len(block_list)}')



#	pixelmap = fov.calculatePixelToBlockIdMap()


	times['summarize'].append(end_time-start_time)	

	times['total'].append(times['render'][-1] + times['readFromOpenGL'][-1] + times['convert'][-1] + times['summarize'][-1])


# Calculate statistics
#meanPrepareTime = np.mean(times['prepareVBO'])
#stdPrepareTime = np.std(times['prepareVBO'])

meanRenderTime = np.mean(times['render'])
stdRenderTime = np.std(times['render'])

meanReadTime = np.mean(times['readFromOpenGL'])
stdReadTime = np.std(times['readFromOpenGL'])

meanConvertTime = np.mean(times['convert'])
stdConvertTime = np.std(times['convert'])

meanSummaryTime = np.mean(times['summarize'])
stdSummaryTime = np.std(times['summarize'])

meanTotalTime = np.mean(times['total'])
stdTotalTime = np.std(times['total'])



# Print the results
print(f'Results over {NUM_POSES} poses (values in seconds):')
#print(f'   Average time to Prepare:    {meanPrepareTime} (Std Dev: {stdPrepareTime})')
print(f'   Average time to Render:     {meanRenderTime} (Std Dev: {stdRenderTime})')
print(f'   Average time to Read Image: {meanReadTime} (Std Dev: {stdReadTime})')
print(f'   Average time to Convert:    {meanConvertTime} (Std Dev: {stdConvertTime})')
print(f'   Average time to Summarize:  {meanSummaryTime} (Std Dev: {stdSummaryTime})')
print(f'   Average total time:         {meanTotalTime} (Std Dev: {stdTotalTime})')
