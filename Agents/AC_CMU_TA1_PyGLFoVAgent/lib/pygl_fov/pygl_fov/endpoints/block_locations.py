"""
"""

import numpy as np

class BlockLocations:
	"""
	An endpoint that provides a list of block locations in the field of view
	"""

	def __init__(self, block_feeder):
		"""
		Create a BlockLocations endpoint

		Args:
			block_feeder - feeder of blocks in the environment
		"""

		self.block_feeder = block_feeder


	def __call__(self, pixelMap):
		"""
		Get the list of the location of blocks in the FOV.

		Args
			pixelMap - calculated pixelMap from FoV

		Returns
			A list of Block locations (x,y,z).
		"""

		# Get the unique IDs contained in the pixelMap
		blockIDs = np.unique(pixelMap)

		# Create a list of blocks, and copy over all blocks in the scene, and
		# add the pixel statistics
		locations = [self.block_feeder[_id].location for _id in blockIDs if _id in self.block_feeder]

		return locations