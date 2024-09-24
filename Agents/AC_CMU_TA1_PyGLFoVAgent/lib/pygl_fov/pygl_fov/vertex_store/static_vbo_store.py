"""
A collection of classes used to store and maintain vertices to render.  A store
is responsible for converting blocks added to it to vertices in OpenGL, and
updating whenever changes are made to blocks under its purview.
"""

from ..vertices import *
from ..id_color_mapper import BlockColorMapper

import logging

import ctypes

from OpenGL import GL


class StaticVboStore:
	"""
	A StaticVboStore converts a provided set of blocks to a Vertex Buffer
	Object.  The blocks in this store are assumed to remain static, and should
	never need updating.
	"""

	def __init__(self, block_list=[], name=None, color_map=BlockColorMapper()):
		"""

		"""

		# Name of the vertex store, in case multiple instances exist
		self.name = name

		# Create a name for the StaticVboStore to use, and grab the instance of
		# the logger.
		self.logger = logging.getLogger(__name__)
		if self.name is None:
			self.__string_name = '[StaticVboStore]'
		else:
			self.__string_name = '[StaticVboStore - %s]' % self.name

		# Retain a copy of the blocks this store is responsible for
		self.blocks = {}
		for block in block_list:
			self.add(block)

		# Object to convert Blocks to color and back
		self.color_map = color_map

		# Vertex and Color buffers
		self.vertex_vbo = GL.glGenBuffers(1)
		self.color_vbo = GL.glGenBuffers(1)
		self.num_vertices = 0

		self.prepare()


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

		self.blocks[block] = {}

		# Register this store with the block to callback when the block is
		# modified
		block.register(self)


	def onBlockModified(self, block, modifications=set()):
		"""
		Callback from a block when it is modified.  When a block is modified,
		recalculate the vertices and load into the VBO.

		Note that the number of vertices of the block should remain unchanged.
		If the vertex count changes, then log an error.

		Args:
			block - Block instance that was modified
		"""

		self.logger.debug("%s: Block Modified: %s", self, block)

		# Recalculate the vertices for the block
		block_vertices = getVerticesLibrary[block.block_type](block)

		# Make sure that the number of new vertices is the same as the number
		# of vertices that are going to be replaced!
		if len(block_vertices) != self.blocks[block]['vertex_size']:
			self.logger.error("%s: Number of vertices of modified block (%d) does not match number of new vertices (%d)", self, len(self.blocks[block]['vertex_size']), len(block_vertices))
			return

		# Re-write the recalculated vertices to the VBO
		GL.glBindBuffer(GL.GL_ARRAY_BUFFER, self.vertex_vbo)
		GL.glBufferSubData(GL.GL_ARRAY_BUFFER,
			               self.blocks[block]['vertex_offset']*ctypes.sizeof(ctypes.c_float),
			               self.blocks[block]['vertex_size']*ctypes.sizeof(ctypes.c_float),
			               (ctypes.c_float*len(block_vertices))(*block_vertices))


	def prepare(self):
		"""
		Prepare the VBO
		"""

		self.logger.debug("%s: Preparing VBO for blocks", self)

		vertices = []
		colors = []

		for block in self.blocks.keys():

			r,g,b = self.color_map.color(block)

			try:
				block_vertices = getVerticesLibrary[block.block_type](block)
			
			except KeyError:
				self.logger.warning("%s: Vertices for block type %s not in library", self, block.block_type)
				block_vertices = None

			# Provide a warning if the vertices were not created
			if block_vertices is None:
				self.logger.warning("%s: No Vertices Generated for Block: %s", self, str(block))

				# Put in a "dummy" empty list of vertices, to ensure that the 
				# block is still handled properly -- in effect, treat the 
				# block like it's an air block or similar
				block_vertices = []


			# Store the offset and size (in number of vertex) of the block
			self.blocks[block]['vertex_offset'] = len(vertices)
			self.blocks[block]['vertex_size'] = len(block_vertices)


			# Set the color
			for i in range(len(block_vertices) // 3):
				colors += [float(r)/255,float(g)/255,float(b)/255]

			vertices += block_vertices


		GL.glBindBuffer(GL.GL_ARRAY_BUFFER, self.vertex_vbo)
		GL.glBufferData(GL.GL_ARRAY_BUFFER, 
			            len(vertices)*ctypes.sizeof(ctypes.c_float), 
			            (ctypes.c_float*len(vertices))(*vertices), 
			            GL.GL_DYNAMIC_DRAW)

		GL.glBindBuffer(GL.GL_ARRAY_BUFFER, self.color_vbo)
		GL.glBufferData(GL.GL_ARRAY_BUFFER, 
			            len(colors)*ctypes.sizeof(ctypes.c_float), 
			            (ctypes.c_float*len(colors))(*colors), 
			            GL.GL_DYNAMIC_DRAW)

		self.num_vertices = len(vertices)


	def render(self, ignore=None):
		"""
		Render the VBO
		"""

		# Assume that the perspective has already been set up
		self.logger.debug("%s: Rendering VBO", self)

		# Draw the blocks using the color and vertex VBO
		GL.glEnableClientState(GL.GL_VERTEX_ARRAY)
		GL.glBindBuffer(GL.GL_ARRAY_BUFFER, self.vertex_vbo)
		GL.glVertexPointer(3, GL.GL_FLOAT, 0, None)

		GL.glEnableClientState(GL.GL_COLOR_ARRAY)
		GL.glBindBuffer(GL.GL_ARRAY_BUFFER, self.color_vbo)
		GL.glColorPointer(3, GL.GL_FLOAT, 0, None)

		GL.glDrawArrays(GL.GL_QUADS, 0, self.num_vertices)

		GL.glDisableClientState(GL.GL_VERTEX_ARRAY)
		GL.glDisableClientState(GL.GL_COLOR_ARRAY)
