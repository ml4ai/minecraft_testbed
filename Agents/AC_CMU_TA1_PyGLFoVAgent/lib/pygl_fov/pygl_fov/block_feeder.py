"""
block_feeder.py

This file defines classes for storing and feeding blocks to 

the FoV membership calculator, as well as default implementations.

At a minimum, a block feeder needs to implement the functions necessary for 
iteration over 


Author: Dana Hughes
email: danahugh@andrew.cmu.edu
"""


from .block import Block
from .block import BlockIdRegistry

import json

import MinecraftElements

import logging


class BlockFeeder():
	"""
	A BlockFeeder is a simple data structure for maintaining a list of blocks
	and corresponding identities.
	"""

	@classmethod
	def loadFromJson(cls, json_path):
		"""
		Create a BlockFeeder consisting of the contents of the provided JSON
		file.

		json_path - path to the json file containing the map
		"""

		blockFeeder = cls()

		# Load the json data and get the 1D list of blocks
		with open(json_path) as json_file:
		    json_data = json.loads(json_file.read())


		# Simply assign block ID based on the order they're read in
		for block in json_data['blocks']:

			# Location and type are required information
			location = (block['location']['x'],
				        block['location']['y'],
				        block['location']['z'])
			block_type = MinecraftElements.Block[block['type']]

			# Optional - facing, powered, attached, half, shape
			facing = block.get('facing', None)
			facing = MinecraftElements.Facing[facing] if facing is not None else None
			powered = block.get('powered', False)
			attached = block.get('attached', False)
			half = block.get('half', None)
			half = MinecraftElements.Half[half] if half is not None else None
			shape = block.get('shape', None)
			shape = MinecraftElements.Shape[shape] if shape is not None else None
			east = block.get('east', False)
			west = block.get('west', False)
			north = block.get('north', False)
			south = block.get('south', False)
			in_wall = block.get('in_wall', False)
			hinge = block.get('hinge', None)
			hinge = MinecraftElements.Hinge[hinge] if hinge is not None else None
			isopen = block.get('open', None)

			# Add the block to the feeder
			blockFeeder.add(Block(location, block_type, 
				                  facing=facing, powered=powered,
				                  attached=attached, half=half, shape=shape,
				                  east=east, west=west, north=north, south=south,
				                  hinge=hinge, in_wall=in_wall, isopen=isopen))

		# Add metadata to the blockFeeder, if it exists in the json
		if "metadata" in json_data.keys():
			blockFeeder.setMetadata(json_data["metadata"])

		return blockFeeder



	def __init__(self, name=None, metadata=None):
		"""
		Create a new block feeder.
		"""

		# Name of the blockfeeder, in case multiple instances exist
		self.name = name

		# Logging -- create a name for the feeder to use, and grab the instance
		# of the logger
		self.logger = logging.getLogger(__name__)
		if self.name is None:
			self.__string_name = '[BlockFeeder]'
		else:
			self.__string_name = '[BlockFeeder - %s]' % self.name

		# Block instances will be jointly stored by location and id, in order
		# to simplify accessing blocks by these
		self.block_map_by_location = {}
		self.block_map_by_id = {}

		# The feeder will allow listeners to register (and deregister)
		# themselves, to be informed when the contents of the feeder have 
		# been changed.
		self.__observers = set()
		self.stale = False

		# A simple store for a dictionary containing metadata of the world
		self.metadata = metadata


	def setMetadata(self, metadata):
		"""
		Set the metadata of the block feeder
		"""

		self.metadata = metadata


	def register(self, observer):
		"""
		Add an observer to the feeder
		"""

		if observer in self.__observers:
			self.logger.warning("%s:  Attemting to add already registered observer: %s", self, observer)

		self.__observers.add(observer)


	def deregister(self, observer):
		"""
		Remove a observer to the feeder
		"""

		if not observer in self.__observers:
			self.logger.warning("%s:  Attemting to remove non-registered observer: %s", self, observer)

		self.__observers.remove(observer)


	def __notify(self):
		"""
		Inform observers that the Block Feed has changed.
		"""

		for observer in self.__observers:
			observer.onBlockFeederUpdate(self)


	def __str__(self):
		"""
		String representation of the BlockFeeder
		"""

		return self.__string_name


	def add(self, block):
		"""
		Add a block to the list
		"""

		# Check if a block with the given id and location exist
		if block.id in self.block_map_by_id.keys():
			self.logger.warning("%s:  Adding a block with existing ID: %d.  Block will be overwritten", self, block.id)
			self.logger.warning("%s:    Original Block: %s", self, self[block.id])
			self.logger.warning("%s:    New Block:      %s", self, block)
		if block.location in self.block_map_by_location.keys():
			self.logger.warning("%s:  Adding a block with existing location: %s.  Block will be overwritten", self, str(block.location))
			self.logger.warning("%s:    Original Block: %s", self, self.getBlockAt(block.location))
			self.logger.warning("%s:    New Block:      %s", self, block)

		# Add the block
		self.block_map_by_id[block.id] = block
		self.block_map_by_location[block.location] = block

		self.logger.debug("%s:  Added block with ID: %d; location: %s", self, block.id, str(block.location))

		self.stale = True

		# Notify each observer that the block was added to this feeder
		for observer in self.__observers:
			observer.onBlockAddedToFeeder(self, block)


	def __contains__(self, block_id):
		"""
		Check if the block id is in the feeder

		Args:
			id - ID of the block to be located
		"""

		return block_id in self.block_map_by_id.keys()


	def __iter__(self):
		"""
		Simply return an iterator over the stored list of blocks (using the ID map)
		"""

		return iter(self.block_map_by_id.values())


	def __len__(self):
		return len(self.block_map_by_id)


	def __getitem__(self, block_id):
		"""
		Return the block with the given ID.  Returns None if an invalid ID is
		provided.

		Args:
		    block_id - integer ID of the desired block.
		"""

		# Alert the logger if the block_id provided isn't valid
		if not block_id in self.block_map_by_id.keys():
			self.logger.warning("%s:  Block ID not in feeder: %d", self, block_id)
			return None

		return self.block_map_by_id[block_id]


	def containsBlockAt(self, location):
		"""
		Check if the feeder has a block at the provided location
		"""

		return location in self.block_map_by_location.keys()


	def getBlockByLocation(self, location):
		"""
		Deprecated version of getBlockAt
		"""

		self.logger.warning("%s:  getBlockByLocation is deprecated.  Replace with getBlockAt", self)
		return self.getBlockAt(location)


	def getBlockAt(self, location):
		"""
		Return the block at the given location.  Returns None if no known block
		is at the location.

		Args:
			location - location (x,y,z) of the block.
		"""

		# Alert the logger if the block_id provided isn't valid
		if not location in self.block_map_by_location.keys():
			self.logger.warning("%s:  Block not in feeder with location: %s", self, str(location))
			return None

		return self.block_map_by_location[location]


	def removeBlockAtLocation(self, location):
		"""
		Deprecated version of getBlockAt
		"""

		self.logger.warning("%s:  removeBlockByAtcation is deprecated.  Replace with removeBlockAt", self)
		return self.removeBlockAt(location)


	def removeBlockAt(self, location):
		"""
		Remove the block at the given location.

		Args:
		    location - location (x,y,z) of the block to remove
		"""

		# Check if the block is in the map, and alert if not
		if not location in self.block_map_by_location.keys():
			self.logger.warning("%s:  Attemping to remove block by location not in feeder: %s", self, str(location))
			return None	

		# Pop the block out of the location-based map, and delete the entry
		# in the id-based map
		removed_block = self.block_map_by_location.pop(location)

		# Check if the removed block exists in the ID map
		if removed_block.id in self.block_map_by_id.keys():
			del(self.block_map_by_id[removed_block.id])
		else:
			self.logger.warning("%s:  Attempting to remove block with invalid ID from feeder: %d", self, removed_block.id)

		self.stale = True


	def removeBlock(self, block_id):
		"""
		Remove the block with a given id.

		Args:
		    block_id - integer ID of the block to remove
		"""

		# Check if the block is in the map, and alert if not
		if not block_id in self.block_map_by_id.keys():
			self.logger.warning("%s:  Attemping to remove block with invalid ID from feeder: %d", self, block_id)
			return None	

		# Pop the block out of the id-based map, and delete the entry
		# in the id-based map
		removed_block = self.block_map_by_id.pop(block_id)

		# Check if the removed block exists in the ID map
		if removed_block.location in self.block_map_by_location.keys():
			del(self.block_map_by_location[removed_block.location])
		else:
			self.logger.warning("%s:  Attempting to remove block by location not in feeder: %s", self, str(removed_block.location))

		self.stale = True


	def finalize(self):
		"""
		Recompute the id of each block in the list
		"""

		self.logger.warning("%s:  finalize is deprecated and does nothing", self)

		pass

