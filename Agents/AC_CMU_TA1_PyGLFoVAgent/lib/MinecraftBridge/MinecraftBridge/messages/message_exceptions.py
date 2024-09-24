# -*- coding: utf-8 -*-
"""
.. module:: message_exceptions
   :platform: Linux, Windows, OSX
   :synopsis: Exception classes for messages

.. moduleauthor:: Dana Hughes <danahugh@andrew.cmu.edu>

A set of user-defined exception classes for handling message-based errors
"""


class MalformedMessageCreationException(Exception):
	"""
	Exception raised when trying to create a message object with incompatible
	arguments

	Attributes:
		message_class - message class attempted to be created
		attribute     - name of the attribute that was malformed
		value         - value passed to the attribute during creation
	"""

	def __init__(self, message_class, attribute, value):
		
		self.message_class = message_class
		self.attribute = attribute
		self.value = value
		self.message = f"Unable to assign '{self.value}' to class '{self.message_class}' attribute '{self.attribute}'"

		Exception.__init__(self, self.message)


class MissingMessageArgumentException(Exception):
	"""
	Exception raised when trying to create a message with missing arguments

	Attributes:
		message_class - message class attempted to be created
		argument_name - name of the missing argument
	"""

	def __init__(self, message_class, argument_name):

		self.message_class = message_class
		self.argument_name = argument_name
		self.message = f"Missing argument '{self.argument_name}' for class '{self.message_class}'"

		Exception.__init__(self, self.message)


class ImmutableAttributeException(Exception):
	"""
	Exception raised when trying to set the value of an immutable attribute in
	a message instance.
	"""

	def __init__(self, message_class, attribute_name):

		self.message_class = message_class
		self.attribute_name = attribute_name
		self.message = f"Unable to assign to immutable attribute '{self.attribute_name}' for class '{self.message_class}'"

		Exception.__init__(self, self.message)
		

class BadHeaderNameException(Exception):
	"""
	Exception raised when trying to add a header to a message using a nonstring
	header name

	Attributes:
	"""

	def __init__(self):

		pass