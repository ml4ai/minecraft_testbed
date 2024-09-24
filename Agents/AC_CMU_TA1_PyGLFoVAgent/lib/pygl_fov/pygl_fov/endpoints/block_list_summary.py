"""
"""

import numpy as np
import copy

import MinecraftElements


class BlockListSummary:
	"""
	A BlockListSummary provides a list of the blocks in the player's FOV, as
	well as the number of pixels associated with each block
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
			A list of Block objects with the number of pixels associated with
			the block in the FOV.
		"""

		# Get the unique IDs contained in the pixelMap
		blockIDs = np.unique(pixelMap)

		# Create a list of blocks, and copy over all blocks in the scene, and
		# add the pixel statistics
		blocks = []

		for blockID in blockIDs:
			if blockID in self.block_feeder:
				block = self.block_feeder[blockID]
				blockIdx = np.where(pixelMap == blockID)

				num_pixels = np.sum(blockIdx)
				bounding_box = [np.min(blockIdx[0]), np.max(blockIdx[0]),
				                      np.min(blockIdx[1]), np.max(blockIdx[1])]

				blocks.append({"block": block, "pixel_count": num_pixels, "bounding_box": bounding_box})

		return blocks





