"""
voxel_map.py

A class for storing, querying, and manipulating a voxel map.
"""

# ORIGIN: -2168 152 51

import sys

# Need to add the location of MinecraftBridge to the path
PATH_TO_MINECRAFT_BRIDGE = "C:\\Research\\ASIST\\minecraft_bridge"
sys.path.append(PATH_TO_MINECRAFT_BRIDGE)


import numpy as np
import json

from MinecraftBridge.MinecraftElements import Block

class VoxelMap:
	"""
	A voxel map stores a 3D representation of blocks in a fixed boundary of the
	environment.

	Instances represent the voxel map as a 3D numpy array of integers, with
	entries representing of blocks enumarated by the Blocks enum.

	Orientation of axes of the VoxelMap correspond to those used in Minecraft:
	x-axis corresponds to WEST-EAST direction, y-axis corresponds to UP-DOWN
	direction, and z-axis corresponds to SOUTH-NORTH direction.
	"""

	def __init__(self, shape, corner):
		"""
		Create a new VoxelMap with the given shape and location.

		shape -  a 3-tuple defining the size of the voxel map, indexed by:
		         axis 0: WEST-EAST length (x-axis in Minecraft)
		         axis 1: UP-DOWN length (y-axis in Minecraft)
		         axis 2: SORTH-NOUTH length (z-axis in Minecraft)		         
		corner - the location of the (WEST,SOUTH,DOWN) corner (min values of
		         x-,y-,z- coordinates).
		"""

		# What are the dimensions and location of the voxel map?
		self.shape = shape
		self.corner = corner

		self.block_map = np.array(self.shape, dtype=np.uint8)


	def __getitem__(self, index):
		"""
		Allows for indexing into the voxel map using slices, similar to 
		indexing with numpy arrays.
		"""

		# NOTE:  Is this really how we should do it?  It'd be best if the
		#        indexing matched actual block locations...

		return self.block_map[index]


	@classmethod
	def loadFromJson(cls, json_path, shape, corner, map_key='grid'):
		"""
		Create a VoxelMap from a json file.

		json_path - path to the json file containing the map
		shape     - the shape of the defined map
		corner    - the corner location of the map
		key       - the JSON key containing a list of string values of
		            each block as a 1D array
		"""

		# Load the json data and get the 1D list of blocks
		with open(json_path) as json_file:
		    json_data = json.loads(json_file.read())

		block_strings = json_data[map_key]

		# Convert each block to the corresponding enumeration.  Reshape to 
		# match the shape provided
		blocks = np.array([Block[b] for b in block_strings], dtype=np.uint8)
		blocks = np.reshape(blocks, (shape[1], shape[2], shape[0]))
		blocks = np.swapaxes(blocks, 0, 1)
		blocks = np.swapaxes(blocks, 0, 2)
#		blocks = np.swapaxes(blocks, 1, 2)

		# Now create the VoxelMap instance
		voxelMap = cls(shape, corner)
		voxelMap.block_map = blocks

		return voxelMap

