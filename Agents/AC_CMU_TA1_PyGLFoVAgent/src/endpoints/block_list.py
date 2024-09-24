# -*- coding: utf-8 -*-
"""
.. module:: block_location_list
   :platform: Linux, Windows, OSX
   :synopsis: Module containing endpoint for providing a list of block 
              locations in the player's field of view.

.. moduleauthor:: Dana Hughes <danahugh@andrew.cmu.edu>

This module contains an endpoint class for producing messages that contain the
(x,y,z) location of each block in the player's Field of View.  The purpose is 
to provide information of which blocks have been seen, but not have details on
pixel counts or locations in order to minimize message size
"""

###import logging
from MinecraftBridge.utils import Loggable

import pygl_fov.endpoints

from MinecraftBridge.messages import FoV_BlockLocationList, BusHeader, MessageHeader
from MinecraftBridge.mqtt.parsers import MessageType, MessageSubtype

import MinecraftElements

import numpy as np

import datetime


class BlockLocationListMessageEndpoint(Loggable):
	"""
	A BlockLocationListMessage endpoint generates a list of the (x,y,z)
	location of each block in the player's Field of View.
	"""


	class Factory(Loggable):
		"""
		A Factory for creating BlockLocationListMessageEndpoint instances.
		"""

		def __init__(self, worker, **kwargs):
			"""
			Create a BlockLocationListEndpoint Factory

			Args:
				worker - instance of the FoVWorker that uses this factory to
				         create endpoints for discovered participants.
			"""

			self.worker = worker
			self.fov_agent = kwargs.get("fov_agent", None)
			self.timestamp_delay = kwargs.get("timestamp_delay", -1)

###			# Grab a handle to logger for the class, if it exists, or the default
###			# logger
###			if self.__class__.__name__ in logging.Logger.manager.loggerDict:
###				self.logger = logging.getLogger(self.__class__.__name__)
###			else:
###				self.logger = logging.getLogger(__name__)


		def __call__(self, participant):
			"""
			Create a BlockSummaryMessageEndpoint instance for the provided
			participant.

			Args:
				participant - participant whose FoV is used to provide block ID
				              maps in the generated instance.
			"""

			if self.worker is None:
				self.logger.error("%s:  Unable to create instance of BlockSummaryMessageEndpoint.  Provided worker handle is None.", self)
				return lambda: None

			if self.fov_agent is None:
				self.logger.error("%s:  Unable to create instance of BlockSummaryMessageEndpoint.  FoV agent / message bus not provided", self)
				return lambda: None


			# Create the location list generator
			location_list_generator = pygl_fov.endpoints.BlockLocationList(self.worker.world)

			return BlockLocationListMessageEndpoint(self.fov_agent, location_list_generator,
				                                    timestamp_delay=self.timestamp_delay)



	def __init__(self, message_bus, location_list_generator, **kwargs):
		"""
		Create a new endpoint, connected to the supplied bridge.

		The optional timestamp_delay argument will timestamp the bus and message
		header by the provided delay amount (in seconds).  If the delay is None
		or negative, then the message headers will be timestamped using the 
		current time.

		Args:
			message_bus - handle to the bridge to the message bus to publish to
			location_list_generator - object to generate list of block locations
			                          from pixelMap data

		Keyword Arguments:
			timestamp_delay - amount of time to advance the timestamp of the 
			                  message from the received PlayerState message.
			message_source  - string name for the message header source
			message_type    - instance of MinecraftBridge.messages.MessageType
			message_subtype - instance of MinecraftBridge.messages.MessageSubtype
			testbed_version - version number of the testbed
		"""

		# String representation of the instance
		self.__string_name = "[BlockLocationListMessageEndpoint]"

		# Store the timestamp_delay, converting to None if negative
		self.timestamp_delay = kwargs.get("timestamp_delay", None)
		if self.timestamp_delay is not None and self.timestamp_delay < 0:
			self.timestamp_delay = None

		# Store keyword arguments, or default values in not provided
		self.message_source = kwargs.get("message_source", "PyGL_FoV_Agent")
		self.message_type = kwargs.get("message_type", MessageType.observation)
		self.message_subtype = kwargs.get("message_subtype", MessageSubtype.FoV_BlockLocationList)
		self.testbed_version = kwargs.get("testbed_version", 0.5)
		self.timestamp_delay = kwargs.get("timestamp_delay", -1)

###		# Grab a handle to logger for the class, if it exists, or the default
###		# logger
###		if self.__class__.__name__ in logging.Logger.manager.loggerDict:
###			self.logger = logging.getLogger(self.__class__.__name__)
###		else:
###			self.logger = logging.getLogger(__name__)

		# Store the message bus handle
		self.message_bus = message_bus
		self.location_generator = location_list_generator


	def __str__(self):
		"""
		String representation of the instance
		"""

		return self.__string_name


	def create_headers(self, player_state_message):
		"""
		Create the bus and message headers using the contents of the player
		state message
		"""

		if player_state_message is None:
			self.logger.error("%s:  Attempting to create message headers with 'None' PlayerState message", self)
			return

		# Get the experiment_id, trial_id, and replay_id (if it exists), and
		# timestamps from the player_state_message
		experiment_id = player_state_message.headers["msg"].experiment_id
		trial_id = player_state_message.headers["msg"].trial_id
		replay_id = player_state_message.headers["msg"].replay_id


		# Calculate the timestamps for the bus and message headers
		if self.timestamp_delay is not None and self.timestamp_delay > 0:
			bus_timestamp = player_state_message.headers["header"].timestamp
			msg_timestamp = player_state_message.headers["msg"].timestamp

			# Parse the timestamps, and advance by the number of seconds
			bus_timestamp = bus_timestamp + datetime.timedelta(seconds=self.timestamp_delay)
			msg_timestamp = msg_timestamp + datetime.timedelta(seconds=self.timestamp_delay)

		else:
			bus_timestamp = datetime.datetime.utcnow()
			msg_timestamp = datetime.datetime.utcnow()


		# Create the bus and message headers
		bus_header = BusHeader(self.message_type, 
			                   timestamp=bus_timestamp,
			                   version=self.testbed_version)

		msg_header = MessageHeader(self.message_subtype,
			                       experiment_id,
			                       trial_id,
			                       self.message_source,
			                       timestamp=msg_timestamp,
			                       version=self.testbed_version,
			                       replay_id=replay_id)

		return bus_header, msg_header


	def __call__(self, pixelMap, **kwargs):
		"""
		Calculate the list of block locations in the field of view, construct a
		message and send to the bus
		"""

		self.logger.debug("%s: Generating Block Location List Message", self)

		# Get the original player state message to get needed information,
		# e.g., observation_number
		player_state_message=kwargs.get("player_state_message", None)

		if player_state_message is None:
			self.logger.error("%s:  Unable to create BlockLocationList message -- PlayerState message not provided.", self)
			return

		# Create the bus and message headers
		busHeader, msgHeader = self.create_headers(player_state_message)

		# Create the FoV_BlockLocationList message
		message = FoV_BlockLocationList(playername=player_state_message.name,
			                            observationNumber=player_state_message.observation_number,
			                            locations=self.location_generator(pixelMap))

		message.addHeader("header", busHeader)
		message.addHeader("msg", msgHeader)

		self.message_bus.publish(message)




