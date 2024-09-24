# -*- coding: utf-8 -*-
"""
.. module:: parser_exceptions
   :platform: Linux, Windows, OSX
   :synopsis: Exception classes for MQTT message parsing

.. moduleauthor:: Dana Hughes <danahugh@andrew.cmu.edu>

A set of user-defined exception classes for handling message parsing errors
"""


class MissingHeaderException(Exception):
	"""
	Exception raised when trying to create a message object with incompatible
	arguments

	Attributes
	----------
	message : dictionary
	    Dictonary of the message being parsed with the missing header
	"""

	def __init__(self, message):
		
		self.message = message
		self.error_message = "Missing header."

		Exception.__init__(self, self.message)

