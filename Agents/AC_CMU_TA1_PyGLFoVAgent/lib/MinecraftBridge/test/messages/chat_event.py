# -*- coding: utf-8 -*-
"""
.. module:: chat_event
   :platform: Linux, Windows, OSX
   :synopsis: Unit tests for ChatEvent messages

.. moduleauthor:: Dana Hughes <danahugh@andrew.cmu.edu>

Suite of unit tests for ChatEvent messages
"""

from MinecraftBridge.messages import ChatEvent
from MinecraftBridge.messages.message_exceptions import (
	MissingMessageArgumentException,
	MalformedMessageCreationException,
	ImmutableAttributeException
)

import unittest


class ChatEventCreationTests(unittest.TestCase):
	"""
	A set of test cases to ensure proper behavior during creation of ChatEvent
	messages.
	"""

	def test_valid_creation_with_mission_timer(self):
		"""
		Test creating a valid ChatEvent message, using a string representation
		of the mission time, and the "mission_timer" keyword argument.
		"""

		chat_event_message = ChatEvent(mission_timer="8 : 36",
			                           elapsed_milliseconds=15113,
			                           sender="Aptiminer1",
			                           addressees=["Player746"],
			                           text="I'm in room 210")

		# Simply make sure that a ChatEvent was created
		self.assertIsInstance(chat_event_message, ChatEvent)


	def test_valid_creation_with_missionTimer(self):
		"""
		Test creating a valid ChatEvent message, using a string representation
		of the mission time, and the "missionTimer" keyword argument.
		"""

		chat_event_message = ChatEvent(missionTimer="8 : 36",
			                           elapsed_milliseconds=15113,
			                           sender="Aptiminer1",
			                           addressees=["Player746"],
			                           text="I'm in room 210")

		# Simply make sure that a ChatEvent was created
		self.assertIsInstance(chat_event_message, ChatEvent)


	def test_valid_creation_no_mission_timer(self):
		"""
		Test creating a valid ChatEvent message, without providing the 
		"mission_timer" keyword argument.
		"""

		chat_event_message = ChatEvent(elapsed_milliseconds=15113,
			                            sender="Aptiminer1",
			                            addressees=["Player746"],
			                            text="I'm in room 210")

		# Simply make sure that a ChatEvent was created
		self.assertIsInstance(chat_event_message, ChatEvent)


	def test_valid_creation_no_elapsed_milliseconds(self):
		"""
		Test creating a valid ChatEvent message, without providing elaped
		milliseconds as part of the keyword arguments
		"""

		chat_event_message = ChatEvent(mission_timer="8 : 36",
			                           sender="Aptiminer1",
			                           addressees=["Player746"],
			                           text="I'm in room 210")

		# Simply make sure that a ChatEvent was created
		self.assertIsInstance(chat_event_message, ChatEvent)


	def test_valid_creation_no_mission_timer_or_elapsed_milliseconds(self):
		"""
		Test creating a valid ChatEvent message, without providing elaped
		milliseconds or mission timer as part of the keyword arguments
		"""

		chat_event_message = ChatEvent(sender="Aptiminer1",
			                           addressees=["Player746"],
			                           text="I'm in room 210")

		# Simply make sure that a ChatEvent was created
		self.assertIsInstance(chat_event_message, ChatEvent)



	def test_valid_creation_tuple_addressees(self):
		"""
		Test creating a valid ChatEvent message, providing a tuple as the
		addressees argument as opposed to a tuple.
		"""

		chat_event_message = ChatEvent(missionTimer="8 : 36",
			                           elapsed_milliseconds=15113,
			                           sender="Aptiminer1",
			                           addressees=("Player746", "Player112"),
			                           text="I'm in room 210")

		# Simply make sure that a ChatEvent was created
		self.assertIsInstance(chat_event_message, ChatEvent)


	def test_invalid_creation_no_sender(self):
		"""
		Test creating a valid  ChatEvent message, without a provided 
		"sender" keyword.

		Trying to create a ChatEvent without the sender should raise a
		MissingMessageArgumentException
		"""

		# Make sure that the exception is raised
		with self.assertRaises(MissingMessageArgumentException):
			chat_event_message = ChatEvent(mission_timer="8 : 36",
				                            elapsed_milliseconds=15113,
			                               addressees=["Player746"],
			                               text="I'm in room 210")


	def test_invalid_creation_no_addressees(self):
		"""
		Test creating a valid  ChatEvent message, without a provided 
		"addressees" keyword.

		Trying to create a ChatEvent without the addressees should raise a
		MissingMessageArgumentException
		"""

		# Make sure that the exception is raised
		with self.assertRaises(MissingMessageArgumentException):
			chat_event_message = ChatEvent(mission_timer="8 : 36",
				                            elapsed_milliseconds=15113,
			                               sender="Aptiminer1",
			                               text="I'm in room 210")


	def test_invalid_creation_no_text(self):
		"""
		Test creating a valid  ChatEvent message, without a provided 
		"text" keyword.

		Trying to create a ChatEvent without the text should raise a
		MissingMessageArgumentException
		"""

		# Make sure that the exception is raised
		with self.assertRaises(MissingMessageArgumentException):
			chat_event_message = ChatEvent(mission_timer="8 : 36",
				                            elapsed_milliseconds=15113,
			                               sender="Aptiminer1",
			                               addressees=["Player746"])


	def test_invalid_creation_non_listlike_addressees(self):
		"""
		Test creating a valid ChatEvent message, providing an addressees argument
		that is not list-like.

		Trying to create the ChatEvent message without a list or similar for 
		addressee will raise a MalformedMessageCreationException
		"""

		# Make sure that the exception is raised
		with self.assertRaises(MalformedMessageCreationException):

			chat_event_message = ChatEvent(missionTimer="8 : 36",
			                               elapsed_milliseconds=15113,
			                               sender="Aptiminer1",
			                               addressees="Player746",
			                               text="I'm in room 210")





class ChatEventTests(unittest.TestCase):
	"""
	A set of test cases to ensure proper behavior of a properly created
	ChatEvent messages.
	"""

	def setUp(self):
		"""
		Create a valid ChatEvent message to evaluate behavior
		"""

		self.chat_event_message = ChatEvent(mission_timer="8 : 36",
			                           elapsed_milliseconds=15113,
			                           sender="Aptiminer1",
			                           addressees=["Player746"],
			                           text="I'm in room 210")

	def test_mission_timer_getter(self):
		"""
		Test accessing the mission timer.

		Should return (8,36)
		"""

		self.assertEqual(self.chat_event_message.mission_timer, (8,36))


	def test_mission_timer_setter(self):
		"""
		Test setting the mission timer.

		Should raise an ImmutableAttributeException.
		"""

		# Make sure that the exception is raised
		with self.assertRaises(ImmutableAttributeException):

			self.chat_event_message.mission_timer = (9,12)


	def test_elapsed_milliseconds_getter(self):
		"""
		Test accessing the elapsed milliseconds attribute.

		Should return 15113
		"""

		self.assertEqual(self.chat_event_message.elapsed_milliseconds, 15113)


	def test_elapsed_milliseconds_setter(self):
		"""
		Test setting the elapsed milliseconds attrubte

		Should raise an ImmutableAttributeException
		"""

		# Make sure that the exception is raised
		with self.assertRaises(ImmutableAttributeException):

			self.chat_event_message.elapsed_milliseconds = 1000


	def test_sender_getter(self):
		"""
		Test accessing the sender attribute

		Should return "Aptiminer1"
		"""

		self.assertEqual(self.chat_event_message.sender, "Aptiminer1")


	def test_sender_setter(self):
		"""
		Test setting the ssender attrubte

		Should raise an ImmutableAttributeException
		"""

		# Make sure that the exception is raised
		with self.assertRaises(ImmutableAttributeException):

			self.chat_event_message.sender = "McSillypants"


	def test_addressees_getter(self):
		"""
		Test accessing the addressees attribute

		Should return ("Player746")
		"""

		self.assertEqual(self.chat_event_message.addressees, ("Player746",))


	def test_addressees_setter(self):
		"""
		Test setting the addressees attrubte

		Should raise an ImmutableAttributeException
		"""

		# Make sure that the exception is raised
		with self.assertRaises(ImmutableAttributeException):

			self.chat_event_message.addressees = ["McSillypants"]


	def test_text_getter(self):
		"""
		Test accessing the text attribute

		Should return "I'm in room 210"
		"""

		self.assertEqual(self.chat_event_message.text, "I'm in room 210")


	def test_text_setter(self):
		"""
		Test setting the ssender attrubte

		Should raise an ImmutableAttributeException
		"""

		# Make sure that the exception is raised
		with self.assertRaises(ImmutableAttributeException):

			self.chat_event_message.text = "McSillypants"			


	def test_to_dictionary(self):
		"""
		Test that the conversion to a dictionary format is correct
		"""

		self.assertDictEqual(self.chat_event_message.toDict(),
			                 {'data': { 'mission_timer': "8 : 36",
			                            'elapsed_milliseconds': 15113,
			                            'sender': "Aptiminer1",
			                            'addressees': ("Player746",),
			                            'text': "I'm in room 210"
			                 }})