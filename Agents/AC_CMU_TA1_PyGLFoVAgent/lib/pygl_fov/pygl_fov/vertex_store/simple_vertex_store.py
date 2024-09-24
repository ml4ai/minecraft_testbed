"""
A store for a single block, which renders the block directly without the use
of a VBO.  This simplifies rendering a bit, at the expense of speed.  It is,
however, useful in situations where there are not a lot of vertices to render.
"""

from OpenGL import GL
from ..id_color_mapper import BlockColorMapper

import logging

class SimpleVertexStore:
	"""
	A StaticVboStore converts a provided set of blocks to a Vertex Buffer
	Object.  The blocks in this store are assumed to remain static, and should
	never need updating.
	"""

	def __init__(self, vertices, dummy_block, name=None, color_map=BlockColorMapper()):
		"""

		The provided vertices are assumed to be for Quads, so there neds to be
		a multiple of 4 vertices in the list.

		Args:
			vertices - a list of vertices, each vertex represented as a 3-tuple
			dummy_block - a block to use as a placeholder for the block's ID,
			              position, and orientation.
		"""

		# Name of the vertex store, in case multiple instances exist
		self.name = name

		# Create a name for the StaticVboStore to use, and grab the instance of
		# the logger.
		self.logger = logging.getLogger(__name__)
		if self.name is None:
			self.__string_name = '[SimpleVertextore]'
		else:
			self.__string_name = '[SimpleVertexStore - %s]' % self.name

		# Check if the number of vertices is a multiple of 4
		if len(vertices) % 4 != 0:
			self.logger.warning("%s:  Number of vertices provided not a multiple of 4.  Ignoring extra vertices")

		# Store the vertices and link to the block
		self.vertices = vertices
		self.dummy_block = dummy_block
		self.dummy_block.register(self)

		# Object to convert Blocks to color and back
		self.color_map = color_map
		self.color = self.color_map.color(self.dummy_block)

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

		pass


	def onBlockModified(self, block, modifications=set()):
		"""
		Callback from a block when it is modified.  When a block is modified,
		recalculate the vertices and load into the VBO.

		Note that the number of vertices of the block should remain unchanged.
		If the vertex count changes, then log an error.

		Args:
			block - Block instance that was modified
		"""

		self.logger.debug("%s: Block Modified: %s.  Ignoring.", self, block)


	def prepare(self):
		"""
		Prepare the VBO
		"""

		self.logger.debug("%s: Preparing Simple Vertex Store.", self)


	def render(self, ignore=None):
		"""
		Render the VBO
		"""

		# Assume that the perspective has already been set up
		self.logger.debug("%s: Rendering Simple Vertex Store", self)

		# Push the current state of the transformation matrix, so that applying
		# the transformation for *this* block doesn't interfere with the rest
		# of the world
		GL.glPushMatrix()

		GL.glTranslatef(self.dummy_block.location[0], self.dummy_block.location[1], self.dummy_block.location[2])
		GL.glRotatef(self.dummy_block.orientation[0], 1.0, 0.0, 0.0)
		GL.glRotatef(-self.dummy_block.orientation[1], 0.0, 1.0, 0.0)
		GL.glRotatef(self.dummy_block.orientation[2], 0.0, 0.0, 1.0)

		# Set the color to the corresponding ID of the block
		GL.glColor3ub(self.color[0], self.color[1], self.color[2])

		# Draw the quads
		GL.glBegin(GL.GL_QUADS)

		for vertex in self.vertices:
			GL.glVertex3f(vertex[0], vertex[1], vertex[2])

		GL.glEnd()
		GL.glFlush()

		# Restore the state of the world
		GL.glPopMatrix()

