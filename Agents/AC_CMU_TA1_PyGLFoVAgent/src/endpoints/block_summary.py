"""
block_summary.py

The BlockSummaryMessageEndpoint defines a wrapper for the pygl_fov 
FilteredBlockListSummary endpoint, by converting the list of block summaries to
a message, as well as defining a Factory to create the endpoint.
"""

###import logging
from MinecraftBridge.utils import Loggable

import pygl_fov.endpoints

from MinecraftBridge.messages import FoVSummary, BusHeader, MessageHeader
from MinecraftBridge.mqtt.parsers import MessageType, MessageSubtype

import MinecraftElements

import numpy as np

import datetime
#from dateutil.parser import isoparse


class BlockSummaryMessageEndpoint(Loggable):
	"""
	A BlockSummaryMessage endpoint calcualtes the pixel statistics of blocks of
	interest using the pygl_fov FilteredBlockSummary endpoint, and creates a
	message to put on the bus with the resulting summary contents.
	"""


	class Factory(Loggable):
		"""
		A Factory for creating BlockSummaryMessageEndpoint instances.
		"""

		def __init__(self, worker, **kwargs):
			"""
			Create a BlockSummaryMessageEndpoint Factory

			Args:
				worker - instance of the FoVWorker that uses this factory to
				         create endpoints for discovered participants.
			"""

			if not "scaling_factor" in kwargs:
				self.logger.warning("%s: No Scaling Factor!", self)

			self.worker = worker
			self.block_list = kwargs.get("blocks_to_summarize", None)
			self.fov_agent = kwargs.get("fov_agent", None)
			self.timestamp_delay = kwargs.get("timestamp_delay", -1)
			self.scaling_factor = kwargs.get("scaling_factor", 1)


			# If no blocks were provided to summarize, assume that all block
			# types are to be summarized
			if self.block_list is None:
				self.block_list = set(MinecraftElements.Block)
			else:
				# Convert the string representation of blocks to
				# MinecraftElements.Block instances
				self.block_list = set([MinecraftElements.Block[block] for block in self.block_list])


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


			# Create the 
			block_list_summary = pygl_fov.endpoints.FilteredBlockListSummary(self.worker.world,
				                                                             self.block_list)

			return BlockSummaryMessageEndpoint(self.fov_agent, block_list_summary, 
				                               timestamp_delay=self.timestamp_delay,
				                               scaling_factor=self.scaling_factor)



	def __init__(self, message_bus, block_summary_endpoint, **kwargs):
		"""
		Create a new endpoint, connected to the supplied bridge.

		The optional timestamp_delay argument will timestamp the bus and message
		header by the provided delay amount (in seconds).  If the delay is None
		or negative, then the message headers will be timestamped using the 
		current time.

		Args:
			message_bus - handle to the bridge to the message bus to publish to
			block_summary_endpoint - instance of a FilteredBlockListSummary

		Keyword Arguments:
			timestamp_delay - amount of time to advance the timestamp of the 
			                  message from the received PlayerState message.
			scaling_factor  - amount to scale the pixel count and bounding box
			                  values, based on the difference of actual viewport
			                  dimentions from "standard" viewport dimensions
			message_source  - string name for the message header source
			message_type    - instance of MinecraftBridge.messages.MessageType
			message_subtype - instance of MinecraftBridge.messages.MessageSubtype
			testbed_version - version number of the testbed
		"""

		# String representation of the instance
		self.__string_name = "[BlockSummaryMessageEndpoint]"

		# Store the timestamp_delay, converting to None if negative
		self.timestamp_delay = kwargs.get("timestamp_delay", None)
		if self.timestamp_delay is not None and self.timestamp_delay < 0:
			self.timestamp_delay = None
		self.scaling_factor = kwargs.get("scaling_factor", 1)
		if self.scaling_factor <= 0:
			self.scaling_factor = 1

		# Store keyword arguments, or default values in not provided
		self.message_source = kwargs.get("message_source", "PyGL_FoV_Agent")
		self.message_type = kwargs.get("message_type", MessageType.observation)
		self.message_subtype = kwargs.get("message_subtype", MessageSubtype.FoV)
		self.testbed_version = kwargs.get("testbed_version", 0.5)
		self.timestamp_delay = kwargs.get("timestamp_delay", -1)


		# Store the base endpoint and message bus
		self.block_summary_endpoint = block_summary_endpoint
		self.message_bus = message_bus


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
		Calculate the pixel statistics of blocks of intetest, construct a
		message and send to the bus
		"""

		self.logger.debug("%s: Generating Block Summary Message", self)

		# Get the original player state message to get needed information,
		# e.g., observation_number
		player_state_message=kwargs.get("player_state_message", None)

		if player_state_message is None:
			self.logger.error("%s:  Unable to create BlockSummary message -- PlayerState message not provided.", self)
			return

		# Create the bus and message headers
		busHeader, msgHeader = self.create_headers(player_state_message)

		# Calculate the block summary
		blockSummary = self.block_summary_endpoint(pixelMap)

		# Get the player's name and the observation number for the message data
		playername = player_state_message.name
		observation_number = player_state_message.observation_number

		# Create the FoVSummary message
		message = FoVSummary(playername=playername,
			                 observationNumber=observation_number,
			                 blocks=[])
		message.addHeader("header", busHeader)
		message.addHeader("msg", msgHeader)

		# Add the blocks that have been summarized
		for summary in blockSummary:

			if summary['block'].victim_id is None:
				_id = -1
			else:
				_id = summary['block'].victim_id


			block_data = { "id":       _id,
				           "location": list(summary['block'].location),
				           "type":     summary['block'].block_type.name,
				           "number_pixels": int(summary['pixel_count'] * (self.scaling_factor**2)),
				           "bounding_box": { "x": [int(summary['bounding_box'][0] * self.scaling_factor), 
				                                   int(summary['bounding_box'][1] * self.scaling_factor)],
				                             "y": [int(summary['bounding_box'][2] * self.scaling_factor),
				                                   int(summary['bounding_box'][3] * self.scaling_factor)]
				                           }
			             }
			if "playername" in summary:
				block_data["playername"] = summary["playername"]

			# Make sure that we don't inadvertently reveal the block type of regular victims
			if block_data['type'] in { "block_victim_1", "block_victim_1b", "block_victim_2" }:
				block_data['type'] = "block_victim_regular"
			if block_data['type'] in { "block_victim_saved_a", "block_victim_saved_b", "block_victim_saved_c" }:
				block_data['type'] = "block_victim_saved"

			# If it's a marker block, add additional keys to the summary
			if summary['block'].block_type == MinecraftElements.Block.marker_block:
				block_data["marker_type"] = summary['block'].marker_type.name
				block_data["owner"] = summary['block'].playername

			message.addBlock(block_data)

		self.message_bus.publish(message)




