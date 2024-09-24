"""
Definition of a composite vertex store class to maintain multiple instances of
vertex stores.
"""

from .vertices import *
from .id_color_mapper import BlockColorMapper

import logging

import ctypes

from OpenGL import GL


class CompositeVertexStore:
	"""
	A CompositeVertexStore maintains a collection of vertex stores, providing a
	common interface as the base vertex stores.
	"""

	def __init__(self, store_list=[], name=None):
		"""
		Create a CompositeVertexStore

		"""

		# Name of the vertex store, in case multiple instances exist
		self.name = name

		# Create a name for the CompositeVertexStore to use, and grab the 
		# instance of the logger.
		self.logger = logging.getLogger(__name__)
		if self.name is None:
			self.__string_name = '[CompositeVertexStore]'
		else:
			self.__string_name = '[CompositeVertexStore - %s]' % self.name

		# Copy over the vertex store list
		self.vertex_stores = [store for store in store_list]


	def __str__(self):
		"""
		String representation of the object
		"""

		return self.__string_name


	def __del__(self):
		"""
		Clean up any OpenGL related things
		"""

		self.logger.debug("%s: Deleting.", self)


	def add(self, block):
		"""
		Add the provided block to the list of blocks to render
		"""

		# Unallowed action, raise a warning and ignore
		self.logger.warning("%s:  Attempting to add a block to a CompositeVertexStore: %s.  Ignoring", self, block)


	def addStore(self, store):
		"""
		Add a vertex store to the composite
		"""

		self.vertex_stores.append(store)


	def onBlockModified(self, block, modifications=set()):
		"""
		Callback from a block when it is modified.  When a block is modified,
		recalculate the vertices and load into the VBO.

		Note that the number of vertices of the block should remain unchanged.
		If the vertex count changes, then log an error.

		Args:
			block - Block instance that was modified
		"""

		# Should not be called by any block
		self.logger.warning("%s:  onBlockModified called with block %s. Composite will not handle.", self, block)


	def prepare(self):
		"""
		Prepare the VBO
		"""

		self.logger.debug("%s: Preparing CompositeVertexStore for blocks", self)

		for store in self.vertex_stores:
			store.prepare()


	def render(self, ignore=[]):
		"""
		Render the scene

		Args:
			ignore - list or set of stores to not render
		"""

		# Assume that the perspective has already been set up
		self.logger.debug("%s:  Rendering CompositeVertexStore", self)

		for store in self.vertex_stores:
			if store not in ignore:
				store.render(ignore=ignore)
			else:
				self.logger.debug("%s:    Not rendering Vertex Store %s", self, store)
