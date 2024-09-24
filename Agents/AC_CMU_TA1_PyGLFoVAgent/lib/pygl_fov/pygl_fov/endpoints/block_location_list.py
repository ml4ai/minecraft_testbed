"""
"""

import numpy as np
import copy

import MinecraftElements


class BlockLocationList:
	"""
	A BlockLocationList provides a list of the locations of blocks in the
	player's FOV
	"""


	def __init__(self, block_feeder):
		"""
		Create a new BlockListSummary

		Args:
			block_feeder - instance of a feeder containing the blocks in the
			               world
		"""

		self.block_feeder = block_feeder

	
	def __call__(self, pixelMap):
		"""
		Get the list of blocks in the FOV, copy the blocks, and decorate
		with the number of pixels.

		Args
			pixelMap - calculated pixelMap from FoV

		Returns
			A list of (x,y,z) tuples of all blocks in the player's FoV
		"""

		# Get the unique IDs contained in the pixelMap
		blockIDs = np.unique(pixelMap)

		# Create a list of block locations
		locations = []

		for blockID in blockIDs:
			if blockID in self.block_feeder and self.block_feeder[blockID].block_type != MinecraftElements.Block.player:
				locations.append(self.block_feeder[blockID].location)

		return locations





