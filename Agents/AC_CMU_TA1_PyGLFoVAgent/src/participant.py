"""
Class encapsulating all components specific to a participant, including the
participant's perspective, location, and endpoints.
"""

import enum

import pygl_fov
###import logging

from MinecraftBridge.utils import Loggable

import MinecraftElements

class Participant(Loggable):
	"""
	Participant instances are lightweight objects containing information needed
	to process the FoV of the participant.
	"""

	class Role(enum.Enum):
		"""
		An enumeration of roles available to the participant
		"""

		none = "none"
		Search_Specialist = "Search_Specialist"
		Hazardous_Material_Specialist = "Hazardous_Material_Specialist"
		Medical_Specialist = "Medical_Specialist"



	def __init__(self, name, **kwargs):
		"""
		Create a new participant
		"""

		# Store the participant's name and a string representation of the 
		# instance
		self.name = name
		self.__string_name = '[Participant - <%s>]' % self.name


		# Knowing the participant's role may be necessary in the future, so
		# have an attribute for it now.
		self.role = Participant.Role.none

		# Is the participant carrying a victim
		self.victim_block = None

		# Position and orieintation of the participant
		self.position = kwargs.get("position", (0,0,0))
		self.orientation = kwargs.get("orientation", (0,0,0))

		# FoV related information
		self.window_size = kwargs.get("window_size", (640,480))

		# Create a block and vertex for the participant
		self.block = pygl_fov.Block(self.position, 
			                        block_type=MinecraftElements.Block.player,
			                        orientation=self.orientation,
			                        playername=self.name)

		self.vertices = pygl_fov.PlayerVboStore(self.block, self.name)


	def set_pose(self, position, orientation):
		"""
		Set the pose of the Participant

		Args:
			position    - (x, y, z) position of the participant
			orientation - (roll, pitch, yaw) of the participant
		"""

		self.logger.debug("%s:  Setting pose: position = %s; orientation = %s", self, str(position), str(orientation))

		self.position = position
		self.orientation = orientation

		# Propagate the pose to the block
		self.block.location = self.position
		self.block.orientation = (0, self.orientation[1], 0)


	def __str__(self):
		"""
		String representation of the instance
		"""

		return self.__string_name


	def __del__(self):
		"""
		Callback when the participant instance is destroyed
		"""

		pass
