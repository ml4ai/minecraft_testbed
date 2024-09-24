"""
A PlayerVBOStore is a special case of a vertex store that stores and updates a
set of quads to draw a player's avatar.
"""


from ..id_color_mapper import BlockColorMapper

import numpy as np

import logging

import ctypes

from ..vertices import getCuboidVertices

from OpenGL import GL


class PlayerVboStore:
	"""
	A Player VBO store 
	"""

	@staticmethod
	def getPlayerVertices(position, orientation):
		"""
		Get verticies of the quads defining a player's avatar, given the
		position and orientation.
		"""

		## Minecraft coordinates:
		#  +z (south) is at 0 degrees
		#  +x (west)  is at -90 degrees
		#  -x (east)  is at 90 degrees
		#  -z (north) is at 180 degrees

		x,y,z = position

		vertices = []

		# Head - 8 x 8 x 8 pixel (1/2 x 1/2 x 1/2 unit) cube
		vertices += getCuboidVertices((x-0.25, y+1.5, z-0.25), (x+0.25, y+2, z+0.25))

		# Body - 4 x 8 x 24 pixel (1/4 x 1/2 x 1-1/2 unit) cuboid
#		vertices += getCuboidVertices((x-0.125, y, z-0.125), (x+0.25, y+1.5, z+0.125))
		vertices += getCuboidVertices((x-0.25, y, z-0.125), (x+0.25, y+1.5, z+0.125))

		# Arms - 4 x 4 x 12 pixel (1/4 x 1/4 x 3/4 unit) cuboid
#		vertices += getCuboidVertices((x-0.125, y+0.75, z-0.5), (x+0.125, y+1.5, z-0.25))
#		vertices += getCuboidVertices((x-0.125, y+0.75, z+0.25), (x+0.125, y+1.5, z+0.5))

		vertices += getCuboidVertices((x-0.5, y+0.75, z-0.125), (x-0.25, y+1.5, z+0.125))
		vertices += getCuboidVertices((x+0.25, y+0.75, z-0.125), (x+0.5, y+1.5, z+0.125))

		return vertices


	def __init__(self, player_block, name=None, color_map=BlockColorMapper()):
		"""
		Args:
			player_block - a "dummy" Block instance containing the player's ID
			               (for color mapping), position, and orientaiton.
		"""

		# Name of the vertex store, in case multiple instances exist
		self.name = name

		# Create a name for the StaticVboStore to use, and grab the instance of
		# the logger.
		self.logger = logging.getLogger(__name__)
		if self.name is None:
			self.__string_name = '[PlayerVboStore]'
		else:
			self.__string_name = '[PlayerVboStore - %s]' % self.name

		# Retain a copy of the player block, and register this objects to get
		# updates on position, orientation, etc.
		self.block = player_block
		self.block.register(self)
		self.color = (0,0,0)

		# Object to convert Blocks to color and back
		self.color_map = color_map

		# Vertex and Color buffers
		self.vertex_vbo = GL.glGenBuffers(1)
		self.color_vbo = GL.glGenBuffers(1)
		self.num_vertices = 0

		# The vertices of the player will be calculated once, and translated 
		# and rotated as needed
		self.base_vertices = np.zeros((0,3))

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


	def __getTransformedVertices(self):
		"""
		Translate and rotate the base vertices by the current position and
		orientation of the player block and return a list of transformed
		vertices.
		"""

		# Rotate along the y-axis only:  Minecraft pitch and yaw are weird
		rotation = self.block.orientation[1] * np.pi / 180.0

		vertices = self.base_vertices.copy()
		vertices[:,0] = np.cos(rotation) * vertices[:,0] + np.sin(rotation) * vertices[:,2]
		vertices[:,2] = -np.sin(rotation) * vertices[:,0] + np.cos(rotation) * vertices[:,2]

		vertices += np.array(self.block.location)

		return np.reshape(vertices, (-1)).tolist()


	def add(self, block):
		"""
		Does nothing.  Included to conform to other vertex store classes
		"""

		pass


	def onBlockModified(self, block, modifications=set()):
		"""
		Callback from the player block when it is modified.  Recalculate the
		vertices of the avatar and reload into the VBO.

		Args:
			block - Block instance that was modified (should be player block)
		"""

		self.logger.debug("%s: Block Modified: %s", self, block)

		# Rotate and translate the base vertices to get the current vertices
		vertices = self.__getTransformedVertices()

		# Re-write the recalculated vertices to the VBO
		GL.glBindBuffer(GL.GL_ARRAY_BUFFER, self.vertex_vbo)
		GL.glBufferSubData(GL.GL_ARRAY_BUFFER, 0, len(vertices)*ctypes.sizeof(ctypes.c_float),
			               (ctypes.c_float*len(vertices))(*vertices))

		self.num_vertices = len(vertices)



	def prepare(self):
		"""
		Prepare the VBO
		"""

		self.logger.debug("%s: Preparing VBO for blocks", self)

		colors = []

		self.color = self.color_map.color(self.block)
		r,g,b = self.color

		# Calculate the vertices for the block -- reshape these to be an Nx3 
		# array of vertices for easy transformation
		self.base_vertices = np.array(PlayerVboStore.getPlayerVertices((0,0,0), (0,0,0)))
		self.base_vertices = np.reshape(self.base_vertices, (-1,3))

		# Rotate and translate the base vertices to get the current vertices
		vertices = self.__getTransformedVertices()

		# Set the color
		for i in range(len(vertices) // 3):
			colors += [float(r)/255,float(g)/255,float(b)/255]


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
