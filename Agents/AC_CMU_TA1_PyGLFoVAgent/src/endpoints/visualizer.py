"""
A simple wrapper for the pygl_fov Matplotlib visualizer.
"""

import pygl_fov.endpoints

###import logging
from MinecraftBridge.utils import Loggable

class MatplotVisualizer(Loggable):
	"""
	A simple wrapper of the pygl_fov components to create a visualizer using
	Matplotlib
	"""


	class Factory(Loggable):
		"""
		A factory for creating MatplotVisualizer instances.  The factory is
		responsible for creating the MatplotWindow instance, and adding the
		instances of SemanticMapVisualizers to the window.
		"""

		def __init__(self, worker, **kwargs):
			"""
			Create a new MatplotVisualizer Factory
			"""

			self.colormap_path = kwargs.get('colormap_path', None)
			self.worker = worker

###			# Grab a handle to logger for the class, if it exists, or the default
###			# logger
###			if self.__class__.__name__ in logging.Logger.manager.loggerDict:
###				self.logger = logging.getLogger(self.__class__.__name__)
###			else:
###				self.logger = logging.getLogger(__name__)



		def __call__(self, participant):
			"""
			Create a specific MatplotVisualizer for the player
			"""

			if self.worker is None:
				self.logger.error("%s:  Unable to create instance of MatplotVisualizer endpoint.  Provided worker handle is None.", self)
				# Return a dummy function, to avoid crashing later on
				return lambda: None

			# Create the visualizer, and register it with the worker's world
			# block feeder to receive updates on block changes
			visualizer = MatplotVisualizer(participant.window_size, self.worker.world, self.colormap_path, participant)
			self.worker.world.register(visualizer)


			return visualizer



	def __init__(self, window_size, feeder, colormap_path=None, participant=None):
		"""
		Create a new visualizer with the provided window size and block feeder

		Args:
			window_size - (width, height) of the desired window
			feeder      - instance of a block_feeder
		"""

		# Determine what the colormap is
		if colormap_path is not None:
			# TODO: Validate, warnings, etc.
			colormap = pygl_fov.endpoints.SemanticMapVisualizer.loadColorsFromCSV(colormap_path)
		else:
			colormap = None

###		# Grab a handle to logger for the class, if it exists, or the default
###		# logger
###		if self.__class__.__name__ in logging.Logger.manager.loggerDict:
###			self.logger = logging.getLogger(self.__class__.__name__)
###		else:
###			self.logger = logging.getLogger(__name__)

		# Get the name of the participant, to use as a title for the plot
		if participant is not None:
			participant_name = participant.name
		else:
			participant_name = None

		self.plotWindow = pygl_fov.endpoints.MatplotWindow()
		self.visualizer = pygl_fov.endpoints.SemanticMapVisualizer(window_size, feeder, colormap)
		self.plotWindow.add(self.visualizer, 111, participant_name)


	def __call__(self, pixelMap, **kwargs):
		"""
		Pass the pixelmap to the visualizer to render

		Args:
			pixelMap - 2D pixelmap of the block IDs
		"""

		self.visualizer(pixelMap)


	# Callbacks from the block feeder and blocks
	def onBlockAddedToFeeder(self, feeder, block):
		"""
		Callback from the block feeder instances indicated when a block has been
		added to the feeder

		Args:
			feeder - instance of the block feeder
			block  - block added to the feeder
		"""

		self.logger.debug("%s:  Handling Block %s added to Feeder %s.", self, block, feeder)

		# Propagate the callback to the visualizer
		self.visualizer.onBlockAddedToFeeder(feeder, block)


	def onBlockFeederUpdate(self, feeder):
		"""
		Callback from block feeder instances indicating when the feeder has 
		been updated

		Args:
			feeder - instance of the updated block feeder		
		"""

		self.logger.debug("%s:  Handling Feeder %s Updated.", self, feeder)

		# Propagate the callback to the visualizer
		self.visualizer.onBlockFeederUpdate(feeder)


	def onBlockModified(self, block):
		"""
		Callback from a block indicating that some property of the block has 
		changed.

		Args:
			block - instance of the updated block
		"""

		self.logger.debug("%s:  Handling Block %s Modified.", self, block)

		# Propagate the callback to the visualizer
		self.visualizer.onBlockModified(block)