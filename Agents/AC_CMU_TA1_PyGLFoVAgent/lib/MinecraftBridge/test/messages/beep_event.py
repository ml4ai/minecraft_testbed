# -*- coding: utf-8 -*-
"""
.. module:: beep_event
   :platform: Linux, Windows, OSX
   :synopsis: Unit tests for BeepEvent messages

.. moduleauthor:: Dana Hughes <danahugh@andrew.cmu.edu>

Suite of unit tests for BeepEvent messages
"""

from MinecraftBridge.messages import BeepEvent
from MinecraftBridge.messages.message_exceptions import (
	MissingMessageArgumentException,
	MalformedMessageCreationException,
	ImmutableAttributeException
)

import unittest
import numpy as np

class BeepEventCreationTests(unittest.TestCase):
	"""
	A set of test cases to ensure proper behavior during creation of BeepEvent
	messages.
	"""

	def test_valid_creation_with_mission_timer(self):
		"""
		Test creating a valid BeepEvent message, using a string representation
		of the mission time, and the "mission_timer" keyword argument.
		"""

		beep_event_message = BeepEvent(mission_timer="8 : 36",
			                           elapsed_milliseconds=15113,
			                           sourceEntity="Victim Detection Device (player)",
			                           message="beep",
			                           location=(-2185, 28, 198))

		# Simply make sure that a BeepEvent was created
		self.assertIsInstance(beep_event_message, BeepEvent)


	def test_valid_creation_with_missionTimer(self):
		"""
		Test creating a valid BeepEvent message, using a string representation
		of the mission time, and the "missionTimer" keyword argument.
		"""

		beep_event_message = BeepEvent(missionTimer="8 : 36",
			                           elapsed_milliseconds=15113,
			                           sourceEntity="Victim Detection Device (player)",
			                           message="beep",
			                           location=(-2185, 28, 198))

		# Simply make sure that a BeepEvent was created
		self.assertIsInstance(beep_event_message, BeepEvent)


	def test_valid_creation_no_mission_timer(self):
		"""
		Test creating a valid BeepEvent message, without providing a mission
		timer as part of the keywords
		"""

		beep_event_message = BeepEvent(elapsed_milliseconds=15113,
			                           sourceEntity="Victim Detection Device (player)",
			                           message="beep",
			                           location=(-2185, 28, 198))

		# Simply make sure that a BeepEvent was created
		self.assertIsInstance(beep_event_message, BeepEvent)


	def test_valid_creation_no_elapsed_milliseconds(self):
		"""
		Test creating a valid BeepEvent message, without providing elaped
		milliseconds as part of the keyword arguments
		"""

		beep_event_message = BeepEvent(missionTimer="8 : 36",
			                           sourceEntity="Victim Detection Device (player)",
			                           message="beep",
			                           location=(-2185, 28, 198))

		# Simply make sure that a BeepEvent was created
		self.assertIsInstance(beep_event_message, BeepEvent)


	def test_valid_creation_no_mission_timer_or_elapsed_milliseconds(self):
		"""
		Test creating a valid BeepEvent message, without providing mission 
		timer or elaped milliseconds as part of the keyword arguments
		"""

		beep_event_message = BeepEvent(sourceEntity="Victim Detection Device (player)",
			                           message="beep",
			                           location=(-2185, 28, 198))

		# Simply make sure that a BeepEvent was created
		self.assertIsInstance(beep_event_message, BeepEvent)


	def test_valid_creation_list_location(self):
		"""
		Test creating a valid BeepEvent message, providing a list as the
		location argument as opposed to a tuple.
		"""

		beep_event_message = BeepEvent(mission_timer="8 : 36",
			                           elapsed_milliseconds=15113,
			                           sourceEntity="Victim Detection Device (player)",
			                           message="beep",
			                           location=[-2185, 28, 198])

		# Simply make sure that a BeepEvent was created
		self.assertIsInstance(beep_event_message, BeepEvent)


	def test_valid_creation_ndarray_location(self):
		"""
		Test creating a valid BeepEvent message, providing a numpy array as the
		location argument as opposed to a tuple.
		"""

		beep_event_message = BeepEvent(mission_timer="8 : 36",
			                           elapsed_milliseconds=15113,
			                           sourceEntity="Victim Detection Device (player)",
			                           message="beep",
			                           location=np.array([-2185, 28, 198]))

		# Simply make sure that a BeepEvent was created
		self.assertIsInstance(beep_event_message, BeepEvent)


	def test_invalid_creation_2D_ndarray_location(self):
		"""
		Test creating a valid BeepEvent message, providing a non-1D numpy array
		as the location argument

		Trying to create the BeepEvent message with a numpy array 
		will raise a MalformedMessageCreationException
		"""

		# Make sure that the exception is raised
		with self.assertRaises(MalformedMessageCreationException):

			beep_event_message = BeepEvent(mission_timer="8 : 36",
				                           elapsed_milliseconds=15113,
				                           sourceEntity="Victim Detection Device (player)",
				                           message="beep",
			    	                       location=np.array([[-2185, 28, 198]]))		


	def test_invalid_creation_no_source_entity(self):
		"""
		Test creating a valid BeepEvent message, without a provided 
		"sourceEntity" keyword.

		Trying to create a BeepEvent without the sourceEntity should raise a
		MissingMessageArgumentException
		"""

		# Make sure that the exception is raised
		with self.assertRaises(MissingMessageArgumentException):

			beep_event_message = BeepEvent(missionTimer="8 : 36",
				                           elapsed_milliseconds=15113,
				                           message="beep",
				                           location=(-2185, 28, 198))


	def test_invalid_creation_no_message(self):
		"""
		Test creating a valid BeepEvent message, without a provided 
		"message" keyword.

		Trying to create a BeepEvent without the message should raise a
		MissingMessageArgumentException
		"""

		# Make sure that the exception is raised
		with self.assertRaises(MissingMessageArgumentException):

			beep_event_message = BeepEvent(missionTimer="8 : 36",
				                           elapsed_milliseconds=15113,
				                           sourceEntity="Victim Detection Device (player)",
				                           location=(-2185, 28, 198))


	def test_invalid_creation_no_location(self):
		"""
		Test creating a valid BeepEvent message, without a provided 
		"location" keyword.

		Trying to create a BeepEvent without the location should raise a
		MissingMessageArgumentException
		"""

		# Make sure that the exception is raised
		with self.assertRaises(MissingMessageArgumentException):

			beep_event_message = BeepEvent(missionTimer="8 : 36",
				                           elapsed_milliseconds=15113,
				                           sourceEntity="Victim Detection Device (player)",
				                           message="beep")


	def test_invalid_creation_insufficient_location_entries(self):
		"""
		Test creating a valid BeepEvent message, providing too few entries for
		the location.

		Trying to create the BeepEvent message without a triple for location
		will raise a MalformedMessageCreationException
		"""

		# Make sure that the exception is raised
		with self.assertRaises(MalformedMessageCreationException):

			beep_event_message = BeepEvent(mission_timer="8 : 36",
				                           elapsed_milliseconds=15113,
				                           sourceEntity="Victim Detection Device (player)",
				                           message="beep",
			    	                       location=(-2185, 28))


	def test_valid_creation_extra_location_entries(self):
		"""
		Test creating a valid BeepEvent message, providing too many entries for
		the location.

		Trying to create the BeepEvent message extra location entries should 
		still result in a valid message being created.
		"""

		beep_event_message = BeepEvent(mission_timer="8 : 36",
			                           elapsed_milliseconds=15113,
			                           sourceEntity="Victim Detection Device (player)",
			                           message="beep",
		    	                       location=(-2185, 28, 198, -52))

		# Simply make sure that a BeepEvent was created
		self.assertIsInstance(beep_event_message, BeepEvent)		


	def test_invalid_creation_non_listlike_location(self):
		"""
		Test creating a valid BeepEvent message, providing a location argument
		that is not list-like.

		Trying to create the BeepEvent message without a list or similar for 
		location will raise a MalformedMessageCreationException
		"""

		# Make sure that the exception is raised
		with self.assertRaises(MalformedMessageCreationException):

			beep_event_message = BeepEvent(mission_timer="8 : 36",
				                           elapsed_milliseconds=15113,
				                           sourceEntity="Victim Detection Device (player)",
				                           message="beep",
			    	                       location="<NOT_A_TUPLE>")





class BeepEventTests(unittest.TestCase):
	"""
	A set of test cases to ensure proper behavior of a properly created
	BeepEvent messages.
	"""

	def setUp(self):
		"""
		Create a valid BeepEvent message to evaluate behavior
		"""

		self.beep_event_message = BeepEvent(mission_timer="8 : 36",
			                                elapsed_milliseconds=15113,
			                                sourceEntity="Victim Detection Device (player)",
			                                message="beep",
			                                location=(-2185, 28, 198))

	def test_mission_timer_getter(self):
		"""
		Test accessing the mission timer of the beep event message.

		Should return (8,36)
		"""

		self.assertEqual(self.beep_event_message.mission_timer, (8,36))


	def test_mission_timer_setter(self):
		"""
		Test setting the mission timer of the beep event message.

		Should raise an ImmutableAttributeException.
		"""

		# Make sure that the exception is raised
		with self.assertRaises(ImmutableAttributeException):

			self.beep_event_message.mission_timer = (9,12)


	def test_elapsed_milliseconds_getter(self):
		"""
		Test accessing the elapsed milliseconds attribute of the beep event
		message.

		Should return 15113
		"""

		self.assertEqual(self.beep_event_message.elapsed_milliseconds, 15113)


	def test_elapsed_milliseconds_setter(self):
		"""
		Test setting the elapsed milliseconds attrubte of the beep message

		Should raise an ImmutableAttributeException
		"""

		# Make sure that the exception is raised
		with self.assertRaises(ImmutableAttributeException):

			self.beep_event_message.elapsed_milliseconds = 1000


	def test_sourceEntity_getter(self):
		"""
		Test accessing the sourceEntity attribute of the beep event
		message.

		Should return "Victim Detection Device (player)"
		"""

		self.assertEqual(self.beep_event_message.sourceEntity, "Victim Detection Device (player)")


	def test_sourceEntity_setter(self):
		"""
		Test setting the sourceEntity attrubte of the beep message

		Should raise an ImmutableAttributeException
		"""

		# Make sure that the exception is raised
		with self.assertRaises(ImmutableAttributeException):

			self.beep_event_message.sourceEntity = "Victim Detection Device"


	def test_source_entity_getter(self):
		"""
		Test accessing the source_entity attribute of the beep event
		message.

		Should return "Victim Detection Device (player)"
		"""

		self.assertEqual(self.beep_event_message.source_entity, "Victim Detection Device (player)")


	def test_source_entity_setter(self):
		"""
		Test setting the source_entity attrubte of the beep message

		Should raise an ImmutableAttributeException
		"""

		# Make sure that the exception is raised
		with self.assertRaises(ImmutableAttributeException):

			self.beep_event_message.source_entity = "Victim Detection Device"


	def test_message_getter(self):
		"""
		Test accessing the message attribute of the beep event
		message.

		Should return "beep"
		"""

		self.assertEqual(self.beep_event_message.message, "beep")


	def test_message_setter(self):
		"""
		Test setting the message attrubte of the beep message

		Should raise an ImmutableAttributeException
		"""

		# Make sure that the exception is raised
		with self.assertRaises(ImmutableAttributeException):

			self.beep_event_message.message = "beep beep"


	def test_location_getter(self):
		"""
		Test accessing the location attribute of the beep event
		message.

		Should return (-2185, 28, 198)
		"""

		self.assertEqual(self.beep_event_message.location, (-2185, 28, 198))


	def test_location_setter(self):
		"""
		Test setting the location attrubte of the beep message

		Should raise an ImmutableAttributeException
		"""

		# Make sure that the exception is raised
		with self.assertRaises(ImmutableAttributeException):

			self.beep_event_message.location = (-2185, 26, 198)


	def test_beep_x_getter(self):
		"""
		Test accessing the beep_x attribute of the beep event
		message.

		Should return -2185
		"""

		self.assertEqual(self.beep_event_message.beep_x, -2185)


	def test_beep_x_setter(self):
		"""
		Test setting the beep_x attrubte of the beep message

		Should raise an ImmutableAttributeException
		"""

		# Make sure that the exception is raised
		with self.assertRaises(ImmutableAttributeException):

			self.beep_event_message.beep_x = -2186


	def test_beep_y_getter(self):
		"""
		Test accessing the beep_y attribute of the beep event
		message.

		Should return -2185
		"""

		self.assertEqual(self.beep_event_message.beep_y, 28)


	def test_beep_y_setter(self):
		"""
		Test setting the beep_y attrubte of the beep message

		Should raise an ImmutableAttributeException
		"""

		# Make sure that the exception is raised
		with self.assertRaises(ImmutableAttributeException):

			self.beep_event_message.beep_y = 86

	def test_beep_z_getter(self):
		"""
		Test accessing the beep_z attribute of the beep event
		message.

		Should return 198
		"""

		self.assertEqual(self.beep_event_message.beep_z, 198)


	def test_beep_z_setter(self):
		"""
		Test setting the beep_z attrubte of the beep message

		Should raise an ImmutableAttributeException
		"""

		# Make sure that the exception is raised
		with self.assertRaises(ImmutableAttributeException):

			self.beep_event_message.beep_z = 199


	def test_to_dictionary(self):
		"""
		Test that the conversion to a dictionary format is correct
		"""

		self.assertDictEqual(self.beep_event_message.toDict(),
			                 {'data': { 'source_entity': "Victim Detection Device (player)",
			                            'mission_timer': "8 : 36",
			                            'elapsed_milliseconds': 15113,
			                            'message': "beep",
			                            'beep_x': -2185,
			                            'beep_y': 28,
			                            'beep_z': 198
			                 }})