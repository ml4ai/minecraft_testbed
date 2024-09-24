# -*- coding: utf-8 -*-
"""
.. module:: competency_task_event
   :platform: Linux, Windows, OSX
   :synopsis: Unit tests for CompetencyTaskEvent messages

.. moduleauthor:: Dana Hughes <danahugh@andrew.cmu.edu>

Suite of unit tests for CompetencyTaskEvent messages
"""

from MinecraftBridge.messages import CompetencyTaskEvent
from MinecraftBridge.messages.message_exceptions import (
	MissingMessageArgumentException,
	MalformedMessageCreationException,
	ImmutableAttributeException
)

import unittest


class CompetencyTaskEventCreationTests(unittest.TestCase):
	"""
	A set of test cases to ensure proper behavior during creation of ChatEvent
	messages.
	"""

	def test_valid_creation_with_taskMessage(self):
		"""
		Test creating a valid CompetencyEvent message, providing only the 
		`taskMessage` keyword argument
		"""

		message = CompetencyTaskEvent(taskMessage="Task 13 Complete.")

		# Simply make sure that a CompetencyEvent was created
		self.assertIsInstance(message, CompetencyTaskEvent)


	@unittest.expectedFailure
	def test_valid_creation_with_task_message(self):
		"""
		Test creating a valid CompetencyEvent message, providing only the 
		`taskMessage` keyword argument.

		NOTE:  This unittest is expected to fail, as the message does not accept
		       `task_message` as an argument.  This is planned to be fixed.
		"""

		message = CompetencyTaskEvent(task_message="Task 13 Complete.")

		# Simply make sure that a CompetencyEvent was created
		self.assertIsInstance(message, CompetencyTaskEvent)


	def test_valid_creation_with_playerName(self):
		"""
		Test creating a valid CompetencyEvent message, providing the 
		`playerName` keyword argument
		"""

		message = CompetencyTaskEvent(taskMessage="Task 13 Complete.",
			                           playerName="BLUE_ASIST1")

		# Simply make sure that a CompetencyEvent was created
		self.assertIsInstance(message, CompetencyTaskEvent)		


	def test_valid_creation_with_callSign(self):
		"""
		Test creating a valid CompetencyEvent message, providing the 
		`callSign` keyword argument
		"""

		message = CompetencyTaskEvent(taskMessage="Task 13 Complete.",
			                           callSign="Blue")

		# Simply make sure that a CompetencyEvent was created
		self.assertIsInstance(message, CompetencyTaskEvent)		


	def test_valid_creation_with_playerName_and_callSign(self):
		"""
		Test creating a valid CompetencyEvent message, providing the 
		`playerName` and `callSign` keyword argument
		"""

		message = CompetencyTaskEvent(taskMessage="Task 13 Complete.",
			                           playerName="BLUE_ASIST1",
			                           callSign="Blue")


	def test_invalid_creation_no_taskMessage(self):
		"""
		Test an invalid CompetencyEvent creation, with no taskMessage 
		provided.

		Expected behavior is to raise a `MissingMessageArgumentException`
		"""
		# Make sure that the exception is raised
		with self.assertRaises(MissingMessageArgumentException):
			message = CompetencyTaskEvent(playerName="BLUE_ASIST1",
				                           callSign="Blue")

		



class CompetencyTaskEventTests(unittest.TestCase):
	"""
	A set of test cases to ensure proper behavior of a properly created
	ChatEvent messages.
	"""

	def setUp(self):
		"""
		Create a valid ChatEvent message to evaluate behavior
		"""

		self.message = CompetencyTaskEvent(taskMessage="Task 13 Complete.",
			                            playerName="BLUE_ASIST1",
			                            callSign="Blue")


	def test_mission_timer_getter(self):
		"""
		Test accessing the mission timer.

		Should return (-1, -1)
		"""

		self.assertEqual(self.message.mission_timer, (-1,-1))


	def test_mission_timer_setter(self):
		"""
		Test setting the mission timer.

		Should raise an ImmutableAttributeException.
		"""

		# Make sure that the exception is raised
		with self.assertRaises(ImmutableAttributeException):

			self.message.mission_timer = (9,12)


	def test_elapsed_milliseconds_getter(self):
		"""
		Test accessing the elapsed milliseconds attribute.

		Should return -1
		"""

		self.assertEqual(self.message.elapsed_milliseconds, -1)


	def test_elapsed_milliseconds_setter(self):
		"""
		Test setting the elapsed milliseconds attrubte

		Should raise an ImmutableAttributeException
		"""

		# Make sure that the exception is raised
		with self.assertRaises(ImmutableAttributeException):

			self.message.elapsed_milliseconds = 1000

		self.message = CompetencyTaskEvent(taskMessage="Task 13 Complete.",
			                            playerName="BLUE_ASIST1",
			                            callSign="Blue")


	def test_taskMessage_getter(self):
		"""
		Test accessing the `taskMessage` attribute

		Should return "Task 13 Complete."
		"""

		self.assertEqual(self.message.taskMessage, "Task 13 Complete.")


	def test_taskMessage_setter(self):
		"""
		Test setting the `taskMessage` attrubte

		Should raise an ImmutableAttributeException
		"""

		# Make sure that the exception is raised
		with self.assertRaises(ImmutableAttributeException):

			self.message.taskMessage = "Task 14 Complete."
			

	def test_task_message_getter(self):
		"""
		Test accessing the `task_message` attribute

		Should return "Task 13 Complete."
		"""

		self.assertEqual(self.message.task_message, "Task 13 Complete.")


	def test_task_message_setter(self):
		"""
		Test setting the `task_message` attrubte

		Should raise an ImmutableAttributeException
		"""

		# Make sure that the exception is raised
		with self.assertRaises(ImmutableAttributeException):

			self.message.task_message = "Task 14 Complete."			


	def test_playerName_getter(self):
		"""
		Test accessing the `playerName` attribute

		Should return "BLUE_ASIST1."
		"""

		self.assertEqual(self.message.playerName, "BLUE_ASIST1")


	def test_playerName_setter(self):
		"""
		Test setting the `playerName` attrubte

		Should raise an ImmutableAttributeException
		"""

		# Make sure that the exception is raised
		with self.assertRaises(ImmutableAttributeException):

			self.message.playerName = "RED_ASIST1"


	def test_callSign_getter(self):
		"""
		Test accessing the `callSign` attribute

		Should return "Blue"
		"""

		self.assertEqual(self.message.callSign, "Blue")


	def test_callSign_setter(self):
		"""
		Test setting the `callSign` attrubte

		Should raise an ImmutableAttributeException
		"""

		# Make sure that the exception is raised
		with self.assertRaises(ImmutableAttributeException):

			self.message.callSign = "Task 14 Complete."			


	def test_to_dictionary(self):
		"""
		Test that the conversion to a dictionary format is correct
		"""

		self.assertDictEqual(self.message.toDict(),
			                 {'data': { 'task_message': "Task 13 Complete.",
			                            'playerName': "BLUE_ASIST1",
			                            'callSign': "Blue"
			                 }})