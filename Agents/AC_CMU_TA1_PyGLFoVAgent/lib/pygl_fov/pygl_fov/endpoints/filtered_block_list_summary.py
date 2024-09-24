import numpy as np
import copy

import MinecraftElements

#from .summary import Summary

class FilteredBlockListSummary:
	"""
	A FilteredBlockListSummary provides a list of the blocks in the player's
	FOV, as well as the number of pixels associated with each block.  The 
	summary will only include blocks of type in the filter, speeding the 
	calculations
	"""


	def __init__(self, block_feeder, blocks_to_summarize):
		"""
		Create a new FilteredBlockListSummary

		Args:
			block_feeder - instance of a feeder containing the blocks in the
			               world
			blocks_to_summarize - list or set of block types to include in the
			                      generated summaries
		"""

		self.block_feeder = block_feeder
		self.filter = set(blocks_to_summarize)



	def addBlockToSummary(self, block_type):
		"""
		Add a block type to summarize

		Args:
			block_type - type of block to summarize
		"""

		self.filter.add(block_type)


	def removeBlockFromSummary(self, block_type):
		"""
		Remove a block type from the summary, if it's in the summary

		Args:
			block_type - type of block to stop summarizing
		"""

		if block_type in self.filter:
			self.filter.remove(block_type)

	
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

				if self.block_feeder[blockID].block_type in self.filter:
					block = self.block_feeder[blockID]

					# Determine which pixels on the pixelMap correspond to the
					# presence of the block.  This will consist of a pair of
					# lists, one for each axes.
					blockIdx = np.where(pixelMap == blockID)

					num_pixels = len(blockIdx[0])
					bounding_box = [np.min(blockIdx[0]), np.max(blockIdx[0]),
		    	                    np.min(blockIdx[1]), np.max(blockIdx[1])]

					block_info = {"block": block, "pixel_count": num_pixels, "bounding_box": bounding_box}

					# If looking at a player, indicate which player it is
					if block.block_type == MinecraftElements.Block.player:
						block_info["playername"] = block.playername

					blocks.append(block_info)

		return blocks





