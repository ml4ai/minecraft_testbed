"""
fov.py

This file defines the main class for calculating the blocks in the player's
Field of View.
"""

import numpy as np

from OpenGL import GL

import time

from .vertices import *
from .id_color_mapper import BlockColorMapper
from .vertex_store import StaticVboStore

import ctypes

import logging


class FOV:
	"""
	FOV is the main class to generate a machine readable version of the field
	of view of the player.  FOV contains instances of a Perspective and 
	a class capable of iterating over Blocks and accessing by ID (e.g., a list
	or equivalent), and uses these to construct the scene, render, and
	convert the output to 2D array containing the block ID of each pixel.

	Downstream processes can use the generated ID-to-pixel map and set of 
	Block instances to perform filtering and post-processing.

	The FOV class can be used in two ways:
		1.  The array can be generated directly by a client, by calling the 
		    getIDArray method.
		2.  The FOV can be set up in an observation chain, by registering it as
		    an observer for its Perspective and BlockFeeder instances, and 
		    allowing any post-processing to be registered as observers.

	If set up in an observation chain, the FOV will receive indications from
	the perspective and block_feeder through calls to its updatePerspective()
	and updateBlockFeed() methods.

	Doenstream processes can register themselves as observers to the FOV with
	the register() and deregister() methods, and will receive notifications
	when the FOV changes through the updateFOV() method.
	"""

	def __init__(self, perspective, vertex_store, observeComponents=True, color_map=BlockColorMapper()):
		"""
		Create a FOV

		Args:
			perspective  - an instance of a Perspective, used to compute the
			               perspective of the player's FoV
			block_feeder - a list (or equivalent) of Blocks.  Instance must be
			               able to iterate over blocks, and access blocks via 
			               their ID.
			observeComponents - a boolean indicating whether the instance 
			                    should register itself as observers of the
			                    perspective and block_feeder instances.
		"""

		self.perspective = perspective

		# Numpy array which stores pixel-to-block ID map
		self.pixelToBlockIdMap = np.zeros((0,))

		# Register this with the corresponding components, if desired
		if observeComponents:
			self.perspective.register(self)

		# Registry of observers
		self.observers = set()


		# Vertex and color buffers
		self.vbo_stale = True

		self.color_map = color_map

		# Vertex Store
		self.scene = vertex_store

		self.vbo_stale = False


	def register(self, observer):
		"""
		Register an observer to recieve notifications of changes to the FOV.

		Registered observers need to implement an updateFOV() method to be able
		to be informed of changes.

		observer - object to be informed of changes to the FOV instance
		"""

		self.observers.add(observer)


	def deregister(self, observer):
		"""
		Remove the observer from the registry of observers.

		observer - object to be removed from the registry.
		"""

		if observer in self.observers:
			self.observers.remove(observer)


	def __notify(self):
		"""
		Inform all observers that the pixelToBlockIdMap has been modified.
		"""

		for observer in self.observers:
			observer.updateFOV()


	def __del__(self):
		"""
		"""

		print("FOV delete")


	def updatePerspective(self):
		"""
		Callback to indicate when the FOV's perspective instance has been 
		modified.
		"""

		# Re-calculate the pixel to block map ID
		_ = self.calculatePixelToBlockIdMap()

		# Notify all observers that the FOV has changed
		self.__notify()


	def updateBlockFeed(self):
		"""
		Callback to indicate when the FOV's block feed has been modified.
		"""

		# Re-calculate the pixel to block map ID
		_ = self.calculatePixelToBlockIdMap()

		# Notify all observers that the FOV has changed
		self.__notify()

		

	def prepareVBO(self):
		"""
		Create the VBO
		"""

		self.scene.prepare()

		self.vbo_stale = False


	def render(self, perspective=None, ignore=[], colorPicker=None):
		"""
		Render the world to the screen
		"""

		# Create the VBO, if it doesn't exist
		if self.vbo_stale:
			self.prepareVBO()

		# Clear the screen
		GL.glClear(GL.GL_COLOR_BUFFER_BIT | GL.GL_DEPTH_BUFFER_BIT)
		GL.glMatrixMode(GL.GL_MODELVIEW)
		GL.glLoadIdentity()
	
		# Set up the perspective, use the default perspective if none is
		# provided
		if perspective is not None:	
			perspective.setup()
		else:	
			self.perspective.setup()

		# Render the scene
		self.scene.render(ignore=ignore)



	def calculatePixelToBlockIdMap(self, perspective=None, ignore=[]):
		"""
		Calculate an array mapping pixel locations to block ID.

		The map is stored as the pixelToBlockIdMap attribute.

		Return:
		    The pixelToBlockIdMap attribute
		"""

		# Render the scene
		self.render(perspective=perspective, ignore=ignore)

		# Get the resulting image from the perspective
		if perspective is not None:
			blockIdImage = perspective.getImage()
		else:
			blockIdImage = self.perspective.getImage()

		self.pixelToBlockIdMap = self.color_map.id((blockIdImage[:,:,0], 
			                                        blockIdImage[:,:,1], 
			                                        blockIdImage[:,:,2]))
		
		return self.pixelToBlockIdMap

