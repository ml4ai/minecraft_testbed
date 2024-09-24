"""
composite_block_feeder.py

This file defines a class for aggregating atomic block feeders.

Author: Dana Hughes
email: danahugh@andrew.cmu.edu
"""


#from .block import Block
#from .block import BlockIdRegistry

#import json

#import MinecraftElements

import logging


class CompositeBlockFeeder():
	"""
	A CompositeBlockFeeder contains several base BlockFeeders.  The Composite
	maintains the same interface as the base BlockFeeder class, so that it may
	be used interchangably with base BlockFeeders.
	"""

	def __init__(self, name=None):
		"""
		Create a CompositeBlockFeeder
		"""
		# Name of the blockfeeder, in case multiple instances exist
		self.name = name

		# Logging -- create a name for the feeder to use, and grab the instance
		# of the logger
		self.logger = logging.getLogger(__name__)
		if self.name is None:
			self.__string_name = '[CompositeBlockFeeder]'
		else:
			self.__string_name = '[CompositeBlockFeeder - %s]' % self.name

		# Store atomic feeders in a list
		self.feeders = []

		# The feeder will allow listeners to register (and deregister)
		# themselves, to be informed when the contents of the feeder have 
		# been changed.
		self.__observers = set()
		self.stale = False

		# Attributes needed for iteration over lists and blocks.  Iteration
		# will be nested:  Iteration is performed over feeders; within each
		# feeder, iteration is performed over blocks
		self.__current_feeder = None
		self.__feeder_iterator = None
		self.__block_iterator = None


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
		The composite feeder should not add any blocks to itself.  Rather,
		blocks need to be added to specific feeders directly.

		Args:
			block - instance of a Block to add to the feeder
		"""

		self.logger.warning("%s:  Attempting to add a block to a composite feeder.  Ignoring.", self)


	def addFeeder(self, feeder):
		"""
		Add the provided feeder to the list of feeders maintained by this 
		composite.

		Args:
			feeder - feeder to add to this composite
		"""

		# Is this feeder already here?
		if feeder in self.feeders:
			self.logger.warning("%s:  Attemting to add block feeder already contained in composite: %s.  Ignoring", self, feeder)
			return

		self.feeders.append(feeder)
		feeder.register(self)

		# Indicate to listeners that this feeder has been modified, and all 
		# blocks in the feeder have been added to this feeder
		for observer in self.__observers:
			observer.onBlockFeederUpdate(self)
			for block in feeder:
				observer.onBlockAddedToFeeder(self, block)


	def __contains__(self, block_id):
		"""
		Check if the block id is in the feeder

		Args:
			id - ID of the block to be located
		"""

		# Check if the block is in any of the contained feeders
		for feeder in self.feeders:
			if block_id in feeder:
				return True

		return False



	def __iter__(self):
		"""
		Start an iterator over all the blocks in all the feeders
		"""

		# Start an iterator over the feeders.  Make sure that the current
		# feeder and block iterator are set to None, so that __next__ can
		# handle the initial cases
		self.__feeder_iterator = iter(self.feeders)
		self.__current_feeder = None
		self.__block_iterator = None

		return self



	def __next__(self):
		"""
		Get the next block in the feeder
		"""

		# Check if there's a current feeder, and grab the next one if not
		if self.__current_feeder == None:
			try:
				self.__current_feeder = next(self.__feeder_iterator)
				self.__block_iterator = iter(self.__current_feeder)
			except StopIteration:
				# If there are no more feeders, then we're all done!
				raise StopIteration

		# Try to get a block from the current __block_iterator
		try:
			block = next(self.__block_iterator)
			return block

		except StopIteration:
			# We've reached the end of the iterator over the current feeder.
			# Set the current feeder and block iterator to None, and recurse
			self.__current_feeder = None
			self.__block_iterator = None
			return next(self)


	def __len__(self):
		"""
		Returns the total number of blocks in all feeders
		"""

		return sum([len(feeder) for feeder in self.feeders])


	def __getitem__(self, block_id):
		"""
		Return the block with the given ID.  Returns None if an invalid ID is
		provided.

		Args:
		    block_id - integer ID of the desired block.
		"""

		# Check if the block is in any of the feeders, and return if so
		for feeder in self.feeders:
			if block_id in feeder:
				return feeder[block_id]

		# The block wasn't found
		self.logger.warning("%s:  Block ID not in feeder: %d", self, block_id)
		return None


	def getFeederOf(self, block):
		"""
		Return the instance of the feeder that contains the block
		"""

		# Get the base feeder that this is in.  Note the natural recursion if
		# there is a hierarchy of composite feeders.
		for feeder in self.feeders:
			if block.id in feeder:
				return feeder


	def containsBlockAt(self, location):
		"""
		Check if the feeder has a block at the provided location
		"""

		# Try to find the block in each of the feeders
		for feeder in self.feeders:
			if feeder.containsBlockAt(location):
				return True

		# Block wasn't found in any of the feeders
		return False



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

		# Check if the block is in any of the feeders, and return if so
		for feeder in self.feeders:
			if feeder.containsBlockAt(location):
				return feeder.getBlockAt(location)

		# No block found
		self.logger.warning("%s:  Block not in feeder with location: %s", self, str(location))
		return None


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

		# Want to raise a warning if _no_ blocks were found
		block_found = False

		# Check if the block is in any of the feeders, and remove is so
		for feeder in self.feeders:
			if feeder.containsBlockAt(location):
				feeder.removeBlockAt(location)
				block_found = True

		# Raise a warning if no block was found
		if not block_found:
			self.logger.warning("%s:  Attemping to remove block by location not in feeder: %s", self, str(location))
			return None	


	def removeBlock(self, block_id):
		"""
		Remove the block with a given id.

		Args:
		    block_id - integer ID of the block to remove
		"""

		# Want to raise a warning if _no_ blocks were found
		block_found = False

		# Check if the block is in any feeder, and remove if so
		for feeder in self.feeders:
			if block_id in feeder:
				feeder.removeBlock(block_id)
				block_found = True

		# Raise a warning if no block was found
		if not block_found:
			self.logger.warning("%s:  Attemping to remove block with invalid ID from feeder: %d", self, block_id)
			return None			


#	def hide(self, block):
#		"""
#		Hide the block by setting its y value to a negative number.  The block
#		and its original location will be stored, so that it can later be
#		unhidden
#
#		Args:
#			block - instance of Block to hide
#		"""
#
#		self.logger.info("%s:  Hiding block: %s", self, block)
#
#		# Does the feeder actually contain this block?
#		if not block.id in self:
#			self.logger.warning("%s:  Attempting to hide block not in feeder: %s.  Ignoring.", self, block)
#			return
#
#		# Check which feeder the block is in, and hide
#		for feeder in self.feeders:
#			if block.id in feeder:
#				feeder.hide(block)
	

#	def unhide(self, block):
#		"""
#		Restore a hidden block to its original position.
#
#		Args:
#			block - instance of Block to unhide
#		"""
#
#		self.logger.info("%s:  Unhiding block: %s", self, block)
#
#		# Does the feeder actually contain this block?
#		if not self.hasHiddenBlock(block): #block.id in self:
#			self.logger.warning("%s:  Attempting to unhide block not in feeder: %s.  Ignoring.", self, block)
#			return
#
#		# Find which feeder the block is in, and unhide
#		for feeder in self.feeders:
#			if feeder.hasHiddenBlock(block): #block.id in feeder:
#				feeder.unhide(block)


#	def hasHiddenBlock(self, block):
#		"""
#		Check if the provided block is in this feeder
#		"""
#
#		# Check if the block is hidden in any of the feeders
#		for feeder in self.feeders:
#			if feeder.hasHiddenBlock(block):
#				return True
#
#		# Block wasn't found as hidden
#		return False


	def finalize(self):
		"""
		Recompute the id of each block in the list
		"""

		self.logger.warning("%s:  finalize is deprecated and does nothing", self)

		pass


	# Callbacks from client block feeders:  any time a feeder sends a callback,
	# propagate that callback to my own obwervers
	def onBlockAddedToFeeder(self, feeder, block):
		"""
		Callback from the block feeder instances indicated when a block has been
		added to the feeder

		Args:
			feeder - instance of the block feeder
			block  - block added to the feeder
		"""

		for observer in self.__observers:
			observer.onBlockAddedToFeeder(feeder, block)			
			observer.onBlockAddedToFeeder(self, block)


	def onBlockFeederUpdate(self, feeder):
		"""
		Callback from block feeder instances indicating when the feeder has 
		been updated

		Args:
			feeder - instance of the updated block feeder		
		"""

		for observer in self.__observers:
			observer.onBlockFeederUpdate(feeder)
			observer.onBlockFeederUpdate(self)


	def onBlockModified(self, block):
		"""
		Callback from a block indicating that some property of the block has 
		changed.

		Args:
			block - instance of the updated block
		"""

		for observer in self.__observers:
			observer.onBlockModified(block)