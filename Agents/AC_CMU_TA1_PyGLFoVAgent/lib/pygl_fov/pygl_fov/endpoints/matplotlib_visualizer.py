"""
matplotlib_visualizer.py

A collection of classes for visualizing the Field of View using Matplotlib.
Visualization is performed by instantiating a MatplotWindow, and adding one
or more Visualizer instances.
"""


import numpy as np

import matplotlib

import matplotlib.pyplot as plt 
from matplotlib import colors, cm
from matplotlib.colors import ListedColormap

import MinecraftElements

import time

import logging

class MatplotWindow:
	"""
	MatplotWindow creates and maintains the main window for visualizing data
	using one or more Visualizers.  Each Visualizer is used to visualize a
	specific type of data.  Each Visualizer instance is responsible for setup
	of the visualization, and update of values visualized.
	"""

	def __init__(self):
		"""
		Create a MatplotWindow
		"""

		# List of visualizers that will be rendered
		self.visualizers = []

		self.logger = logging.getLogger(__name__)
		
		# Create the figure 
		plt.ion()
		self.figure = plt.figure()

		# Do the initial plot
		self.figure.show()


	def __str__(self):
		"""
		String representation of the window
		"""

		return '[MatplotWindow]'


	def add(self, visualizer, position, title=None):
		"""
		Construct the provided visualizer in the provided position

		visualizer - instance of MatplotVisualizer
		position   - location of the visualizer, following the format of
		             Matplotlib's subplot (e.g., 312)
		title      - Optional title for the visualizer
		"""

		# Create the subplot within the figure
		axes = self.figure.add_subplot(position)

		if title is not None:
			axes.set_title(title)

		# Build the and store the visualizer
		visualizer.construct(axes)
		self.visualizers.append(visualizer)


	def close(self):
		"""
		Close the Matplot window
		"""

		plt.close(self.figure)


	def redraw(self):
		"""
		Re-render the all visualizers in the Matplot window
		"""

		# Explicitly call the update methods for each visualizer
		for visualizer in self.visualizers:
			visualizer.update()

		# Perform and flush all rendering operations on the actual canvas
		self.figure.canvas.draw_idle()
		self.figure.canvas.flush_events()




class MatplotVisualizer:
	"""
	A abstract version of a Matplot visualizer.  Specific visualizers should
	subclass this class, and implement the needed functionality to construct
	and update.
	"""

	def __init__(self):
		"""
		Initialize common components of all visualizers, i.e., the axes that
		the visualizer will be drawn to.
		"""

		# This is unknown until build is called.
		self.axes=None

		self.logger = logging.getLogger(__name__)


	def __str__(self):
		"""
		String representation
		"""

		return '[MatplotVisualizer]'


	def construct(self, axes):
		"""
		Store the provided axis for the visualizer, and call the subclass
		specific build method.
		"""
		
		# Store the axes
		self.axes = axes

		# Call the subclass-specific build method to build the visualization
		self.build()


	def build(self):
		"""
		The build method is called to create a subclass-specific visualization
		"""

		raise NotImplementedError


	def update(self):
		"""
		The update method is called whenever visualization should be updated.
		It is assumed that the specific subclass instance has the ability to
		access necessary data, as data is not passed to the update method.
		"""
		
		raise NotImplementedError




class SemanticMapVisualizer(MatplotVisualizer):
	"""
	Convert the field of view to a semantic map
	"""

	@staticmethod
	def loadColorsFromCSV(filename):
		"""
		Load a colormap from the provided filename

		Args:
			filename - path to a CSV file containing color definitions

		Returns:
			numpy array of RGB colors for each block type
		"""

		# TODO: Check if the file exists
		with open(filename) as csv_file:
			lines = csv_file.readlines()[1:]
			color_data = [[x.strip() for x in line.split(',')] for line in lines]
			color_dictionary = {c[0]: [int(value) for value in c[1:]] for c in color_data}

		# Create an Nx3 array of zeros, where N is 2 larger than the largest
		# value in MinecraftElements.Block:  one entry is added to account for
		# indexing from zero, while the last entry will be for invalid block
		# numbers (i.e., pixels where no blocks were rendered).
		color_map = np.zeros((max(MinecraftElements.Block)+2,3), dtype=np.int)

		# Populate the map with entries from the color dictionary
		for block_name, color in color_dictionary.items():
			color_map[MinecraftElements.Block[block_name]] = color

		return color_map


	def __init__(self, shape, block_feeder, colormap=None):
		"""
		Create a visualization of the field of view that generates a semantic
		colormap of block types

		Args:
			shape        - dimensions of the player's view
			colormap     - an Nx3 dimensional array, where N is 2 more than the
			               largest value in MinecraftElements.Block (257)
			block_feeder - instance of a block feeder, containing the blocks in
			               the world
		"""

		# Initialize abstract parent class parameters
		MatplotVisualizer.__init__(self)

		self.logger = logging.getLogger(__name__)

		# Store the colormap, and shape of the output
		self.colormap = colormap
		self.shape = shape

		self.data = None
		self.values = None

		self.block_feeder = block_feeder

		# No colormap provided?  Use random colors
		if self.colormap is None:
			colormap_shape = (max(MinecraftElements.Block)+2, 3)
			self.colormap = np.random.randint(0, 256, colormap_shape, dtype=np.int)

		# Register this with the block feeder and each block
		self.block_feeder.register(self)
		for block in self.block_feeder:
			block.register(self)

		# Create the initial ID-to-block-type map
		max_id = 0
		for block in self.block_feeder:
			max_id = max(max_id, block.id)

		self.id_to_type = np.zeros((max_id+2,))

		# Map block IDs to block types
		for block in self.block_feeder:
			self.id_to_type[block.id] = block.block_type

		# Keep a "dummy" value at the end of the map for pixels with 
		# non-corresponding blocks (i.e, -1).  Use a "structure_block" as a 
		# dummy block
		self.id_to_type[max_id+1] = MinecraftElements.Block.structure_block


	def __str__(self):
		"""
		String representation of the visualizer
		"""

		return '[SemanticMapVisualizer]'


	# Callbacks from the block feeder and blocks
	def onBlockAddedToFeeder(self, feeder, block):
		"""
		Callback from block feeder instances indicating when a block has been
		added to the feeder

		Args:
			feeder - instance of the block feeder
			block  - block added to the feeder
		"""

		self.logger.debug("%s:  Callback from Feeder %s -- Added Block %s", self, feeder, block)

		# Add rows to the id_to_type map so that there are sufficient entires
		# Remember to keep the extra entry for the dummy block
		num_rows = block.id - len(self.id_to_type) + 2
		if num_rows > 0:
			self.id_to_type = np.append(self.id_to_type,[np.zeros(num_rows,)])
			# Set the last block to a dummy block
			self.id_to_type[len(self.id_to_type)-1] = MinecraftElements.Block.structure_block

		self.id_to_type[block.id] = block.block_type

		# Register this with the added block
		block.register(self)

		self.logger.debug("%s:    Number of Blocks in Feeder: %d", self, len(self.block_feeder))
		self.logger.debug("%s:    Number of ID to Type Entries: %d", self, len(self.id_to_type))


	def onBlockFeederUpdate(self, feeder):
		"""
		Callback from block feeder instances indicating when the feeder has 
		been updated

		Args:
			feeder - instance of the updated block feeder
		"""

		self.logger.debug("%s:  Callback from Feeder %s -- Feeder Updated", self, feeder)

		pass


	def onBlockModified(self, block):
		"""
		Callback from a block indicating that some property of the block has 
		changed.

		Args:
			block - instance of the updated block
		"""

		self.logger.debug("%s:  Handling Block %s modified", self, block)

		self.id_to_type[block.id] = block.block_type


	def build(self):
		"""
		Construct the initial representation of the semantic map, which is just
		a black screen.
		"""

		self.values = np.zeros((self.shape[1], self.shape[0], 3))
		self.data = plt.imshow(self.values, interpolation="none")


	def update(self):
		"""
		Update the semantic map to reflect the current contents of values
		"""

		self.data.set_data(self.values)

		plt.pause(0.0001)


	def save(self, path):
		"""
		Save the current plot
		"""

		plt.savefig(path)


	def __call__(self, pixelMap):
		"""
		Calculate the semantic map from the pixelMap, and update the
		visualization
		"""

		# Set the values equal to the mapping of block_id to type.  Also, any
		# invalid block IDs (not in the block feeder) should be set to the 
		# "dummy block" index
		pixelMap[pixelMap>len(self.id_to_type)] = len(self.id_to_type)-1

		self.values = self.colormap[(self.id_to_type[pixelMap.T]).astype(np.int)]

		self.update()
