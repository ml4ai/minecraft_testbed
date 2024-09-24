"""
semantic_map.py

A simple example showing how to get a semantic visualization of the player's
field of view.

In this example, an FOV pipeline is created with a block summary and 
visualization sinks.  The player is placed in the center of the hallway 
intersection, and rotated 360 degrees at 10 degree intervals.  At each 
interval, the visualizer renders a semantic map of the scene, and the summary
provides a list of which blocks are present (location, type, and number of pixels).
"""


import numpy as np
import time

import pygl_fov
import pygl_fov.visualize
import pygl_fov.summaries

#import pygame

### PLAYER POSE AND WINDOW SIZE ###
### The position represents a value that would come out of the USAR experiment,
### as of testbed version 0.4.  The position listed here corresponds to the 
### intersections of the three main hallways. 
PLAYER_POSITION = (-2139.0, 52.0, 176.0)
PLAYER_ORIENTATION = (0.0, 0.0, 0.0)
WINDOW_SIZE = (852, 480)


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

# BlockListFeeder uses a list of blocks in the environment, which is simpler to
# use and allows for block modifiers (e.g., facing)
feeder = pygl_fov.BlockListFeeder.loadFromJson("data/map_blocks.json")

# The Perspective class requires the initial position and orientation of the
# perspective, and the size of the window presented to the player.  All values
# can be updated during execution (e.g., as the player moves); the window size
# should match that of the Minecraft window, or at least have the same aspect
# ratio.
perspective = pygl_fov.Perspective(position=PLAYER_POSITION,
	                               orientation=PLAYER_ORIENTATION,
	                               window_size=WINDOW_SIZE)


# The FOV class controls interaction between the block feeder and perspective.
fov = pygl_fov.FOV(perspective, feeder)

fov.prepareVBO()


# The SemanticMapVisualizer is a visualizer that can be rendered in a Matplot
# window, and is relatively simple to construct.  Note that this approach
# allows more than one visualization to be created and rendered in the window;
# this example simply shows the case where a single visualization is shown.
pltWindow = pygl_fov.visualize.MatplotWindow()
semanticVis = pygl_fov.visualize.SemanticMapVisualizer(WINDOW_SIZE)
pltWindow.add(semanticVis, 111)

"""
# PygameVisualizer is a very simple visualizer to generate a semantic map
# of the scene
pygameVis = pygl_fov.visualize.PygameVisualizer(WINDOW_SIZE)
"""

summary = pygl_fov.summaries.BlockListSummary(fov)

# Loop through 360 degrees, i.e., have the player rotate areound in at the
# intersection of the hallways.
for angle in range(0,360,10):
	# Set the player's orientation
	perspective.orientation=(0.0, angle, 0.0)

	# Create the pixel to block ID map
	pixelMap = fov.calculatePixelToBlockIdMap()

	# Create a semanticMap based on blockIDs in the pixel map
	semanticMap = np.zeros(pixelMap.shape)

	for blockID in np.unique(pixelMap):
		if blockID != -1:
			semanticMap[pixelMap == blockID] = feeder[blockID].block_type

	# This isn't the best way to update the visualization, but it'll have to do
	# until I wrap my head around this part
	semanticVis.values = semanticMap
	semanticVis.update()

	"""
	pygameVis.draw(semanticMap)


#	pygame.display.flip()
	"""

	for block in summary():
		print(f'Block Location: {block.location}\tBlock Type: {block.block_type}\tNum Pixels: {block.num_pixels}')


